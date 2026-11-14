# Comprehensive Design Explanation: LFSR PRPG & Programmable Toggle-Rate Control

**Course**: VL405 – Design for Testability  
**Project**: Design and Implementation of Scan-Based Logic Built-In Self-Test (LBIST) with Programmable Scan-Shift Power Control Using MIPS32 Architecture  
**Role**: Member 2 – PRPG and Toggle-Rate Control  

---

## 1. Linear Feedback Shift Register (LFSR) Fundamentals

A Linear Feedback Shift Register (LFSR) is a sequential shift register whose input bit is a linear function (specifically, XOR or XNOR) of its previous state. In Design for Testability (DFT), LFSRs serve as the primary hardware primitive for **Pseudorandom Pattern Generators (PRPGs)** and **Multiple-Input Signature Registers (MISRs)**.

### 1.1 Mathematical Formulation & Polynomial Theory
The operation of an $n$-bit LFSR is formally characterized by a characteristic polynomial $P(x)$ defined over the Galois Field of two elements, $GF(2)$:

$$P(x) = c_n x^n + c_{n-1} x^{n-1} + \dots + c_1 x + c_0$$

where each coefficient $c_i \in \{0, 1\}$. By definition of an $n$-stage LFSR:
- $c_n = 1$ (represents the input/feedback tap at stage $n$)
- $c_0 = 1$ (represents the feedback closure)
- The intermediate coefficients $c_i = 1$ correspond to physical feedback taps where the state is sampled and combined via modulo-2 addition (XOR).

### 1.2 Maximal-Length Sequences (m-sequences)
An $n$-bit LFSR has $2^n$ possible binary states. When constructed using XOR feedback gates, the all-zero state ($00\dots0$) is an **absorbing / dead state** because $0 \oplus 0 = 0$; if entered, the register would remain trapped in all zeros indefinitely. Therefore, the maximum attainable period of an $n$-bit autonomous XOR-based LFSR is:

$$T_{\text{max}} = 2^n - 1$$

An LFSR achieves this maximal length if and only if its characteristic polynomial $P(x)$ is **primitive** over $GF(2)$. A polynomial is primitive if:
1. It is **irreducible** (cannot be factored into polynomials of lower degree over $GF(2)$).
2. It divides $x^m - 1$ for $m = 2^n - 1$, but does not divide $x^k - 1$ for any $k < m$.

#### Why Maximal-Length Sequences are Critical in LBIST:
- **Pseudo-Exhaustive Coverage**: Over its full cycle of $2^n - 1$ states, every possible non-zero binary vector appears exactly once.
- **Ideal Pseudorandom Distribution (Golomb's Randomness Postulates)**:
  1. *Balance Property*: In every full period, the count of 1s exceeds the count of 0s by exactly 1 (there are $2^{n-1}$ ones and $2^{n-1} - 1$ zeros).
  2. *Run-Length Property*: Exactly half the runs of consecutive identical bits have length 1, one-quarter have length 2, one-eighth have length 3, etc.
  3. *Ideal Autocorrelation*: The circular autocorrelation function $R(\tau)$ is two-valued:
     $$R(\tau) = \begin{cases} 1, & \tau = 0 \pmod{2^n - 1} \\ -\frac{1}{2^n - 1}, & \tau \ne 0 \pmod{2^n - 1} \end{cases}$$
- **Fault Detection Probability**: Ensures unbiased excitation across combinatorial cones in the Circuit Under Test (CUT), maximizing detection probability for stuck-at, transition, and bridging faults.

### 1.3 Topology Selection: Galois vs. Fibonacci LFSR
In VLSI implementation, two distinct LFSR architectures exist:

| Feature | Fibonacci (Standard) LFSR | Galois (Modular) LFSR (Selected) |
| :--- | :--- | :--- |
| **Feedback Mechanism** | External feedback tree: Multiple taps are XORed together and fed back into the serial input stage $D_0$. | Internal distributed feedback: The output bit is XORed into intermediate stages in parallel. |
| **Critical Path Delay** | Long critical path: $t_{\text{crit}} = t_{\text{cq}} + \lceil \log_2(k) \rceil \cdot t_{\text{xor}} + t_{\text{setup}}$, where $k$ is the number of active taps. Multi-input XOR trees degrade $f_{\text{max}}$. | Minimal critical path: At most **one 2-input XOR gate** between adjacent flip-flops: $t_{\text{crit}} = t_{\text{cq}} + t_{\text{xor}} + t_{\text{setup}}$, independent of LFSR width! |
| **Maximum Operating Frequency** | Moderate (scales poorly with register width $n \ge 32$). | High ($> 450 \text{ MHz}$ on modern FPGA/ASIC processes). |
| **Hardware Mapping** | Asymmetric routing congestion around input stage. | Highly regular, localized register-to-register interconnect. |

**Selected Architecture**: Our design implements a **16-bit Galois LFSR** using the standard primitive polynomial:

$$P(x) = x^{16} + x^{14} + x^{13} + x^{11} + 1$$

- Feedback Tap Vector: `0xB400` (binary `1011_0100_0000_0000`, corresponding to taps at stages 16, 14, 13, and 11).
- Non-Zero Default Seed: `0xACE1`.
- Cycle Period: $2^{16} - 1 = 65,535$ distinct pseudorandom patterns.

### 1.4 Autonomous Anti-Lockup Zero-State Recovery
If a power-on glitch, electrostatic discharge (ESD), or Single Event Upset (SEU) flips all LFSR flip-flops to zero, an unassisted XOR LFSR freezes permanently.
Our VHDL implementation in [`lfsr_prpg.vhd`](file:///C:/Users/Nishi%20Kumari/.gemini/antigravity/scratch/Member_2_PRPG_Toggle_Control/RTL/lfsr_prpg.vhd) includes an autonomous combinational NOR-based zero-state detector:

$$\text{is\_all\_zero} = \begin{cases} 1, & \text{if } Q[15:0] = 16'h0000 \\ 0, & \text{otherwise} \end{cases}$$

When `is_all_zero = '1'`, the LFSR state transition process automatically overrides the invalid state and forces an instantaneous recovery reload of `DEFAULT_SEED` (`0xACE1`) on the next active clock edge, guaranteeing continuous, uninterrupted operation.

---

## 2. The Scan-Shift Power Crisis & Transition Theory

### 2.1 Distinction Between Word Hamming Distance and Scan Shift Activity
A fundamental contribution of this work is establishing the rigorous distinction between parallel word switching and scan-chain shifting dynamics:

1. **Word-Level Hamming Distance ($HD$)**:
   $$\text{HD}(P(t), P(t-1)) = \sum_{i=0}^{W-1} \left(P_i(t) \oplus P_i(t-1)\right)$$
   Measures parallel transitions across broadside primary inputs or between successive parallel test words. For unconstrained 16-bit LFSR patterns, the expected value is:
   $$E[\text{HD}] = 16 \times 0.50 = 8.0 \text{ transitions/pattern (50.0\% toggle rate)}$$

2. **Scan-Chain Shift Switching Activity ($SCA$)**:
   In a scan chain with $L$ sequential flip-flops, the test pattern is loaded serially over $L$ shift clock cycles. At shift cycle $k$, bit $S_{\text{in}}(k)$ enters cell 0, while the existing contents ripple through cells $1, 2, \dots, L-1$.
   The state of cell $j$ at shift cycle $k$ is $C_j(k) = S_{\text{in}}(k - j)$.
   Therefore, cell $j$ switches at cycle $k$ if:
   $$C_j(k) \oplus C_j(k-1) = S_{\text{in}}(k - j) \oplus S_{\text{in}}(k - j - 1) = 1$$
   This proves that a single transition in the serial scan input stream causes switching in **all $L$ scan cells** as it travels down the chain!
   
   If the serial transition probability is $p_t = P(S_{\text{in}}(k) \ne S_{\text{in}}(k-1))$, the total expected transitions in the scan chain over $L$ shift cycles is:
   $$E[\text{Total Scan Transitions}] \approx p_t \cdot L^2$$
   By reducing $p_t$ from $0.50$ down to $0.07$ (a $10\%$ target rate), the total switching dissipation across the scan chain decreases quadratically relative to unconstrained testing!

---

## 3. The Proposed Dual-Domain Rotating Transition Suppression (DDRTS) Technique

### 3.1 Motivation & Starvation Problem in Conventional Suppression
If transitions are suppressed using a fixed priority encoder (e.g. always checking bits from index 0 upward and suppressing once the limit is reached), lower-order bit positions ($0, 1, 2$) will consume all available transition quotas. Higher-order bit positions ($10 \dots 15$) will almost never toggle. In an LBIST environment, this results in "cold" scan chains that are starved of test stimuli, causing catastrophic fault coverage degradation!

### 3.2 DDRTS Algorithm Architecture
To solve this, our design introduces a **Rotating Priority Token Ring**:

1. **Raw Transition Extraction**:
   $$\text{raw\_diff} = P_{\text{raw}}(t) \oplus P_{\text{prev}}(t-1)$$
2. **Dynamic Priority Rotation**:
   A modulo-$W$ rotation pointer `rot_pointer` increments each clock cycle:
   $$\text{rot\_pointer} \leftarrow (\text{rot\_pointer} + 3) \pmod W$$
   (The step size of +3 is relatively prime to $W = 16$, ensuring a full cycle across all bit indices).
3. **Rotated Priority Inspection**:
   The transition mask is circularly rotated by `rot_pointer`:
   $$\text{rotated\_diff}[j] = \text{raw\_diff}[(j + \text{rot\_pointer}) \pmod W]$$
4. **Quota-Limited Grant Allocation**:
   A combinational priority arbiter scans `rotated_diff` from index 0 to $W-1$, granting transitions up to `active_limit`:
   $$\text{approved\_rotated}[j] = \begin{cases} 1, & \text{if } \text{rotated\_diff}[j] = 1 \text{ and } \text{granted\_count} < \text{active\_limit} \\ 0, & \text{otherwise} \end{cases}$$
5. **Reverse Rotation & Bit Modification**:
   $$\text{approved\_mask}[i] = \text{approved\_rotated}[(i - \text{rot\_pointer} + W) \pmod W]$$
   $$P_{\text{mod}}(t) = P_{\text{prev}}(t-1) \oplus \text{approved\_mask}$$

This guarantees:
- **Strict Bound**: The instantaneous number of transitions never exceeds `active_limit`.
- **Zero Starvation**: All $W$ bit positions experience an identical long-term switching probability, preserving spatial entropy and fault detection efficiency!

---

## 4. Fractional Dither Toggle-Rate Controller

Because $W = 16$, integer limits yield discrete toggle rates:
- Limit = 1: $1/16 = 6.25\%$
- Limit = 2: $2/16 = 12.50\%$
- Limit = 3: $3/16 = 18.75\%$
- Limit = 4: $4/16 = 25.00\%$
- Limit = 5: $5/16 = 31.25\%$

To hit exact fractional targets (such as **10.0%**, **20.0%**, **30.0%**, **40.0%**, **60.0%**), the controller implements a **First-Order Sigma-Delta / Fractional Dither Accumulator**:

For target 10% ($16 \times 0.10 = 1.6$ toggles/pattern average):
- In every block of 10 patterns, 6 patterns use Limit = 2, and 4 patterns use Limit = 1:
  $$\text{Average Toggles} = \frac{6 \times 2 + 4 \times 1}{10} = 1.60 \implies \frac{1.60}{16} = \mathbf{10.00\% \text{ exactly!}}$$

For target 20% ($16 \times 0.20 = 3.2$ toggles/pattern average):
- Alternates between Limit = 3 and Limit = 4:
  $$\text{Average Toggles} = \frac{8 \times 3 + 2 \times 4}{10} = 3.20 \implies \frac{3.20}{16} = \mathbf{20.00\% \text{ exactly!}}$$

Similarly, for the serial scan-shift stream, a Bresenham rate multiplier adds `target_pct` each shift clock, granting serial transitions only when the accumulator overflows 100, directly achieving the exact programmed serial scan toggle rate!

