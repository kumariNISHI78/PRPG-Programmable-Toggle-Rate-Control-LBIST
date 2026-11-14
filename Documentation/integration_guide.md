# Inter-Module Integration Guide: Member 2 (PRPG & Toggle Control)

**Project**: Design and Implementation of Scan-Based Logic Built-In Self-Test (LBIST) with Programmable Scan-Shift Power Control Using MIPS32 Architecture  
**Document**: Interface Specification & Inter-Team Integration Manual  
**Author**: Member 2 – PRPG and Toggle-Rate Control  
**Target Audience**: Member 1 (MIPS32 Core & Scan Architecture), Member 3 (LBIST Controller & MISR)  

---

## 1. Top-Level Entity Interface: `modified_prpg_top`

The top-level entity implemented by Member 2 is:

```vhdl
entity modified_prpg_top is
    generic (
        WIDTH        : positive := 16;
        POLYNOMIAL   : std_logic_vector(15 downto 0) := x"B400";
        DEFAULT_SEED : std_logic_vector(15 downto 0) := x"ACE1"
    );
    port (
        -- Global System Signals
        clk                   : in  std_logic;
        rst_n                 : in  std_logic;
        
        -- LBIST Controller Handshake (Controlled by Member 3)
        lbist_enable          : in  std_logic;
        seed_load             : in  std_logic;
        seed_data             : in  std_logic_vector(WIDTH-1 downto 0);
        target_rate_sel       : in  std_logic_vector(2 downto 0);
        custom_toggle_limit   : in  unsigned(4 downto 0);
        pattern_valid         : out std_logic;
        all_zero_detected     : out std_logic;
        
        -- Scan Chain Interface (Connected to Member 1 CUT Scan Inputs)
        scan_data_parallel    : out std_logic_vector(WIDTH-1 downto 0);
        scan_data_serial      : out std_logic;
        
        -- Diagnostic & Fault Evaluation Signals (Monitored by Member 3)
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
```

---

## 2. Signal Mapping for Member 1 (MIPS Core & Scan Architecture)

Member 1 is responsible for the MIPS32 processor, sequential scan insertion, scan flip-flop multiplexers, and scan-chain routing.

### 2.1 Connecting Scan Inputs
Member 1 must connect the scan inputs of the MIPS32 scan chains to Member 2 as follows:

| Member 2 Port Name | Direction | Width | Member 1 Scan Architecture Connection | Description |
| :--- | :---: | :---: | :--- | :--- |
| `scan_data_serial` | **OUT** | 1 bit | `SCAN_IN` of primary serial scan chain | High-efficiency toggle-controlled serial test pattern. Injected into cell 0 of the scan chain during scan shift mode (`scan_enable = '1'`). |
| `scan_data_parallel` | **OUT** | $W$ bits (16/32) | Multiple parallel scan chain inputs `SCAN_IN[15:0]` | Parallel scan input bus for partitioned scan chains (e.g. 16 parallel chains across ALU, Register File, PC, and Control). |
| `pattern_valid` | **OUT** | 1 bit | `SCAN_INPUT_VALID` | Qualified strobe indicating that valid, stabilized test data is present on the scan outputs. |

### 2.2 Scan Shifting Timing Handshake
```text
           __    __    __    __    __    __    __    __    __
clk     __|  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__
               _____________________________________________
lbist_en _____/
                      ______________________________________
pattern_valid _______/
         =============X=====================================
scan_serial           | Bit 0 | Bit 1 | Bit 2 | Bit 3 | ...
         =============X=====================================
```
- When `lbist_enable` is asserted HIGH by Member 3, Member 2 generates a new modified scan vector on every rising edge of `clk`.
- Member 1 holds `scan_enable = '1'` during scan shifting ($L$ clock cycles) while sampling `scan_data_serial` into the MIPS scan register.

---

## 3. Signal Mapping for Member 3 (LBIST Controller & MISR Compactor)

Member 3 coordinates test sequencing, fault injection, and MISR response compaction.

### 3.1 Controller Handshake Ports

| Member 2 Port Name | Direction | Width | Member 3 Connection | Description |
| :--- | :---: | :---: | :--- | :--- |
| `lbist_enable` | **IN** | 1 bit | `PRPG_ENABLE` from LBIST FSM | Clocks the PRPG and pattern modifier. Deasserted during CUT functional capture cycles. |
| `target_rate_sel` | **IN** | 3 bits | `CONFIG_REG[2:0]` / FSM State | Selects target toggle rate (see decoding table below). |
| `seed_load` | **IN** | 1 bit | `RESEED_STROBE` | Optional: asserts HIGH for 1 cycle to reload PRPG seed. |
| `seed_data` | **IN** | $W$ bits | `SEED_REGISTER` | Seed vector to load into PRPG. |
| `custom_toggle_limit` | **IN** | 5 bits | `CUSTOM_LIMIT_REG` | Direct toggle limit used when `target_rate_sel = "111"`. |
| `all_zero_detected` | **OUT** | 1 bit | `DFT_STATUS_FAULT` | Hardware alert flag: asserts '1' if LFSR ever enters all-zero state (triggers autonomous recovery). |

### 3.2 Target Toggle-Rate Decoding Table

| `target_rate_sel(2 downto 0)` | Selected Mode | Nominal Toggle Rate | Scan Power Saved vs. Baseline | Use Case Recommendation |
| :---: | :---: | :---: | :---: | :--- |
| `"000"` | **Ultra Low Power** | **10.0%** | **~85% Power Reduction** | Thermal-critical wafer testing, low-power field BIST. |
| `"001"` | **Low Power** | **20.0%** | **~81% Power Reduction** | Standard LBIST shift mode (recommended default). |
| `"010"` | **Medium Power** | **30.0%** | **~72% Power Reduction** | Balanced power-coverage trade-off. |
| `"011"` | **Moderate Power** | **40.0%** | **~63% Power Reduction** | Fast fault grading mode. |
| `"100"` | **50% Limit** | **50.0%** | **~52% Power Reduction** | Bounded pseudorandom testing. |
| `"101"` | **High Activity** | **60.0%** | **~45% Power Reduction** | At-speed delay fault test. |
| `"110"` | **Bypass Mode** | **100% (Baseline)** | **0% (Unmodified LFSR)** | Reference benchmark and baseline comparison. |
| `"111"` | **Custom Mode** | User-defined | Configurable via `custom_toggle_limit` | Parametric lab experiments and characterization. |

### 3.3 Diagnostic Outputs for Member 3 Fault Coverage Analysis
To facilitate Member 3's automated fault simulation, fault injection, and coverage grading:
1. `raw_pattern_out`: Provides the untouched, original pseudorandom sequence from the LFSR. This allows Member 3 to simulate fault coverage with the baseline PRPG without needing a separate LFSR instance.
2. `modification_active`: High when the pattern modifier intervened to suppress transitions in the current cycle.
3. `measured_toggle_rate`: Real-time 8-bit percentage register ($0 \dots 100\%$) indicating cumulative observed switching activity.
4. `total_patterns_gen`, `total_word_toggles`, `total_serial_shifts`: Hardware counters for automated test report generation.

---

## 4. Synthesis and Verification Checklist for System Integration

When integrating all three members into the top-level project `lbist_mips32_top.vhd`:

- [x] **Clocking**: Single synchronous clock domain `clk` shared across PRPG, Scan Chains, and LBIST Controller.
- [x] **Reset Strategy**: Active-low asynchronous reset `rst_n` driving all sequential elements.
- [x] **No Latches**: All Member 2 modules are 100% combinational or synchronous register updates; zero inferred latches.
- [x] **Scalability**: All modules parameterizable via generic `WIDTH` (default 16, scales to 32 for direct 32-bit MIPS data path testing).
- [x] **Area Budget**: Member 2 consumes fewer than **85 LUTs and 58 Flip-Flops**, ensuring minimal silicon footprint.

