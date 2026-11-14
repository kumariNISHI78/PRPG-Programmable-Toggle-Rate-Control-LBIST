--------------------------------------------------------------------------------
-- Project   : Scan-Based LBIST with Programmable Toggle-Rate Control
-- File      : toggle_rate_controller.vhd
-- Role      : Member 2 - PRPG and Toggle-Rate Control
-- Design    : Programmable Toggle-Rate Controller & Activity Monitor
-- Standard  : IEEE 1076-2008 (VHDL-2008) / Synthesizable RTL
--------------------------------------------------------------------------------
-- Description:
--   Decodes target toggle rates (10%, 20%, 30%, 40%, 50%, 60%, Bypass, Custom).
--   Features:
--     1. Fractional Dither Accumulator: Dynamically alternates integer limits
--        to hit exact average fractional target toggle rates for parallel vectors.
--     2. Bresenham Rate Multiplier: Generates exact serial toggle-enable pulses
--        for serial scan chain shifting.
--     3. Cumulative Activity Measurement: Tracks total transitions, total patterns,
--        total shift bits, and real-time average toggle percentage.
--     4. Dynamic on-the-fly target configuration without requiring reset.
--------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity toggle_rate_controller is
    generic (
        WIDTH : positive := 16
    );
    port (
        clk                  : in  std_logic;
        rst_n                : in  std_logic;
        enable               : in  std_logic;
        -- Target toggle-rate selection:
        -- "000": 10%, "001": 20%, "010": 30%, "011": 40%, "100": 50%, "101": 60%,
        -- "110": Bypass (100% PRPG passthrough), "111": Custom direct limit
        target_rate_sel      : in  std_logic_vector(2 downto 0);
        custom_toggle_limit  : in  unsigned(4 downto 0);
        
        -- Control outputs to pattern modifier
        active_toggle_limit  : out unsigned(4 downto 0);
        serial_toggle_enable : out std_logic;
        bypass_mode          : out std_logic;
        
        -- Activity metrics from pattern modifier
        actual_toggles_in    : in  unsigned(4 downto 0);
        serial_bit_toggled   : in  std_logic;
        
        -- Cumulative activity statistics outputs
        total_word_toggles   : out unsigned(31 downto 0);
        total_patterns_gen   : out unsigned(31 downto 0);
        total_serial_toggles : out unsigned(31 downto 0);
        total_serial_shifts  : out unsigned(31 downto 0);
        measured_toggle_rate : out unsigned(7 downto 0) -- Scaled 0 to 100%
    );
end entity toggle_rate_controller;

architecture rtl of toggle_rate_controller is

    -- Target percentage (0 to 100)
    signal target_pct          : unsigned(7 downto 0);
    signal is_bypass           : std_logic;
    
    -- Fractional toggle budget dither accumulator (for parallel word matching)
    -- Accumulates remainder to achieve exact average fractional counts
    signal frac_accum          : unsigned(7 downto 0);
    signal current_limit       : unsigned(4 downto 0);
    
    -- Bresenham serial rate accumulator
    signal serial_accum        : unsigned(7 downto 0);
    signal serial_en_reg       : std_logic;
    
    -- Statistics accumulators
    signal word_toggle_acc     : unsigned(31 downto 0);
    signal pattern_count_acc   : unsigned(31 downto 0);
    signal serial_toggle_acc   : unsigned(31 downto 0);
    signal serial_shift_acc    : unsigned(31 downto 0);

begin

    bypass_mode <= is_bypass;
    active_toggle_limit <= current_limit;
    serial_toggle_enable <= serial_en_reg;

    -- Decode Target Toggle Rate Selection
    process(target_rate_sel, custom_toggle_limit)
    begin
        is_bypass <= '0';
        case target_rate_sel is
            when "000" => target_pct <= to_unsigned(10, 8); -- 10%
            when "001" => target_pct <= to_unsigned(20, 8); -- 20%
            when "010" => target_pct <= to_unsigned(30, 8); -- 30%
            when "011" => target_pct <= to_unsigned(40, 8); -- 40%
            when "100" => target_pct <= to_unsigned(50, 8); -- 50%
            when "101" => target_pct <= to_unsigned(60, 8); -- 60%
            when "110" => 
                target_pct <= to_unsigned(100, 8);          -- Bypass (unmodified PRPG)
                is_bypass  <= '1';
            when "111" => 
                target_pct <= resize(custom_toggle_limit * 6, 8); -- Custom approx
            when others =>
                target_pct <= to_unsigned(50, 8);
        end case;
    end process;

    -- Dynamic Toggle Limit Generation (Fractional Dithering for Parallel Vectors)
    -- Computes limit per cycle:
    -- Target for 16-bit:
    -- 10% -> 1.6 avg (base 1, +1 when frac_accum >= 100)
    -- 20% -> 3.2 avg (base 3, +1 when frac_accum >= 100)
    -- 30% -> 4.8 avg (base 4, +1 when frac_accum >= 100)
    -- 40% -> 6.4 avg (base 6, +1 when frac_accum >= 100)
    -- 50% -> 8.0 avg (base 8)
    -- 60% -> 9.6 avg (base 9, +1 when frac_accum >= 100)
    process(clk, rst_n)
        variable next_accum : unsigned(7 downto 0);
    begin
        if rst_n = '0' then
            frac_accum    <= (others => '0');
            current_limit <= to_unsigned(8, 5);
        elsif rising_edge(clk) then
            if enable = '1' then
                if is_bypass = '1' then
                    current_limit <= to_unsigned(WIDTH, 5); -- Allow all transitions
                    frac_accum    <= (others => '0');
                elsif target_rate_sel = "111" then
                    current_limit <= custom_toggle_limit;
                else
                    case target_rate_sel is
                        when "000" => -- 10% target: average 1.6 toggles -> base 1, fraction 60/100
                            next_accum := frac_accum + 60;
                            if next_accum >= 100 then
                                frac_accum    <= next_accum - 100;
                                current_limit <= to_unsigned(2, 5);
                            else
                                frac_accum    <= next_accum;
                                current_limit <= to_unsigned(1, 5);
                            end if;

                        when "001" => -- 20% target: average 3.2 toggles -> base 3, fraction 20/100
                            next_accum := frac_accum + 20;
                            if next_accum >= 100 then
                                frac_accum    <= next_accum - 100;
                                current_limit <= to_unsigned(4, 5);
                            else
                                frac_accum    <= next_accum;
                                current_limit <= to_unsigned(3, 5);
                            end if;

                        when "010" => -- 30% target: average 4.8 toggles -> base 4, fraction 80/100
                            next_accum := frac_accum + 80;
                            if next_accum >= 100 then
                                frac_accum    <= next_accum - 100;
                                current_limit <= to_unsigned(5, 5);
                            else
                                frac_accum    <= next_accum;
                                current_limit <= to_unsigned(4, 5);
                            end if;

                        when "011" => -- 40% target: average 6.4 toggles -> base 6, fraction 40/100
                            next_accum := frac_accum + 40;
                            if next_accum >= 100 then
                                frac_accum    <= next_accum - 100;
                                current_limit <= to_unsigned(7, 5);
                            else
                                frac_accum    <= next_accum;
                                current_limit <= to_unsigned(6, 5);
                            end if;

                        when "100" => -- 50% target: exact 8 toggles
                            frac_accum    <= (others => '0');
                            current_limit <= to_unsigned(8, 5);

                        when "101" => -- 60% target: average 9.6 toggles -> base 9, fraction 60/100
                            next_accum := frac_accum + 60;
                            if next_accum >= 100 then
                                frac_accum    <= next_accum - 100;
                                current_limit <= to_unsigned(10, 5);
                            else
                                frac_accum    <= next_accum;
                                current_limit <= to_unsigned(9, 5);
                            end if;

                        when others =>
                            current_limit <= to_unsigned(8, 5);
                    end case;
                end if;
            end if;
        end if;
    end process;

    -- Bresenham Rate Multiplier for Serial Scan Shift Transitions
    process(clk, rst_n)
        variable next_ser : unsigned(7 downto 0);
    begin
        if rst_n = '0' then
            serial_accum  <= (others => '0');
            serial_en_reg <= '1';
        elsif rising_edge(clk) then
            if enable = '1' then
                if is_bypass = '1' then
                    serial_en_reg <= '1';
                    serial_accum  <= (others => '0');
                else
                    next_ser := serial_accum + target_pct;
                    if next_ser >= 100 then
                        serial_accum  <= next_ser - 100;
                        serial_en_reg <= '1'; -- Grant serial transition
                    else
                        serial_accum  <= next_ser;
                        serial_en_reg <= '0'; -- Suppress serial transition
                    end if;
                end if;
            end if;
        end if;
    end process;

    -- Cumulative Statistical Activity Monitoring Process
    process(clk, rst_n)
    begin
        if rst_n = '0' then
            word_toggle_acc   <= (others => '0');
            pattern_count_acc <= (others => '0');
            serial_toggle_acc <= (others => '0');
            serial_shift_acc  <= (others => '0');
        elsif rising_edge(clk) then
            if enable = '1' then
                word_toggle_acc   <= word_toggle_acc + resize(actual_toggles_in, 32);
                pattern_count_acc <= pattern_count_acc + 1;
                
                if serial_bit_toggled = '1' then
                    serial_toggle_acc <= serial_toggle_acc + 1;
                end if;
                serial_shift_acc <= serial_shift_acc + 1;
            end if;
        end if;
    end process;

    -- Output Stats
    total_word_toggles   <= word_toggle_acc;
    total_patterns_gen   <= pattern_count_acc;
    total_serial_toggles <= serial_toggle_acc;
    total_serial_shifts  <= serial_shift_acc;

    -- Real-time measured toggle rate estimation (scaled percentage)
    -- Approximated for display in simulation: (total_word_toggles * 100) / (total_patterns_gen * WIDTH)
    process(word_toggle_acc, pattern_count_acc)
        variable total_bits_mult : unsigned(47 downto 0);
        variable pct_calc_mult   : unsigned(47 downto 0);
    begin
        total_bits_mult := pattern_count_acc * to_unsigned(WIDTH, 16);
        if total_bits_mult > 0 then
            pct_calc_mult := (word_toggle_acc * to_unsigned(100, 16)) / total_bits_mult;
            measured_toggle_rate <= resize(pct_calc_mult(7 downto 0), 8);
        else
            measured_toggle_rate <= (others => '0');
        end if;
    end process;

end architecture rtl;

