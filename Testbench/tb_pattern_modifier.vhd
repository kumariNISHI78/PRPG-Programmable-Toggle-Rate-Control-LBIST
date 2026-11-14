--------------------------------------------------------------------------------
-- Project   : Scan-Based LBIST with Programmable Toggle-Rate Control
-- File      : tb_pattern_modifier.vhd
-- Role      : Member 2 - Verification
-- Design    : Unit Testbench for Pattern Modifier & Rotating Priority
-- Standard  : IEEE 1076-2008 (VHDL-2008)
--------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_textio.all;
use std.textio.all;

entity tb_pattern_modifier is
end entity tb_pattern_modifier;

architecture sim of tb_pattern_modifier is

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

    constant WIDTH       : positive := 16;
    constant CLK_PERIOD  : time := 10 ns;
    
    signal clk           : std_logic := '0';
    signal rst_n         : std_logic := '0';
    signal enable        : std_logic := '0';
    
    signal raw_pattern   : std_logic_vector(WIDTH-1 downto 0) := (others => '0');
    signal raw_serial    : std_logic := '0';
    signal active_limit  : unsigned(4 downto 0) := to_unsigned(2, 5);
    signal serial_toggle_enable : std_logic := '1';
    signal bypass_mode   : std_logic := '0';
    
    signal mod_pattern   : std_logic_vector(WIDTH-1 downto 0);
    signal mod_serial    : std_logic;
    signal prev_pattern  : std_logic_vector(WIDTH-1 downto 0);
    signal toggles_count : unsigned(4 downto 0);
    signal serial_toggled: std_logic;
    signal mod_active    : std_logic;
    
    signal sim_done      : boolean := false;

begin

    dut : entity work.pattern_modifier
        generic map (
            WIDTH => WIDTH
        )
        port map (
            clk                  => clk,
            rst_n                => rst_n,
            enable               => enable,
            raw_pattern          => raw_pattern,
            raw_serial           => raw_serial,
            active_limit         => active_limit,
            serial_toggle_enable => serial_toggle_enable,
            bypass_mode          => bypass_mode,
            mod_pattern          => mod_pattern,
            mod_serial           => mod_serial,
            prev_pattern_out     => prev_pattern,
            toggles_count        => toggles_count,
            serial_toggled       => serial_toggled,
            modification_active  => mod_active
        );

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

    stim_proc : process
        variable l : line;
    begin
        write(l, string'("================================================================"));
        writeline(output, l);
        write(l, string'(" Unit Test: Pattern Modifier with Rotating Priority"));
        writeline(output, l);
        write(l, string'("================================================================"));
        writeline(output, l);
        
        rst_n  <= '0';
        enable <= '0';
        wait for CLK_PERIOD * 2;
        rst_n  <= '1';
        wait for CLK_PERIOD;
        enable <= '1';
        
        -- Case 1: Limit = 2 toggles. Feed all-ones pattern (16 toggles requested)
        active_limit <= to_unsigned(2, 5);
        raw_pattern  <= x"FFFF";
        raw_serial   <= '1';
        wait until rising_edge(clk);
        
        write(l, string'("Step 1 (Limit=2, Input=0xFFFF): Mod Pattern = 0x"));
        write(l, to_hex_str(mod_pattern));
        write(l, string'(", Granted Toggles = "));
        write(l, to_integer(toggles_count));
        write(l, string'(", Suppression Active = "));
        write(l, to_char(mod_active));
        writeline(output, l);
        assert toggles_count = 2 report "Error: Toggles count must equal active limit 2" severity error;
        
        -- Case 2: Consecutive cycle with same all-ones raw input. Rotating priority should grant NEXT 2 bits!
        wait until rising_edge(clk);
        write(l, string'("Step 2 (Limit=2, Input=0xFFFF, Rotated): Mod Pattern = 0x"));
        write(l, to_hex_str(mod_pattern));
        write(l, string'(", Granted Toggles = "));
        write(l, to_integer(toggles_count));
        writeline(output, l);
        
        -- Case 3: Limit = 4 toggles. Feed alternating pattern
        active_limit <= to_unsigned(4, 5);
        raw_pattern  <= x"5555";
        wait until rising_edge(clk);
        write(l, string'("Step 3 (Limit=4, Input=0x5555): Mod Pattern = 0x"));
        write(l, to_hex_str(mod_pattern));
        write(l, string'(", Granted Toggles = "));
        write(l, to_integer(toggles_count));
        writeline(output, l);
        assert toggles_count <= 4 report "Error: Toggles count exceeded limit 4" severity error;
        
        -- Case 4: Bypass mode test
        bypass_mode <= '1';
        raw_pattern <= x"AAAA";
        wait until rising_edge(clk);
        write(l, string'("Step 4 (Bypass Mode): Mod Pattern = 0x"));
        write(l, to_hex_str(mod_pattern));
        write(l, string'(", Granted Toggles = "));
        write(l, to_integer(toggles_count));
        write(l, string'(", Mod Active = "));
        write(l, to_char(mod_active));
        writeline(output, l);
        assert mod_pattern = x"AAAA" report "Error: Bypass mode failed" severity error;
        
        write(l, string'("Pattern Modifier Unit Test Completed Successfully."));
        writeline(output, l);
        write(l, string'("================================================================"));
        writeline(output, l);
        
        sim_done <= true;
        wait;
    end process;

end architecture sim;

