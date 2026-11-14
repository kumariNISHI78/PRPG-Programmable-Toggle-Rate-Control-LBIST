--------------------------------------------------------------------------------
-- Project   : Scan-Based LBIST with Programmable Toggle-Rate Control
-- File      : scan_chain_model.vhd
-- Role      : Member 2 - Verification & Power Evaluation
-- Design    : Parameterizable Scan Chain Hardware Shift & Switching Activity Model
-- Standard  : IEEE 1076-2008 (VHDL-2008) / Synthesizable RTL
--------------------------------------------------------------------------------
-- Description:
--   Accurately models physical scan-chain shifting dynamics:
--     1. Shifts serial scan-in data into an L-cell sequential scan chain.
--     2. Records chain state before shift: C(t-1).
--     3. Updates chain state after shift: C(t).
--     4. Calculates exact cell-by-cell flip-flop transitions: Sum (C_j(t) xor C_j(t-1)).
--     5. Accumulates total cell transitions over the entire scan shift sequence.
--     6. Computes actual Scan-Shift Toggle Rate:
--        Scan Toggle Rate (%) = (Total Cell Transitions / (Total Shift Cycles * L)) * 100
--------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity scan_chain_model is
    generic (
        CHAIN_LENGTH : positive := 32 -- Number of sequential scan flip-flops
    );
    port (
        clk                     : in  std_logic;
        rst_n                   : in  std_logic;
        shift_enable            : in  std_logic;
        scan_in                 : in  std_logic;
        
        -- Chain state outputs
        scan_out                : out std_logic;
        chain_state             : out std_logic_vector(CHAIN_LENGTH-1 downto 0);
        
        -- Activity metrics
        cycle_transitions       : out unsigned(7 downto 0);
        accumulated_transitions : out unsigned(31 downto 0);
        total_shift_cycles      : out unsigned(31 downto 0);
        measured_scan_toggle_pct: out unsigned(7 downto 0)
    );
end entity scan_chain_model;

architecture rtl of scan_chain_model is

    -- Scan cell flip-flops
    signal cells_reg         : std_logic_vector(CHAIN_LENGTH-1 downto 0);
    signal cells_prev        : std_logic_vector(CHAIN_LENGTH-1 downto 0);
    
    -- Transition counters
    signal trans_accum       : unsigned(31 downto 0);
    signal cycles_accum      : unsigned(31 downto 0);
    signal current_cycle_tog : unsigned(7 downto 0);

begin

    chain_state <= cells_reg;
    scan_out    <= cells_reg(CHAIN_LENGTH-1);
    
    cycle_transitions        <= current_cycle_tog;
    accumulated_transitions  <= trans_accum;
    total_shift_cycles       <= cycles_accum;

    -- Scan Chain Shifting Process
    process(clk, rst_n)
        variable next_cells : std_logic_vector(CHAIN_LENGTH-1 downto 0);
        variable tog_count  : unsigned(7 downto 0);
    begin
        if rst_n = '0' then
            cells_reg         <= (others => '0');
            cells_prev        <= (others => '0');
            trans_accum       <= (others => '0');
            cycles_accum      <= (others => '0');
            current_cycle_tog <= (others => '0');
        elsif rising_edge(clk) then
            if shift_enable = '1' then
                -- 1. Compute next state after shifting in scan_in bit at position 0
                next_cells := cells_reg(CHAIN_LENGTH-2 downto 0) & scan_in;
                
                -- 2. Count exact number of flip-flops that changed state
                tog_count := (others => '0');
                for j in 0 to CHAIN_LENGTH-1 loop
                    if (next_cells(j) xor cells_reg(j)) = '1' then
                        tog_count := tog_count + 1;
                    end if;
                end loop;
                
                -- 3. Register state and update accumulators
                cells_prev        <= cells_reg;
                cells_reg         <= next_cells;
                current_cycle_tog <= tog_count;
                
                trans_accum  <= trans_accum + resize(tog_count, 32);
                cycles_accum <= cycles_accum + 1;
            end if;
        end if;
    end process;

    -- Cumulative Scan Toggle Percentage
    process(trans_accum, cycles_accum)
        variable total_possible : unsigned(63 downto 0);
        variable pct_val        : unsigned(63 downto 0);
    begin
        total_possible := cycles_accum * to_unsigned(CHAIN_LENGTH, 32);
        if total_possible > 0 then
            pct_val := (trans_accum * to_unsigned(100, 32)) / total_possible;
            measured_scan_toggle_pct <= resize(pct_val(7 downto 0), 8);
        else
            measured_scan_toggle_pct <= (others => '0');
        end if;
    end process;

end architecture rtl;

