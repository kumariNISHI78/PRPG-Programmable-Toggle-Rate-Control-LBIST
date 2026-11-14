--------------------------------------------------------------------------------
-- Project   : Scan-Based LBIST with Programmable Toggle-Rate Control
-- File      : hamming_distance.vhd
-- Role      : Member 2 - PRPG and Toggle-Rate Control
-- Design    : Combinational Hamming Distance / Popcount Calculator
-- Standard  : IEEE 1076-2008 (VHDL-2008) / Synthesizable RTL
--------------------------------------------------------------------------------
-- Description:
--   Computes the bitwise Hamming distance between two binary vectors:
--     HD(A, B) = Sum_{i=0}^{WIDTH-1} (A(i) XOR B(i))
--   This represents the instantaneous switching activity (number of bit toggles)
--   between consecutive test patterns.
--------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity hamming_distance is
    generic (
        WIDTH : positive := 16
    );
    port (
        vec_a    : in  std_logic_vector(WIDTH-1 downto 0);
        vec_b    : in  std_logic_vector(WIDTH-1 downto 0);
        diff_vec : out std_logic_vector(WIDTH-1 downto 0);
        distance : out unsigned(4 downto 0) -- Supports widths up to 31 (0 to 16 for WIDTH=16)
    );
end entity hamming_distance;

architecture rtl of hamming_distance is
    signal xor_diff : std_logic_vector(WIDTH-1 downto 0);
begin

    -- Bitwise difference vector: '1' indicates a transition in that bit position
    xor_diff <= vec_a xor vec_b;
    diff_vec <= xor_diff;

    -- Combinational population count of active bit transitions
    process(xor_diff)
        variable count : unsigned(4 downto 0);
    begin
        count := (others => '0');
        for i in 0 to WIDTH-1 loop
            if xor_diff(i) = '1' then
                count := count + 1;
            end if;
        end loop;
        distance <= count;
    end process;

end architecture rtl;

