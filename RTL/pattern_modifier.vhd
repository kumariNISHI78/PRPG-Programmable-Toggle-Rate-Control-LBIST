--------------------------------------------------------------------------------
-- Project   : Scan-Based LBIST with Programmable Toggle-Rate Control
-- File      : pattern_modifier.vhd
-- Role      : Member 2 - PRPG and Toggle-Rate Control
-- Design    : Rotating Priority Transition-Suppression Pattern Modifier
-- Standard  : IEEE 1076-2008 (VHDL-2008) / Synthesizable RTL
--------------------------------------------------------------------------------
-- Description:
--   Implements Dual-Domain Rotating Transition Suppression (DDRTS).
--   Features:
--     1. Parallel Vector Domain:
--        Compares incoming raw LFSR pattern against previous modified pattern.
--        If requested bit toggles exceed active_limit, suppresses excess toggles
--        by holding previous bit states.
--     2. Rotating Priority Token Ring:
--        Rotates the bit-inspection starting index across cycles, ensuring uniform
--        spatial toggle distribution across all scan chains and preventing fault
--        coverage starvation in upper bit positions.
--     3. Serial Scan Domain:
--        Suppresses transitions in serial scan-in data when serial_toggle_enable
--        is deasserted, directly scaling scan-chain shift power.
--------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity pattern_modifier is
    generic (
        WIDTH : positive := 16
    );
    port (
        clk                  : in  std_logic;
        rst_n                : in  std_logic;
        enable               : in  std_logic;
        
        -- Inputs from LFSR PRPG
        raw_pattern          : in  std_logic_vector(WIDTH-1 downto 0);
        raw_serial           : in  std_logic;
        
        -- Inputs from Toggle-Rate Controller
        active_limit         : in  unsigned(4 downto 0);
        serial_toggle_enable : in  std_logic;
        bypass_mode          : in  std_logic;
        
        -- Modified outputs to Scan Chain / CUT
        mod_pattern          : out std_logic_vector(WIDTH-1 downto 0);
        mod_serial           : out std_logic;
        prev_pattern_out     : out std_logic_vector(WIDTH-1 downto 0);
        
        -- Activity metrics back to controller and monitor
        toggles_count        : out unsigned(4 downto 0);
        serial_toggled       : out std_logic;
        modification_active  : out std_logic
    );
end entity pattern_modifier;

architecture rtl of pattern_modifier is

    -- Previous registered pattern and serial state
    signal prev_pattern_reg : std_logic_vector(WIDTH-1 downto 0);
    signal prev_serial_reg  : std_logic;
    
    -- Rotating priority pointer to prevent spatial bias across scan chains
    signal rot_pointer      : unsigned(3 downto 0);
    
    -- Internal combinational signals for modified values
    signal comb_mod_pattern : std_logic_vector(WIDTH-1 downto 0);
    signal comb_mod_serial  : std_logic;
    signal comb_toggles     : unsigned(4 downto 0);
    signal comb_serial_tog  : std_logic;
    signal comb_mod_active  : std_logic;

begin

    prev_pattern_out <= prev_pattern_reg;
    mod_pattern      <= comb_mod_pattern;
    mod_serial       <= comb_mod_serial;
    toggles_count    <= comb_toggles;
    serial_toggled   <= comb_serial_tog;
    modification_active <= comb_mod_active;

    -- Combinational Pattern Modification Logic with Rotating Priority
    process(raw_pattern, prev_pattern_reg, active_limit, bypass_mode, 
            rot_pointer, raw_serial, prev_serial_reg, serial_toggle_enable)
        variable raw_diff           : std_logic_vector(WIDTH-1 downto 0);
        variable rotated_diff       : std_logic_vector(WIDTH-1 downto 0);
        variable approved_rotated   : std_logic_vector(WIDTH-1 downto 0);
        variable approved_mask      : std_logic_vector(WIDTH-1 downto 0);
        variable granted_count      : unsigned(4 downto 0);
        variable raw_toggle_count   : unsigned(4 downto 0);
        variable r_idx              : integer;
        variable rot_offset         : integer;
    begin
        -- 1. Bitwise difference: '1' where a transition is requested
        raw_diff := raw_pattern xor prev_pattern_reg;
        
        -- Count raw requested transitions
        raw_toggle_count := (others => '0');
        for i in 0 to WIDTH-1 loop
            if raw_diff(i) = '1' then
                raw_toggle_count := raw_toggle_count + 1;
            end if;
        end loop;

        rot_offset := to_integer(rot_pointer);

        if bypass_mode = '1' then
            -- Bypass mode: pass raw PRPG vectors unaltered (baseline reference)
            comb_mod_pattern <= raw_pattern;
            comb_toggles     <= raw_toggle_count;
            comb_mod_active  <= '0';
            
            comb_mod_serial  <= raw_serial;
            comb_serial_tog  <= raw_serial xor prev_serial_reg;
            
        else
            -- 2. Forward Rotation by rot_offset: shifts priority window
            for j in 0 to WIDTH-1 loop
                r_idx := (j + rot_offset) mod WIDTH;
                rotated_diff(j) := raw_diff(r_idx);
            end loop;

            -- 3. Priority Allocation: grant up to active_limit transitions
            granted_count    := (others => '0');
            approved_rotated := (others => '0');
            
            for j in 0 to WIDTH-1 loop
                if rotated_diff(j) = '1' then
                    if granted_count < active_limit then
                        approved_rotated(j) := '1';
                        granted_count := granted_count + 1;
                    else
                        approved_rotated(j) := '0';
                    end if;
                end if;
            end loop;

            -- 4. Reverse Rotation: map approved transitions back to original bit positions
            for i in 0 to WIDTH-1 loop
                r_idx := (i - rot_offset + WIDTH) mod WIDTH;
                approved_mask(i) := approved_rotated(r_idx);
            end loop;

            -- 5. Construct modified output:
            -- If approved_mask(i) = '1', toggle is permitted (prev xor 1 = not prev = raw)
            -- If approved_mask(i) = '0', toggle is suppressed (prev xor 0 = prev)
            comb_mod_pattern <= prev_pattern_reg xor approved_mask;
            comb_toggles     <= granted_count;
            
            if raw_toggle_count > active_limit then
                comb_mod_active <= '1';
            else
                comb_mod_active <= '0';
            end if;

            -- 6. Serial Scan-In Modification:
            if (raw_serial xor prev_serial_reg) = '1' then
                if serial_toggle_enable = '1' then
                    comb_mod_serial <= raw_serial;      -- Transition permitted
                    comb_serial_tog <= '1';
                else
                    comb_mod_serial <= prev_serial_reg; -- Transition suppressed: hold previous bit
                    comb_serial_tog <= '0';
                end if;
            else
                comb_mod_serial <= raw_serial;          -- Identical bit: no transition anyway
                comb_serial_tog <= '0';
            end if;
        end if;
    end process;

    -- Sequential Process: State Registration & Priority Rotation
    process(clk, rst_n)
    begin
        if rst_n = '0' then
            prev_pattern_reg <= (others => '0');
            prev_serial_reg  <= '0';
            rot_pointer      <= (others => '0');
        elsif rising_edge(clk) then
            if enable = '1' then
                prev_pattern_reg <= comb_mod_pattern;
                prev_serial_reg  <= comb_mod_serial;
                
                -- Increment rotation pointer with prime step (e.g. +3 mod 16)
                -- to ensure rapid cyclic coverage of all bit lanes
                rot_pointer <= rot_pointer + 3;
            end if;
        end if;
    end process;

end architecture rtl;

