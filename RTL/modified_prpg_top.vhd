--------------------------------------------------------------------------------
-- Project   : Scan-Based LBIST with Programmable Toggle-Rate Control
-- File      : modified_prpg_top.vhd
-- Role      : Member 2 - PRPG and Toggle-Rate Control
-- Design    : Top-Level Toggle-Controlled PRPG Architecture
-- Standard  : IEEE 1076-2008 (VHDL-2008) / Synthesizable RTL
--------------------------------------------------------------------------------
-- Description:
--   Top-level module for Member 2 integrating:
--     1. LFSR PRPG Core (maximal-length Galois LFSR with anti-lockup)
--     2. Combinational Hamming Distance / Popcount unit
--     3. Programmable Toggle-Rate Controller (10% to 60%, Bypass, Custom)
--     4. Dual-Domain Rotating Transition Suppression Pattern Modifier
--     5. Cumulative Activity & Statistics Monitoring
--   Provides clean interface for:
--     - Member 1: Scan Chain Interface (Parallel scan vectors & serial scan bit)
--     - Member 3: LBIST Controller Handshake (Enable, target rate, stats, seed load)
--------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity modified_prpg_top is
    generic (
        WIDTH        : positive := 16;
        POLYNOMIAL   : std_logic_vector(15 downto 0) := x"B400";
        DEFAULT_SEED : std_logic_vector(15 downto 0) := x"ACE1"
    );
    port (
        -- Global Clock and Reset
        clk                   : in  std_logic;
        rst_n                 : in  std_logic;
        
        -- LBIST Controller Handshake (Member 3 Interface)
        lbist_enable          : in  std_logic;
        seed_load             : in  std_logic;
        seed_data             : in  std_logic_vector(WIDTH-1 downto 0);
        target_rate_sel       : in  std_logic_vector(2 downto 0);
        custom_toggle_limit   : in  unsigned(4 downto 0);
        pattern_valid         : out std_logic;
        all_zero_detected     : out std_logic;
        
        -- Scan Chain Interface (Member 1 Interface)
        scan_data_parallel    : out std_logic_vector(WIDTH-1 downto 0);
        scan_data_serial      : out std_logic;
        
        -- Diagnostic & Fault Analysis Outputs (Member 3 Interface)
        raw_pattern_out       : out std_logic_vector(WIDTH-1 downto 0);
        prev_pattern_out      : out std_logic_vector(WIDTH-1 downto 0);
        modification_active   : out std_logic;
        baseline_hamming_dist : out unsigned(4 downto 0);
        instantaneous_toggles : out unsigned(4 downto 0);
        
        -- Cumulative Activity Statistics
        total_word_toggles    : out unsigned(31 downto 0);
        total_patterns_gen    : out unsigned(31 downto 0);
        total_serial_toggles  : out unsigned(31 downto 0);
        total_serial_shifts   : out unsigned(31 downto 0);
        measured_toggle_rate  : out unsigned(7 downto 0)
    );
end entity modified_prpg_top;

architecture rtl of modified_prpg_top is

    -- Internal connections
    signal raw_pattern          : std_logic_vector(WIDTH-1 downto 0);
    signal raw_serial           : std_logic;
    signal raw_prev_reg         : std_logic_vector(WIDTH-1 downto 0);
    signal raw_hd               : unsigned(4 downto 0);
    signal raw_diff_vec         : std_logic_vector(WIDTH-1 downto 0);
    
    signal active_limit         : unsigned(4 downto 0);
    signal serial_toggle_enable : std_logic;
    signal bypass_mode          : std_logic;
    
    signal mod_pattern_int      : std_logic_vector(WIDTH-1 downto 0);
    signal mod_serial_int       : std_logic;
    signal actual_toggles       : unsigned(4 downto 0);
    signal serial_toggled_int   : std_logic;
    signal mod_active_int       : std_logic;

begin

    -- 1. LFSR Pseudorandom Pattern Generator
    u_lfsr : entity work.lfsr_prpg
        generic map (
            WIDTH        => WIDTH,
            POLYNOMIAL   => POLYNOMIAL,
            DEFAULT_SEED => DEFAULT_SEED
        )
        port map (
            clk               => clk,
            rst_n             => rst_n,
            enable            => lbist_enable,
            seed_load         => seed_load,
            seed_data         => seed_data,
            lfsr_out          => raw_pattern,
            serial_out        => raw_serial,
            all_zero_detected => all_zero_detected
        );

    -- 2. Baseline Raw LFSR Hamming Distance Measurement
    process(clk, rst_n)
    begin
        if rst_n = '0' then
            raw_prev_reg <= (others => '0');
        elsif rising_edge(clk) then
            if lbist_enable = '1' then
                raw_prev_reg <= raw_pattern;
            end if;
        end if;
    end process;

    u_baseline_hd : entity work.hamming_distance
        generic map (
            WIDTH => WIDTH
        )
        port map (
            vec_a    => raw_pattern,
            vec_b    => raw_prev_reg,
            diff_vec => raw_diff_vec,
            distance => raw_hd
        );

    -- 3. Programmable Toggle-Rate Controller & Activity Monitor
    u_controller : entity work.toggle_rate_controller
        generic map (
            WIDTH => WIDTH
        )
        port map (
            clk                  => clk,
            rst_n                => rst_n,
            enable               => lbist_enable,
            target_rate_sel      => target_rate_sel,
            custom_toggle_limit  => custom_toggle_limit,
            active_toggle_limit  => active_limit,
            serial_toggle_enable => serial_toggle_enable,
            bypass_mode          => bypass_mode,
            actual_toggles_in    => actual_toggles,
            serial_bit_toggled   => serial_toggled_int,
            total_word_toggles   => total_word_toggles,
            total_patterns_gen   => total_patterns_gen,
            total_serial_toggles => total_serial_toggles,
            total_serial_shifts  => total_serial_shifts,
            measured_toggle_rate => measured_toggle_rate
        );

    -- 4. Rotating Transition Suppression Pattern Modifier
    u_modifier : entity work.pattern_modifier
        generic map (
            WIDTH => WIDTH
        )
        port map (
            clk                  => clk,
            rst_n                => rst_n,
            enable               => lbist_enable,
            raw_pattern          => raw_pattern,
            raw_serial           => raw_serial,
            active_limit         => active_limit,
            serial_toggle_enable => serial_toggle_enable,
            bypass_mode          => bypass_mode,
            mod_pattern          => mod_pattern_int,
            mod_serial           => mod_serial_int,
            prev_pattern_out     => prev_pattern_out,
            toggles_count        => actual_toggles,
            serial_toggled       => serial_toggled_int,
            modification_active  => mod_active_int
        );

    -- Pattern Valid handshake: asserted when PRPG is actively clocking patterns
    pattern_valid <= lbist_enable;

    -- Output Assignments
    scan_data_parallel    <= mod_pattern_int;
    scan_data_serial      <= mod_serial_int;
    raw_pattern_out       <= raw_pattern;
    modification_active   <= mod_active_int;
    baseline_hamming_dist <= raw_hd;
    instantaneous_toggles <= actual_toggles;

end architecture rtl;

