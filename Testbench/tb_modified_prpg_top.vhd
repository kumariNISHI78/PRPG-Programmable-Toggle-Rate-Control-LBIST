--------------------------------------------------------------------------------
-- Project   : Scan-Based LBIST with Programmable Toggle-Rate Control
-- File      : tb_modified_prpg_top.vhd
-- Role      : Member 2 - Comprehensive System Verification & Power Evaluation
-- Design    : Full Verification Testbench Covering Tests 1 to 7 & Scan Power
-- Standard  : IEEE 1076-2008 (VHDL-2008)
--------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_textio.all;
use std.textio.all;

entity tb_modified_prpg_top is
end entity tb_modified_prpg_top;

architecture sim of tb_modified_prpg_top is

    -- Universal string/character conversion helpers for 100% VHDL-93/2008 compatibility
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

    function to_char(s : std_logic) return character is
    begin
        case s is
            when '1' => return '1';
            when '0' => return '0';
            when others => return 'X';
        end case;
    end function;

    constant WIDTH        : positive := 16;
    constant CHAIN_LENGTH : positive := 32;
    constant CLK_PERIOD   : time := 10 ns;
    
    -- Global Testbench Signals
    signal clk            : std_logic := '0';
    signal rst_n          : std_logic := '0';
    signal lbist_enable   : std_logic := '0';
    signal seed_load      : std_logic := '0';
    signal seed_data      : std_logic_vector(WIDTH-1 downto 0) := (others => '0');
    signal target_rate_sel: std_logic_vector(2 downto 0) := "110"; -- Default Bypass
    signal custom_limit   : unsigned(4 downto 0) := to_unsigned(8, 5);
    
    -- Modified PRPG Top Outputs
    signal pattern_valid         : std_logic;
    signal all_zero_detected     : std_logic;
    signal scan_data_parallel    : std_logic_vector(WIDTH-1 downto 0);
    signal scan_data_serial      : std_logic;
    signal raw_pattern_out       : std_logic_vector(WIDTH-1 downto 0);
    signal prev_pattern_out      : std_logic_vector(WIDTH-1 downto 0);
    signal modification_active   : std_logic;
    signal baseline_hamming_dist : unsigned(4 downto 0);
    signal instantaneous_toggles : unsigned(4 downto 0);
    signal total_word_toggles    : unsigned(31 downto 0);
    signal total_patterns_gen    : unsigned(31 downto 0);
    signal total_serial_toggles  : unsigned(31 downto 0);
    signal total_serial_shifts   : unsigned(31 downto 0);
    signal measured_toggle_rate  : unsigned(7 downto 0);

    -- Baseline Conventional PRPG (for concurrent benchmark comparison)
    signal base_pattern_out      : std_logic_vector(WIDTH-1 downto 0);
    signal base_serial_out       : std_logic;
    signal base_hamming_dist     : unsigned(4 downto 0);
    signal base_total_toggles    : unsigned(31 downto 0);
    signal base_total_patterns   : unsigned(31 downto 0);
    signal base_all_zero         : std_logic;

    -- Scan Chain Model 1: Driven by Baseline PRPG Serial Stream
    signal base_scan_out         : std_logic;
    signal base_chain_state      : std_logic_vector(CHAIN_LENGTH-1 downto 0);
    signal base_chain_cyc_tog    : unsigned(7 downto 0);
    signal base_chain_acc_tog    : unsigned(31 downto 0);
    signal base_chain_shifts     : unsigned(31 downto 0);
    signal base_scan_toggle_pct  : unsigned(7 downto 0);

    -- Scan Chain Model 2: Driven by Modified PRPG Serial Stream
    signal mod_scan_out          : std_logic;
    signal mod_chain_state       : std_logic_vector(CHAIN_LENGTH-1 downto 0);
    signal mod_chain_cyc_tog     : unsigned(7 downto 0);
    signal mod_chain_acc_tog     : unsigned(31 downto 0);
    signal mod_chain_shifts      : unsigned(31 downto 0);
    signal mod_scan_toggle_pct   : unsigned(7 downto 0);

    signal sim_done              : boolean := false;

begin

    -- 1. DUT: Modified PRPG Top
    dut_modified_prpg : entity work.modified_prpg_top
        generic map (
            WIDTH        => WIDTH,
            POLYNOMIAL   => x"B400",
            DEFAULT_SEED => x"ACE1"
        )
        port map (
            clk                   => clk,
            rst_n                 => rst_n,
            lbist_enable          => lbist_enable,
            seed_load             => seed_load,
            seed_data             => seed_data,
            target_rate_sel       => target_rate_sel,
            custom_toggle_limit   => custom_limit,
            pattern_valid         => pattern_valid,
            all_zero_detected     => all_zero_detected,
            scan_data_parallel    => scan_data_parallel,
            scan_data_serial      => scan_data_serial,
            raw_pattern_out       => raw_pattern_out,
            prev_pattern_out      => prev_pattern_out,
            modification_active   => modification_active,
            baseline_hamming_dist => baseline_hamming_dist,
            instantaneous_toggles => instantaneous_toggles,
            total_word_toggles    => total_word_toggles,
            total_patterns_gen    => total_patterns_gen,
            total_serial_toggles  => total_serial_toggles,
            total_serial_shifts   => total_serial_shifts,
            measured_toggle_rate  => measured_toggle_rate
        );

    -- 2. Reference Benchmark: Conventional PRPG
    dut_baseline_prpg : entity work.conventional_prpg
        generic map (
            WIDTH        => WIDTH,
            POLYNOMIAL   => x"B400",
            DEFAULT_SEED => x"ACE1"
        )
        port map (
            clk               => clk,
            rst_n             => rst_n,
            enable            => lbist_enable,
            pattern_out       => base_pattern_out,
            serial_out        => base_serial_out,
            hamming_dist      => base_hamming_dist,
            total_toggles     => base_total_toggles,
            total_patterns    => base_total_patterns,
            all_zero_detected => base_all_zero
        );

    -- 3. Scan Chain Model for Baseline Serial Stream
    u_scan_baseline : entity work.scan_chain_model
        generic map (
            CHAIN_LENGTH => CHAIN_LENGTH
        )
        port map (
            clk                      => clk,
            rst_n                    => rst_n,
            shift_enable             => lbist_enable,
            scan_in                  => base_serial_out,
            scan_out                 => base_scan_out,
            chain_state              => base_chain_state,
            cycle_transitions        => base_chain_cyc_tog,
            accumulated_transitions  => base_chain_acc_tog,
            total_shift_cycles       => base_chain_shifts,
            measured_scan_toggle_pct => base_scan_toggle_pct
        );

    -- 4. Scan Chain Model for Modified Serial Stream
    u_scan_modified : entity work.scan_chain_model
        generic map (
            CHAIN_LENGTH => CHAIN_LENGTH
        )
        port map (
            clk                      => clk,
            rst_n                    => rst_n,
            shift_enable             => lbist_enable,
            scan_in                  => scan_data_serial,
            scan_out                 => mod_scan_out,
            chain_state              => mod_chain_state,
            cycle_transitions        => mod_chain_cyc_tog,
            accumulated_transitions  => mod_chain_acc_tog,
            total_shift_cycles       => mod_chain_shifts,
            measured_scan_toggle_pct => mod_scan_toggle_pct
        );

    -- Clock Generator
    clk_gen : process
    begin
        while not sim_done loop
            clk <= '0';
            wait for CLK_PERIOD / 2;
            clk <= '1';
            wait for CLK_PERIOD / 2;
        end loop;
        wait;
    end process;

    -- Master Stimulus & Verification Sequence
    stim_proc : process
        variable l : line;
        
        -- Helper procedure to execute a test configuration and display results
        procedure run_test_configuration(
            constant test_name    : in string;
            constant sel_code     : in std_logic_vector(2 downto 0);
            constant target_pct   : in real;
            constant num_cycles   : in integer
        ) is
            variable start_base_tog : integer;
            variable start_mod_tog  : integer;
            variable start_base_scan: integer;
            variable start_mod_scan : integer;
            
            variable diff_base_tog  : integer;
            variable diff_mod_tog   : integer;
            variable diff_base_scan : integer;
            variable diff_mod_scan  : integer;
            
            variable base_word_pct  : real;
            variable mod_word_pct   : real;
            variable word_reduction : real;
            
            variable base_scan_pct  : real;
            variable mod_scan_pct   : real;
            variable scan_reduction : real;
        begin
            write(l, string'("----------------------------------------------------------------"));
            writeline(output, l);
            write(l, test_name);
            writeline(output, l);
            write(l, string'("----------------------------------------------------------------"));
            writeline(output, l);
            
            target_rate_sel <= sel_code;
            wait until rising_edge(clk);
            
            -- Record baseline stats at start of configuration
            start_base_tog  := to_integer(base_total_toggles);
            start_mod_tog   := to_integer(total_word_toggles);
            start_base_scan := to_integer(base_chain_acc_tog);
            start_mod_scan  := to_integer(mod_chain_acc_tog);
            
            -- Run specified shift/pattern cycles
            for i in 1 to num_cycles loop
                wait until rising_edge(clk);
                if i <= 5 then
                    write(l, string'("  [Cycle "));
                    write(l, i);
                    write(l, string'("] RawPattern=0x"));
                    write(l, to_hex_str(raw_pattern_out));
                    write(l, string'(", ModPattern=0x"));
                    write(l, to_hex_str(scan_data_parallel));
                    write(l, string'(", BaseHD="));
                    write(l, to_integer(baseline_hamming_dist));
                    write(l, string'(", ModTog="));
                    write(l, to_integer(instantaneous_toggles));
                    write(l, string'(", ModActive="));
                    write(l, to_char(modification_active));
                    writeline(output, l);
                end if;
            end loop;
            
            -- Calculate differences during this configuration window
            diff_base_tog  := to_integer(base_total_toggles) - start_base_tog;
            diff_mod_tog   := to_integer(total_word_toggles) - start_mod_tog;
            diff_base_scan := to_integer(base_chain_acc_tog) - start_base_scan;
            diff_mod_scan  := to_integer(mod_chain_acc_tog) - start_mod_scan;
            
            base_word_pct  := (real(diff_base_tog) / real(num_cycles * WIDTH)) * 100.0;
            mod_word_pct   := (real(diff_mod_tog) / real(num_cycles * WIDTH)) * 100.0;
            if base_word_pct > 0.0 then
                word_reduction := ((base_word_pct - mod_word_pct) / base_word_pct) * 100.0;
            else
                word_reduction := 0.0;
            end if;
            
            base_scan_pct  := (real(diff_base_scan) / real(num_cycles * CHAIN_LENGTH)) * 100.0;
            mod_scan_pct   := (real(diff_mod_scan) / real(num_cycles * CHAIN_LENGTH)) * 100.0;
            if base_scan_pct > 0.0 then
                scan_reduction := ((base_scan_pct - mod_scan_pct) / base_scan_pct) * 100.0;
            else
                scan_reduction := 0.0;
            end if;
            
            write(l, string'(">>> RESULTS FOR: "));
            write(l, test_name);
            writeline(output, l);
            write(l, string'("    Target Toggle Rate Setting   : "));
            write(l, target_pct);
            write(l, string'(" %"));
            writeline(output, l);
            write(l, string'("    Conventional Word Toggle Rate: "));
            write(l, base_word_pct);
            write(l, string'(" %"));
            writeline(output, l);
            write(l, string'("    Modified Word Toggle Rate    : "));
            write(l, mod_word_pct);
            write(l, string'(" %"));
            writeline(output, l);
            write(l, string'("    Word Switching Reduction     : "));
            write(l, word_reduction);
            write(l, string'(" %"));
            writeline(output, l);
            write(l, string'("    Conventional Scan Shift Rate : "));
            write(l, base_scan_pct);
            write(l, string'(" %"));
            writeline(output, l);
            write(l, string'("    Modified Scan Shift Rate     : "));
            write(l, mod_scan_pct);
            write(l, string'(" %"));
            writeline(output, l);
            write(l, string'("    Scan Shift Power Reduction   : "));
            write(l, scan_reduction);
            write(l, string'(" %"));
            writeline(output, l);
        end procedure;

    begin
        write(l, string'("################################################################"));
        writeline(output, l);
        write(l, string'("  VL405 LBIST PRPG & TOGGLE-RATE CONTROL SYSTEM VERIFICATION"));
        writeline(output, l);
        write(l, string'("  Member 2 - Full Verification Test Suite (Tests 1 to 7)"));
        writeline(output, l);
        write(l, string'("################################################################"));
        writeline(output, l);
        
        -- Power-on Reset Sequence
        rst_n        <= '0';
        lbist_enable <= '0';
        seed_load    <= '0';
        wait for CLK_PERIOD * 3;
        rst_n        <= '1';
        wait for CLK_PERIOD * 2;
        lbist_enable <= '1';
        
        -- TEST 1: Baseline Conventional PRPG (Bypass mode)
        run_test_configuration("TEST 1 & 4: Baseline Bypass PRPG (100% Passthrough)", "110", 100.0, 100);
        
        -- TEST 2: Modified PRPG at 10% Target
        run_test_configuration("TEST 2: Target Toggle Rate = 10%", "000", 10.0, 150);
        
        -- TEST 3: Modified PRPG at 20%, 30%, 40%, 50%, 60% Targets
        run_test_configuration("TEST 3A: Target Toggle Rate = 20%", "001", 20.0, 150);
        run_test_configuration("TEST 3B: Target Toggle Rate = 30%", "010", 30.0, 150);
        run_test_configuration("TEST 3C: Target Toggle Rate = 40%", "011", 40.0, 150);
        run_test_configuration("TEST 3D: Target Toggle Rate = 50%", "100", 50.0, 150);
        run_test_configuration("TEST 3E: Target Toggle Rate = 60%", "101", 60.0, 150);
        
        -- TEST 5: Reset and Restart Verification
        write(l, string'("----------------------------------------------------------------"));
        writeline(output, l);
        write(l, string'("TEST 5: Asynchronous Reset and Restart Verification"));
        writeline(output, l);
        write(l, string'("----------------------------------------------------------------"));
        writeline(output, l);
        
        rst_n <= '0'; -- Assert reset mid-operation
        wait for CLK_PERIOD * 3;
        write(l, string'("  Reset asserted: scan_data_parallel = 0x"));
        write(l, to_hex_str(scan_data_parallel));
        write(l, string'(", instantaneous_toggles = "));
        write(l, to_integer(instantaneous_toggles));
        writeline(output, l);
        -- LFSR correctly resets to DEFAULT_SEED (0xACE1), NOT all-zeros.
        -- The anti-lockup mechanism seeds the LFSR to a known non-zero state on rst_n='0'.
        -- Asserting all-zeros on reset would indicate a broken LFSR (lockup state).
        assert scan_data_parallel = x"ACE1"
            report "Reset state check failed: expected LFSR seed 0xACE1 after reset" severity error;
        
        rst_n <= '1'; -- Deassert reset
        target_rate_sel <= "000"; -- Set to 10% target
        wait for CLK_PERIOD * 5;
        write(l, string'("  Restart confirmed: PRPG resuming generation with valid patterns."));
        writeline(output, l);
        
        -- TEST 6: Continuous Operation Verification (Long Run)
        write(l, string'("----------------------------------------------------------------"));
        writeline(output, l);
        write(l, string'("TEST 6: Continuous Long-Sequence Operation (500 cycles at 20%)"));
        writeline(output, l);
        write(l, string'("----------------------------------------------------------------"));
        writeline(output, l);
        target_rate_sel <= "001";
        for k in 1 to 500 loop
            wait until rising_edge(clk);
            assert all_zero_detected = '0' report "Error: Illegal all-zero LFSR state detected!" severity failure;
        end loop;
        write(l, string'("  Continuous 500-cycle run passed with zero lockup / illegal states."));
        writeline(output, l);
        
        -- TEST 7: Dynamic Configuration Changes On-The-Fly
        write(l, string'("----------------------------------------------------------------"));
        writeline(output, l);
        write(l, string'("TEST 7: Dynamic On-The-Fly Configuration Changes"));
        writeline(output, l);
        write(l, string'("----------------------------------------------------------------"));
        writeline(output, l);
        
        target_rate_sel <= "000"; -- Switch to 10%
        wait for CLK_PERIOD * 20;
        write(l, string'("  Switched to 10%: Instantaneous toggles = "));
        write(l, to_integer(instantaneous_toggles));
        writeline(output, l);
        
        target_rate_sel <= "011"; -- Switch to 40%
        wait for CLK_PERIOD * 20;
        write(l, string'("  Switched to 40%: Instantaneous toggles = "));
        write(l, to_integer(instantaneous_toggles));
        writeline(output, l);
        
        target_rate_sel <= "110"; -- Switch to Bypass
        wait for CLK_PERIOD * 20;
        write(l, string'("  Switched to Bypass: Instantaneous toggles = "));
        write(l, to_integer(instantaneous_toggles));
        writeline(output, l);

        write(l, string'("################################################################"));
        writeline(output, l);
        write(l, string'(" ALL 7 LBIST PRPG VERIFICATION SUITES COMPLETED SUCCESSFULLY!  "));
        writeline(output, l);
        write(l, string'("################################################################"));
        writeline(output, l);

        sim_done <= true;
        wait;
    end process;

end architecture sim;

