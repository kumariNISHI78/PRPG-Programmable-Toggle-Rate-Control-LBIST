--------------------------------------------------------------------------------
-- Project   : Scan-Based LBIST with Programmable Toggle-Rate Control
-- File      : conventional_prpg.vhd
-- Role      : Member 2 - PRPG and Toggle-Rate Control
-- Design    : Baseline Conventional PRPG with Activity Measurement
-- Standard  : IEEE 1076-2008 (VHDL-2008) / Synthesizable RTL
--------------------------------------------------------------------------------
-- Description:
--   Baseline unconstrained LFSR-based PRPG.
--   Provides reference metrics for comparison against the modified PRPG:
--     - Unconstrained pseudorandom pattern stream.
--     - Consecutive pattern Hamming distance monitoring.
--     - Cumulative transition accumulator and pattern counter.
--     - Reference serial scan-shift bit stream.
--------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity conventional_prpg is
    generic (
        WIDTH        : positive := 16;
        POLYNOMIAL   : std_logic_vector(15 downto 0) := x"B400";
        DEFAULT_SEED : std_logic_vector(15 downto 0) := x"ACE1"
    );
    port (
        clk               : in  std_logic;
        rst_n             : in  std_logic;
        enable            : in  std_logic;
        pattern_out       : out std_logic_vector(WIDTH-1 downto 0);
        serial_out        : out std_logic;
        hamming_dist      : out unsigned(4 downto 0);
        total_toggles     : out unsigned(31 downto 0);
        total_patterns    : out unsigned(31 downto 0);
        all_zero_detected : out std_logic
    );
end entity conventional_prpg;

architecture rtl of conventional_prpg is

    -- Internal PRPG output and previous pattern register
    signal current_pattern : std_logic_vector(WIDTH-1 downto 0);
    signal prev_pattern    : std_logic_vector(WIDTH-1 downto 0);
    signal current_hd      : unsigned(4 downto 0);
    signal diff_vector     : std_logic_vector(WIDTH-1 downto 0);
    
    -- Accumulators for statistical evaluation
    signal toggle_accum    : unsigned(31 downto 0);
    signal pattern_accum   : unsigned(31 downto 0);
    signal first_pattern   : std_logic;

begin

    -- Instantiate the Parameterizable LFSR Core
    u_lfsr : entity work.lfsr_prpg
        generic map (
            WIDTH        => WIDTH,
            POLYNOMIAL   => POLYNOMIAL,
            DEFAULT_SEED => DEFAULT_SEED
        )
        port map (
            clk               => clk,
            rst_n             => rst_n,
            enable            => enable,
            seed_load         => '0',
            seed_data         => (others => '0'),
            lfsr_out          => current_pattern,
            serial_out        => serial_out,
            all_zero_detected => all_zero_detected
        );

    -- Combinational Hamming Distance between consecutive patterns
    u_hd : entity work.hamming_distance
        generic map (
            WIDTH => WIDTH
        )
        port map (
            vec_a    => current_pattern,
            vec_b    => prev_pattern,
            diff_vec => diff_vector,
            distance => current_hd
        );

    -- Pattern Registration and Activity Accumulation
    process(clk, rst_n)
    begin
        if rst_n = '0' then
            prev_pattern  <= (others => '0');
            toggle_accum  <= (others => '0');
            pattern_accum <= (others => '0');
            first_pattern <= '1';
        elsif rising_edge(clk) then
            if enable = '1' then
                prev_pattern  <= current_pattern;
                pattern_accum <= pattern_accum + 1;
                
                -- Skip first pattern transition recording to avoid uninitialized boundary artifact
                if first_pattern = '1' then
                    first_pattern <= '0';
                else
                    toggle_accum <= toggle_accum + resize(current_hd, 32);
                end if;
            end if;
        end if;
    end process;

    -- Output Assignments
    pattern_out    <= current_pattern;
    hamming_dist   <= current_hd;
    total_toggles  <= toggle_accum;
    total_patterns <= pattern_accum;

end architecture rtl;

