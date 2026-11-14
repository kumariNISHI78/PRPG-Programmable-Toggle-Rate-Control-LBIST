--------------------------------------------------------------------------------
-- Project   : Scan-Based LBIST with Programmable Toggle-Rate Control
-- File      : tb_conventional_prpg.vhd
-- Role      : Member 2 - Verification
-- Design    : Testbench for Baseline Conventional LFSR PRPG
-- Standard  : IEEE 1076-2008 (VHDL-2008)
--------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_textio.all;
use std.textio.all;

entity tb_conventional_prpg is
end entity tb_conventional_prpg;

architecture sim of tb_conventional_prpg is

    -- Universal hex conversion helper for 100% VHDL-93/2008 compatibility
    function to_hex_str(slv : std_logic_vector) return string is
        constant hex_chars : string(1 to 16) := "0123456789ABCDEF";
        variable result    : string(1 to slv'length / 4);
        variable nibble    : std_logic_vector(3 downto 0);
        variable val       : integer;
    begin
        for i in 0 to (slv'length / 4) - 1 loop
            nibble := slv(slv'length - 1 - i*4 downto slv'length - 4 - i*4);
            val := 0;
            if nibble(0) = '1' then val := val + 1; end if;
            if nibble(1) = '1' then val := val + 2; end if;
            if nibble(2) = '1' then val := val + 4; end if;
            if nibble(3) = '1' then val := val + 8; end if;
            result(i + 1) := hex_chars(val + 1);
        end loop;
        return result;
    end function;

    constant WIDTH       : positive := 16;
    constant CLK_PERIOD  : time := 10 ns;
    
    signal clk           : std_logic := '0';
    signal rst_n         : std_logic := '0';
    signal enable        : std_logic := '0';
    
    signal pattern_out   : std_logic_vector(WIDTH-1 downto 0);
    signal serial_out    : std_logic;
    signal hamming_dist  : unsigned(4 downto 0);
    signal total_toggles : unsigned(31 downto 0);
    signal total_patterns: unsigned(31 downto 0);
    signal all_zero      : std_logic;
    
    signal sim_done      : boolean := false;

begin

    -- Device Under Test
    dut : entity work.conventional_prpg
        generic map (
            WIDTH        => WIDTH,
            POLYNOMIAL   => x"B400",
            DEFAULT_SEED => x"ACE1"
        )
        port map (
            clk               => clk,
            rst_n             => rst_n,
            enable            => enable,
            pattern_out       => pattern_out,
            serial_out        => serial_out,
            hamming_dist      => hamming_dist,
            total_toggles     => total_toggles,
            total_patterns    => total_patterns,
            all_zero_detected => all_zero
        );

    -- Clock Generation
    clk_proc : process
    begin
        while not sim_done loop
            clk <= '0';
            wait for CLK_PERIOD / 2;
            clk <= '1';
            wait for CLK_PERIOD / 2;
        end loop;
        wait;
    end process;

    -- Stimulus and Reporting Process
    stim_proc : process
        variable l : line;
        variable pct : real;
    begin
        write(l, string'("================================================================"));
        writeline(output, l);
        write(l, string'(" TEST 1: Baseline Conventional LFSR PRPG Simulation"));
        writeline(output, l);
        write(l, string'("================================================================"));
        writeline(output, l);
        
        -- Reset phase
        rst_n  <= '0';
        enable <= '0';
        wait for CLK_PERIOD * 3;
        
        -- Release Reset
        rst_n  <= '1';
        wait for CLK_PERIOD * 2;
        
        -- Enable pattern generation
        enable <= '1';
        
        -- Run for 200 pattern cycles
        for cycle in 1 to 200 loop
            wait until rising_edge(clk);
            if cycle <= 10 then
                write(l, string'("Cycle "));
                write(l, cycle);
                write(l, string'(": Pattern = 0x"));
                -- Write hex representation
                write(l, to_hex_str(pattern_out));
                write(l, string'(", Hamming Distance = "));
                write(l, to_integer(hamming_dist));
                writeline(output, l);
            end if;
        end loop;
        
        -- Wait for settling
        wait until rising_edge(clk);
        enable <= '0';
        wait for CLK_PERIOD * 2;
        
        -- Compute and display metrics
        pct := (real(to_integer(total_toggles)) / real(to_integer(total_patterns) * WIDTH)) * 100.0;
        
        write(l, string'("----------------------------------------------------------------"));
        writeline(output, l);
        write(l, string'(" Baseline PRPG Results:"));
        writeline(output, l);
        write(l, string'(" Total Patterns Generated : "));
        write(l, to_integer(total_patterns));
        writeline(output, l);
        write(l, string'(" Total Bit Toggles        : "));
        write(l, to_integer(total_toggles));
        writeline(output, l);
        write(l, string'(" Baseline Average Toggle Rate: "));
        write(l, pct);
        write(l, string'(" % (Expected ~50.0%)"));
        writeline(output, l);
        write(l, string'("================================================================"));
        writeline(output, l);
        
        sim_done <= true;
        wait;
    end process;

end architecture sim;

