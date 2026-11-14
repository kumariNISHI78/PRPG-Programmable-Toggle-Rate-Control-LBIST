# Architecture and Algorithmic Analysis: Low-Power Scan-Based LBIST PRPG

**Project**: Design and Implementation of Scan-Based Logic Built-In Self-Test (LBIST) with Programmable Scan-Shift Power Control Using MIPS32 Architecture  
**Role**: Member 2 – PRPG and Toggle-Rate Control  
**Author**: Antigravity (Pair Programming with Engineering Team)  
**Date**: November 2026  

---

## 1. Executive Summary and Problem Formulation

In modern VLSI systems, Logic Built-In Self-Test (LBIST) provides an autonomous, self-contained mechanism to test internal digital logic without relying on expensive Automated Test Equipment (ATE). At the core of conventional LBIST is a Linear Feedback Shift Register (LFSR) acting as a Pseudorandom Pattern Generator (PRPG). The generated pseudorandom vectors are shifted into internal scan chains to initialize the internal sequential elements (flip-flops) of the Circuit Under Test (CUT), here the MIPS32 processor core (assigned to Member 1).

### 1.1 The Scan-Shift Power Crisis
During functional operation, typical microprocessor workloads switch only **5% to 20%** of circuit nodes simultaneously due to data correlation and clock gating. In contrast, an unrestricted maximal-length LFSR generates pseudo-random bits with a transition probability of:

$$P(\text{transition}) = P(b_t \ne b_{t-1}) \approx 0.5 \quad (50\% \text{ toggle rate})$$

When an unconstrained vector is serially shifted through a scan chain of length $L$, every bit transition ($0 \to 1$ or $1 \to 0$) injected at the scan-in input ripples across all subsequent scan flip-flops until it reaches the end of the chain or shifts out. Specifically, if a transition enters at cycle $t$, it causes switching in cell 0 at cycle $t$, cell 1 at cycle $t+1$, ..., and cell $L-1$ at cycle $t+L-1$.

The dynamic power dissipation in CMOS digital circuits is governed by:

$$P_{\text{dynamic}} = \alpha \cdot C_{\text{eff}} \cdot V_{DD}^2 \cdot f_{\text{shift}}$$

where:
- $\alpha$: Switching activity factor (average probability of a node toggling per clock cycle).
- $C_{\text{eff}}$: Total effective switched load capacitance (scan flip-flop internals, clock distribution tree, scan routing, and combinational logic driven by scan flip-flops).
- $V_{DD}$: Supply voltage.
- $f_{\text{shift}}$: Scan shifting clock frequency.

During scan shift with $\alpha \approx 0.50$, the cumulative power consumption, peak supply current ($I_{\text{peak}}$), and transient $L \frac{di}{dt}$ ground bounce are **200% to 500% higher** than rated functional limits. This causes severe adverse effects:
1. **Excessive $IR$ Voltage Drop**: Causes false timing violations during shift, leading to pseudo-defects and unnecessary test yield loss.
2. **Elevated Junction Temperatures**: Thermal stress can physically damage the silicon or packaging during manufacturing burn-in and wafer-level test.
3. **Battery Depletion in Field LBIST**: Prevents reliable in-field or power-on self-test in automotive, aerospace, and battery-operated IoT applications.

---

## 2. Theoretical Analysis of Pattern Modification Algorithms

To control and reduce scan-shift switching activity, several algorithmic strategies exist in Design for Testability (DFT) literature. We evaluate four candidate approaches below:

| Approach | Working Principle | Hardware Complexity | Impact on Fault Coverage | Programmability | Evaluation for LBIST |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A. Selective Bit-Flipping** | XORs specific bit positions based on fixed decoding logic to match precomputed deterministic ATPG cubes. | Medium (depends on target cube count; requires term decoders). | High for deterministic ATPG; poor for autonomous pseudorandom LBIST. | Rigid; hardcoded to specific circuit structure; cannot dynamically vary toggle rate. | **Rejected**: Not flexible for variable power budgets; highly dependent on CUT netlist. |
| **B. Programmable Bit-Masking (AND/OR Gating)** | Forces subsets of scan chains or parallel bits to constant '0' or '1' using masking gates. | Low (AND/OR gates with enable masks). | Moderate to severe (masked cells cannot detect faults requiring the masked polarity). | Coarse (coarse-grained steps like 25%, 50%, 75%). | **Rejected**: Creates severe fault-coverage dead zones by starving certain scan cells of alternating stimuli. |
| **C. Transition Suppression with Bit-Holding** | Detects when a generated transition would violate the target toggle budget. If disallowed, holds the previous bit value ($P_{\text{mod}}(t) = P_{\text{mod}}(t-1)$). | Low to Medium (requires subtractor/accumulator, priority logic, and multiplexers). | Preserves pseudorandom properties and state space; distributes transitions across test time. | Excellent; easily programmable from 10% to 60% and bypass (100%). | **Selected as Core Mechanism**. |
| **D. Rotating Priority Token-Based Transition Suppression** | Extends Transition Suppression by adding a rotating round-robin priority token pointer that shifts the transition allocation window across cycles. | Low (1 shift-register/counter ring + priority encoder tree). | Eliminates structural spatial bias; ensures all bit positions have equal long-term transition probability. | Optimal; strictly enforces both instantaneous and average toggle rate targets. | **Selected & Implemented**. |

### 2.1 Justification for the Selected Technique
Our design implements **Dual-Domain Rotating Transition Suppression (DDRTS)**:
1. **Parallel Vector Domain**: For $W$-bit parallel words feeding scan chains, the raw Hamming distance $H_{\text{raw}}(t) = \sum_{i=0}^{W-1} (P_{\text{LFSR}, i}(t) \oplus P_{\text{prev}, i}(t-1))$ is calculated. The programmable controller translates the selected target toggle rate $T\%$ into an allowable transition quota $K_{\text{target}} = \text{round}(W \times T\%)$. If $H_{\text{raw}} > K_{\text{target}}$, only $K_{\text{target}}$ transitions are granted, and remaining candidate transitions are suppressed by retaining $P_{\text{prev}, i}$.
2. **Rotating Spatial Priority**: To prevent lower-index bits from starving higher-index bits (which would otherwise suppress transitions always in bits $[K_{\text{target}} \dots W-1]$ and collapse fault coverage on upper scan chains), a cyclic rotation pointer shifts the starting index of the priority encoder by $(t \bmod W)$ each cycle.
3. **Serial Scan-Shift Domain**: For serial scan input streams, a fractional accumulator (Bresenham-style rate multiplier) tracks the exact transition budget. When the raw serial LFSR bit attempts a transition ($S_{\text{LFSR}}(t) \ne S_{\text{prev}}(t-1)$), it is enabled only if the accumulator overflows its programmable step threshold. Otherwise, the previous scan-in bit is repeated ($S_{\text{mod}}(t) = S_{\text{prev}}(t-1)$).

---

## 3. Mathematical Distinction: Word Hamming Distance vs. Scan-Chain Shift Power

A critical theoretical requirement of this project is to explicitly distinguish between:
1. **Pattern-to-Pattern Word Hamming Distance ($HD$)**:
   $$\text{HD}(P_A, P_B) = \sum_{i=0}^{W-1} (P_{A, i} \oplus P_{B, i})$$
   This measures the parallel bit difference between two consecutive words. If words are applied broadside (e.g. PI capture), $HD$ measures input switching.

2. **Scan-Chain Shift Switching Activity ($SCA$)**:
   In a scan chain with $L$ sequential cells, let $C_j(t) \in \{0, 1\}$ be the binary state of cell $j \in [0, L-1]$ at shift clock cycle $t$.
   At shift clock $t$, the scan chain undergoes a single-bit right shift with serial input $S_{\text{in}}(t)$:
   $$C_0(t) = S_{\text{in}}(t)$$
   $$C_j(t) = C_{j-1}(t-1), \quad \forall j \in [1, L-1]$$
   
   A flip-flop switch occurs at cycle $t$ if $C_j(t) \ne C_j(t-1)$.
   Notice that:
   $$C_j(t) \oplus C_j(t-1) = C_{j-1}(t-1) \oplus C_{j-1}(t-2) = \dots = S_{\text{in}}(t-j) \oplus S_{\text{in}}(t-j-1)$$
   
   Thus, cell $j$ switches at cycle $t$ if and only if the serial scan-in stream had a transition between cycles $(t-j)$ and $(t-j-1)$.
   The total number of internal flip-flop transitions across the entire scan chain during shift cycle $t$ is:
   $$\text{Transitions}(t) = \sum_{j=0}^{L-1} (C_j(t) \oplus C_j(t-1))$$

   Over a complete scan shift sequence of $N_{\text{shift}}$ clock cycles, the **Cumulative Scan Toggle Rate** is defined as:
   $$\text{Scan Toggle Rate (\%)} = \frac{\sum_{t=1}^{N_{\text{shift}}} \sum_{j=0}^{L-1} (C_j(t) \oplus C_j(t-1))}{N_{\text{shift}} \times L} \times 100\%$$

   By controlling the transition density of $S_{\text{in}}(t)$ using our programmable modifier, the transition count inside the scan chain is directly scaled from the nominal 50% baseline down to the exact programmed target (10%, 20%, 30%, 40%, 50%, 60%).

---

## 4. Hardware Module Partitioning

The Member 2 design is partitioned into modular, fully synthesizable VHDL entities:

1. **`lfsr_prpg.vhd`**:
   - Parameterizable width $W$ (default 16 or 32).
   - Maximal-length primitive polynomial implementation (Galois topology for minimal critical path delay).
   - Autonomous anti-lockup zero-detection and non-zero seed recovery logic.
   - Synchronous clock enable and active-low reset.

2. **`conventional_prpg.vhd`**:
   - Baseline benchmark architecture without modification.
   - Generates unconstrained pseudorandom patterns and logs continuous Hamming distance and toggle rate metrics.

3. **`hamming_distance.vhd`**:
   - Synthesizable combinational popcount / adder-tree computing $\sum (A_i \oplus B_i)$.
   - Latency-free combinational output feeding the controller.

4. **`pattern_modifier.vhd`**:
   - Implements Rotating Priority Token-Based Transition Suppression.
   - Modifies incoming parallel vectors to strictly satisfy the programmable limit $K_{\text{target}}$.
   - Implements serial transition holding for scan-in serial streams.

5. **`toggle_rate_controller.vhd`**:
   - Programmable configuration decoder supporting standard target rates:
     - `000`: 10%
     - `001`: 20%
     - `010`: 30%
     - `011`: 40%
     - `100`: 50%
     - `101`: 60%
     - `110`: Bypass (Unconstrained LFSR)
     - `111`: Custom rate via register
   - Accumulator and rate meter tracking cumulative toggles, pattern counts, and measured percentages.

6. **`modified_prpg_top.vhd`**:
   - Integrates all Member 2 blocks with clean handshakes:
     - Connects to Member 1 (MIPS32 scan chain inputs).
     - Connects to Member 3 (LBIST controller and MISR).

7. **`scan_chain_model.vhd`**:
   - Hardware simulation verification model representing a physical scan chain of $L$ cells.
   - Tracks actual physical flip-flop switching to verify dynamic power reduction during shift.

