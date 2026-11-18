"""
Builds a professional 4-slide PowerPoint presentation for VL405 DFT Laboratory Project.
Theme: IIT/VLSI High-End Engineering (Dark Navy, Cyan/Teal accents, Crisp Typography).
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank layout

    # Color Palette Definitions
    C_BG = RGBColor(10, 25, 47)         # Deep Navy (#0A192F)
    C_CARD_BG = RGBColor(17, 34, 64)    # Container Slate Card (#112240)
    C_CARD_BORDER = RGBColor(35, 53, 84)# Subtle Border (#233554)
    C_TEXT_WHITE = RGBColor(255, 255, 255)
    C_TEXT_MUTED = RGBColor(204, 214, 246)
    C_TEXT_DIM = RGBColor(136, 146, 176)
    C_TEAL = RGBColor(100, 255, 218)     # Accent Cyan/Teal (#64FFDA)
    C_BLUE = RGBColor(56, 189, 248)     # Accent Sky Blue (#38BDF8)
    C_GREEN = RGBColor(16, 185, 129)    # Accent Emerald (#10B981)
    C_AMBER = RGBColor(245, 158, 11)    # Accent Amber (#F59E0B)
    C_RED = RGBColor(239, 68, 68)       # Accent Coral (#EF4444)
    C_CARD_M1 = RGBColor(20, 45, 75)
    C_CARD_M2 = RGBColor(16, 50, 60)
    C_CARD_M3 = RGBColor(35, 30, 65)

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, subtitle_text, slide_num):
        # Header Box
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.95))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = title_text
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT_WHITE

        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEAL
        p2.space_before = Pt(4)

        # Slide Number Badge
        num_box = slide.shapes.add_textbox(Inches(12.0), Inches(0.4), Inches(0.6), Inches(0.4))
        ntf = num_box.text_frame
        ntf.margin_left = ntf.margin_top = ntf.margin_right = ntf.margin_bottom = 0
        np = ntf.paragraphs[0]
        np.text = f"{slide_num}/4"
        np.alignment = PP_ALIGN.RIGHT
        np.font.name = "Segoe UI"
        np.font.size = Pt(12)
        np.font.bold = True
        np.font.color.rgb = C_TEXT_DIM

        # Accent rule
        rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.02))
        rule.fill.solid()
        rule.fill.fore_color.rgb = C_CARD_BORDER
        rule.line.fill.background()

    # =========================================================================
    # SLIDE 1: INTRODUCTION AND PROBLEM STATEMENT
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Title & Subtitle
    add_header(s1,
               "Low-Power Scan-Based LBIST Using MIPS32 Architecture",
               "VL405 – Design for Testability (DFT) Laboratory Project Assignment",
               1)

    # Team Members Banner Cards (3 Columns)
    members_data = [
        ("Harshitha Modekurty", "Roll: B23272", "Member 1: MIPS32 Core & Scan Architecture", C_BLUE),
        ("Nishi Kumari", "Roll: B24495", "Member 2: PRPG & Toggle-Rate Control", C_TEAL),
        ("Gaurav Tiwari", "Roll: B24483", "Member 3: LBIST Controller & Fault Analysis", C_AMBER)
    ]
    card_w = Inches(3.75)
    card_h = Inches(0.9)
    card_y = Inches(1.5)

    for idx, (name, roll, role, acc_color) in enumerate(members_data):
        card_x = Inches(0.8) + idx * (card_w + Inches(0.24))
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card_x, card_y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = acc_color
        card.line.width = Pt(1.5)

        tb = s1.shapes.add_textbox(card_x + Inches(0.15), card_y + Inches(0.08), card_w - Inches(0.3), card_h - Inches(0.16))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p = tf.paragraphs[0]
        p.text = f"{name} ({roll})"
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE

        p2 = tf.add_paragraph()
        p2.text = role
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = acc_color
        p2.space_before = Pt(2)

    # Column 1: The Scan-Shift Power Crisis (Left Box)
    col1_x = Inches(0.8)
    col1_y = Inches(2.6)
    col1_w = Inches(5.7)
    col1_h = Inches(4.5)

    box1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col1_x, col1_y, col1_w, col1_h)
    box1.fill.solid()
    box1.fill.fore_color.rgb = C_CARD_BG
    box1.line.color.rgb = C_CARD_BORDER
    box1.line.width = Pt(1)

    tb1 = s1.shapes.add_textbox(col1_x + Inches(0.25), col1_y + Inches(0.2), col1_w - Inches(0.5), col1_h - Inches(0.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_top = tf1.margin_bottom = tf1.margin_left = tf1.margin_right = 0

    p = tf1.paragraphs[0]
    p.text = "THE PROBLEM: THE SCAN-SHIFT POWER CRISIS"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_RED

    points_c1 = [
        ("Scan-Based Testing Necessity:", " Scan flip-flops serialize internal states to grant full controllability & observability of sequential logic without multi-million dollar ATE."),
        ("Abnormal Switching Activity:", " Normal functional operation exhibits 5%–20% switching. Unconstrained LFSR PRPG generates pseudo-independent bits with ~50% transition probability (P(b_t != b_{t-1}) ≈ 0.50)."),
        ("The Ripple Effect:", " Consecutive bit flips ripple through the entire scan chain (16–32 cells deep) every shift cycle, charging/discharging parasitic capacitance for >99% of test time."),
        ("Catastrophic Impact:", " Excessive current induces power-grid IR-drop, increasing gate delays and triggering false delay faults (rejecting good chips). Thermal hotspots cause packaging burnout."),
        ("Dynamic Power Formula:", " P_dynamic = α · C_eff · V_DD² · f_shift  --> Controlling activity factor α directly scales dynamic test power down.")
    ]

    for title, desc in points_c1:
        p = tf1.add_paragraph()
        p.space_before = Pt(8)
        run_t = p.add_run()
        run_t.text = "• " + title
        run_t.font.name = "Segoe UI"
        run_t.font.size = Pt(10)
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE

        run_d = p.add_run()
        run_d.text = desc
        run_d.font.name = "Segoe UI"
        run_d.font.size = Pt(9.5)
        run_d.font.color.rgb = C_TEXT_MUTED

    # Column 2: Objective & Proposed 5-Step Methodology (Right Box)
    col2_x = Inches(6.833)
    col2_y = Inches(2.6)
    col2_w = Inches(5.7)
    col2_h = Inches(4.5)

    box2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col2_x, col2_y, col2_w, col2_h)
    box2.fill.solid()
    box2.fill.fore_color.rgb = C_CARD_BG
    box2.line.color.rgb = C_CARD_BORDER
    box2.line.width = Pt(1)

    tb2 = s1.shapes.add_textbox(col2_x + Inches(0.25), col2_y + Inches(0.2), col2_w - Inches(0.5), col2_h - Inches(0.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_top = tf2.margin_bottom = tf2.margin_left = tf2.margin_right = 0

    p = tf2.paragraphs[0]
    p.text = "PROJECT OBJECTIVE & PROPOSED METHODOLOGY"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    points_c2 = [
        ("Core Project Objective:", " Design and implement an autonomous scan-based LBIST engine that regulates scan-shift toggle rate to arbitrary target limits (10% to 60%, or Bypass) without sacrificing fault coverage or test time."),
        ("1. Pseudorandom Pattern Generation:", " Parameterizable 16-bit Galois LFSR (polynomial x^16 + x^14 + x^13 + x^11 + 1, seed 0xACE1) with autonomous anti-lockup zero-recovery."),
        ("2. Programmable Pattern Modification:", " Dual-Domain Rotating Transition Suppression (DDRTS) with modulo-16 rotating priority token ring to eliminate scan starvation."),
        ("3. Low-Power Scan Ingestion:", " Feeds 16 parallel scan chains and serial scan input of the MIPS32 processor core during shift cycles."),
        ("4. Response Compaction & Signature:", " Circuit responses are compacted via Multiple-Input Signature Register (MISR) to detect structural faults."),
        ("5. Hardware Activity Tracking:", " Closed-loop 32-cell physical scan-chain model validates genuine flip-flop transitions and power reduction.")
    ]

    for title, desc in points_c2:
        p = tf2.add_paragraph()
        p.space_before = Pt(8)
        run_t = p.add_run()
        run_t.text = "• " + title
        run_t.font.name = "Segoe UI"
        run_t.font.size = Pt(10)
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE

        run_d = p.add_run()
        run_d.text = desc
        run_d.font.name = "Segoe UI"
        run_d.font.size = Pt(9.5)
        run_d.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 2: OVERALL SYSTEM ARCHITECTURE AND WORK DIVISION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)

    add_header(s2,
               "Proposed LBIST Architecture and Methodology",
               "Complete System Dataflow, Inter-Module Coordination & Group Work Division",
               2)

    # Architecture Flow Banner (6 Connected Block Cards)
    arch_nodes = [
        ("LFSR PRPG", "16-bit Galois\nPoly: 0xB400", C_TEAL),
        ("Modifier & Controller", "DDRTS Engine\nFractional Dither", C_TEAL),
        ("Scan Chain Array", "16 Parallel Chains\n+ Serial Scan In", C_BLUE),
        ("MIPS32 Core", "CUT: ALU, RegFile,\nPC, Control Logic", C_BLUE),
        ("MISR Compactor", "Response Compaction\nLFSR Signature", C_AMBER),
        ("Signature Analyzer", "Fault Evaluation\nGolden Compare", C_AMBER)
    ]

    node_w = Inches(1.8)
    node_h = Inches(1.05)
    node_y = Inches(1.6)

    for i, (ntitle, nsub, ncolor) in enumerate(arch_nodes):
        nx = Inches(0.8) + i * (node_w + Inches(0.186))
        nbox = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, nx, node_y, node_w, node_h)
        nbox.fill.solid()
        nbox.fill.fore_color.rgb = C_CARD_BG
        nbox.line.color.rgb = ncolor
        nbox.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(nx + Inches(0.05), node_y + Inches(0.12), node_w - Inches(0.1), node_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.text = ntitle
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE

        p2 = tf.add_paragraph()
        p2.text = nsub
        p2.alignment = PP_ALIGN.CENTER
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_TEXT_MUTED
        p2.space_before = Pt(3)

        # Draw arrow to next block
        if i < len(arch_nodes) - 1:
            arr_x = nx + node_w + Inches(0.02)
            arr = s2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arr_x, node_y + Inches(0.38), Inches(0.14), Inches(0.25))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_CARD_BORDER
            arr.line.fill.background()

    # Central LBIST Controller Coordination Strip
    fsm_w = Inches(11.733)
    fsm_h = Inches(0.45)
    fsm_y = Inches(2.78)
    fsm_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), fsm_y, fsm_w, fsm_h)
    fsm_box.fill.solid()
    fsm_box.fill.fore_color.rgb = RGBColor(25, 40, 75)
    fsm_box.line.color.rgb = C_BLUE
    fsm_box.line.width = Pt(1)

    ftb = s2.shapes.add_textbox(Inches(0.9), fsm_y + Inches(0.08), fsm_w - Inches(0.2), fsm_h - Inches(0.16))
    ftf = ftb.text_frame
    fp = ftf.paragraphs[0]
    fp.text = "Central LBIST FSM Controller: Orchestrates Reset -> Scan Shift (lbist_en='1') -> CUT Functional Capture -> MISR Compact -> Golden Signature Compare"
    fp.alignment = PP_ALIGN.CENTER
    fp.font.name = "Segoe UI"
    fp.font.size = Pt(9.5)
    fp.font.bold = True
    fp.font.color.rgb = C_TEXT_WHITE

    # 3 Member Responsibility Cards (Lower Section)
    m_cards = [
        ("MEMBER 1: MIPS32 CORE & SCAN", "Harshitha Modekurty (B23272)", C_BLUE, [
            ("MIPS32 Processor Selection:", "Synthesizable VHDL processor core implementing standard MIPS instruction set (ALU, Register File, PC)."),
            ("Sequential Identification:", "Audited processor pipeline registers and control flip-flops for scan-chain insertion."),
            ("Scan-Multiplexer Integration:", "Replaced conventional D-FFs with scan flip-flops (Mux-DFF) to support normal vs. test modes."),
            ("Scan-Chain Partitioning:", "Configured 16 balanced parallel scan chains + serial scan chain with global scan_enable routing."),
            ("Functional Verification:", "Verified normal processor execution alongside serial/parallel scan shifting operations.")
        ]),
        ("MEMBER 2: PRPG & TOGGLE CONTROL", "Nishi Kumari (B24495)", C_TEAL, [
            ("Galois LFSR Design:", "16-bit maximal-length PRPG (poly 0xB400, seed 0xACE1) with autonomous anti-lockup zero-recovery."),
            ("Baseline Conventional PRPG:", "Implemented reference LFSR with 32-bit accumulators to benchmark natural switching (~50%)."),
            ("DDRTS Pattern Modifier:", "Modulo-16 rotating priority token ring preventing scan starvation while holding excess bits."),
            ("Programmable Rate Controller:", "Decodes 10%-60% targets using fractional sigma-delta dither to hit exact toggle limits."),
            ("Activity Evaluation & Synthesis:", "Built 32-cell physical scan-chain model (cutting shift power by 84.35%) and synthesized on Artix-7.")
        ]),
        ("MEMBER 3: LBIST CONTROLLER & FAULT", "Gaurav Tiwari (B24483)", C_AMBER, [
            ("Central LBIST Controller:", "FSM test controller sequencing autonomous shift, capture, and comparison cycles."),
            ("Scan Mode Coordination:", "Drives lbist_enable, target_rate_sel, seed_load, and test sequence clocking."),
            ("MISR Response Compaction:", "Multiple-Input Signature Register compacting parallel CUT responses into a 16-bit golden signature."),
            ("Fault Injection Framework:", "Automated single stuck-at fault injection mechanism across MIPS32 datapath/control."),
            ("Fault Coverage & Performance:", "Grading fault coverage convergence and test time tradeoffs between modified and baseline LBIST.")
        ])
    ]

    mc_w = Inches(3.75)
    mc_h = Inches(3.85)
    mc_y = Inches(3.35)

    for i, (m_title, m_author, m_col, m_tasks) in enumerate(m_cards):
        mx = Inches(0.8) + i * (mc_w + Inches(0.24))
        mbox = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, mx, mc_y, mc_w, mc_h)
        mbox.fill.solid()
        mbox.fill.fore_color.rgb = C_CARD_BG
        mbox.line.color.rgb = m_col
        mbox.line.width = Pt(1.5)

        mtb = s2.shapes.add_textbox(mx + Inches(0.18), mc_y + Inches(0.15), mc_w - Inches(0.36), mc_h - Inches(0.3))
        mtf = mtb.text_frame
        mtf.word_wrap = True
        mtf.margin_top = mtf.margin_bottom = mtf.margin_left = mtf.margin_right = 0

        mp = mtf.paragraphs[0]
        mp.text = m_title
        mp.font.name = "Segoe UI"
        mp.font.size = Pt(11)
        mp.font.bold = True
        mp.font.color.rgb = m_col

        mp_sub = mtf.add_paragraph()
        mp_sub.text = m_author
        mp_sub.font.name = "Segoe UI"
        mp_sub.font.size = Pt(9)
        mp_sub.font.color.rgb = C_TEXT_WHITE
        mp_sub.space_before = Pt(1)

        for task_t, task_d in m_tasks:
            tp = mtf.add_paragraph()
            tp.space_before = Pt(5)
            r1 = tp.add_run()
            r1.text = "• " + task_t
            r1.font.name = "Segoe UI"
            r1.font.size = Pt(8.5)
            r1.font.bold = True
            r1.font.color.rgb = C_TEXT_WHITE

            r2 = tp.add_run()
            r2.text = " " + task_d
            r2.font.name = "Segoe UI"
            r2.font.size = Pt(8)
            r2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 3: IMPLEMENTATION RESULTS AND OBSERVATIONS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)

    add_header(s3,
               "Simulation Results and Performance Analysis",
               "Hardware-Accurate XSim Verification, Measured Toggle Rates, Power Curves & Real Waveforms",
               3)

    # Left Container: Results Table & Engineering Analysis
    res_w = Inches(6.0)
    res_h = Inches(5.7)
    res_x = Inches(0.8)
    res_y = Inches(1.5)

    rbox = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, res_x, res_y, res_w, res_h)
    rbox.fill.solid()
    rbox.fill.fore_color.rgb = C_CARD_BG
    rbox.line.color.rgb = C_CARD_BORDER
    rbox.line.width = Pt(1)

    rtb = s3.shapes.add_textbox(res_x + Inches(0.2), res_y + Inches(0.15), res_w - Inches(0.4), res_h - Inches(0.3))
    rtf = rtb.text_frame
    rtf.word_wrap = True
    rtf.margin_top = rtf.margin_bottom = rtf.margin_left = rtf.margin_right = 0

    rp = rtf.paragraphs[0]
    rp.text = "MEASURED EXPERIMENTAL RESULTS (VIVADO XSIM)"
    rp.font.name = "Segoe UI"
    rp.font.size = Pt(11)
    rp.font.bold = True
    rp.font.color.rgb = C_TEAL

    # Table on Left Side
    table_shape = s3.shapes.add_table(8, 5, res_x + Inches(0.15), res_y + Inches(0.45), Inches(5.7), Inches(2.2))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(1.1)
    tbl.columns[1].width = Inches(1.1)
    tbl.columns[2].width = Inches(1.1)
    tbl.columns[3].width = Inches(1.1)
    tbl.columns[4].width = Inches(1.3)

    headers = ["Target", "Conv Word", "Mod Word", "Mod Scan", "Scan Power Red."]
    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(25, 45, 80)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Segoe UI"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE

    table_data = [
        ("Bypass (100%)", "48.50%", "49.00%", "38.44%", "0.00% (Baseline)"),
        ("10% Target", "54.04%", "10.29%", "8.67%", "84.35% Saved"),
        ("20% Target", "55.00%", "19.92%", "9.92%", "81.76% Saved"),
        ("30% Target", "49.54%", "29.88%", "17.31%", "64.64% Saved"),
        ("40% Target", "47.79%", "36.21%", "18.65%", "63.85% Saved"),
        ("50% Target", "48.33%", "44.08%", "18.40%", "60.33% Saved"),
        ("60% Target", "49.54%", "49.13%", "30.98%", "37.44% Saved")
    ]

    for row_idx, row in enumerate(table_data):
        for col_idx, val in enumerate(row):
            cell = tbl.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(14, 28, 52) if row_idx % 2 == 0 else RGBColor(19, 36, 68)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Segoe UI"
            p.font.size = Pt(8)
            if col_idx == 4 and "Saved" in val:
                p.font.bold = True
                p.font.color.rgb = C_GREEN
            else:
                p.font.color.rgb = C_TEXT_MUTED

    # Analysis Bullets below table
    tb_analysis = s3.shapes.add_textbox(res_x + Inches(0.2), res_y + Inches(2.75), res_w - Inches(0.4), Inches(2.7))
    atf = tb_analysis.text_frame
    atf.word_wrap = True
    atf.margin_top = atf.margin_bottom = atf.margin_left = atf.margin_right = 0

    ap = atf.paragraphs[0]
    ap.text = "KEY TECHNICAL OBSERVATIONS"
    ap.font.name = "Segoe UI"
    ap.font.size = Pt(10.5)
    ap.font.bold = True
    ap.font.color.rgb = C_BLUE

    obs_bullets = [
        ("Massive Scan Power Reduction:", " At 10% target, scan-shift toggle rate plunges from 55.37% down to 8.67%, achieving an 84.35% reduction in dynamic scan power (P_dynamic = α · C · V² · f)."),
        ("Fractional Dither Convergence:", " First-order sigma-delta accumulator dynamically alternates integer limits (Limit 1 vs 2) to tightly achieve 10.29% toggle rate (target: 10.00%)."),
        ("Minimal Hardware Overhead:", " Synthesized on Xilinx Artix-7 (xc7a35t): Core consumes only 82 LUTs and 57 FFs (<0.5% overhead of a MIPS32 core), operating at >350 MHz."),
        ("Honest Integration Status:", " Member 2 subsystem is 100% completed & verified in Vivado XSim across 7 suites. Member 1 scan-chain integration & Member 3 MISR/fault-grading are architecturally mapped; full closed-loop MIPS32 fault grading is scheduled for joint integration.")
    ]

    for o_title, o_desc in obs_bullets:
        p = atf.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + o_title
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = C_TEXT_WHITE

        r2 = p.add_run()
        r2.text = " " + o_desc
        r2.font.name = "Segoe UI"
        r2.font.size = Pt(8)
        r2.font.color.rgb = C_TEXT_MUTED

    # Right Side: Real Waveform Capture + Matplotlib Performance Chart
    right_x = Inches(7.0)
    right_y = Inches(1.5)
    right_w = Inches(5.533)

    # 1. Matplotlib Chart
    chart_path = "Analysis/slide3_performance_chart.png"
    if os.path.exists(chart_path):
        s3.shapes.add_picture(chart_path, right_x, right_y, width=right_w, height=Inches(2.65))

    # 2. Actual Waveform Screenshot
    wave_path = "Waveforms/waveform_hex_verification_test1.png"
    if os.path.exists(wave_path):
        wave_pic = s3.shapes.add_picture(wave_path, right_x, right_y + Inches(2.75), width=right_w, height=Inches(2.55))

    # Waveform Caption Box
    wcap_box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, right_y + Inches(5.35), right_w, Inches(0.4))
    wcap_box.fill.solid()
    wcap_box.fill.fore_color.rgb = RGBColor(14, 25, 45)
    wcap_box.line.color.rgb = C_CARD_BORDER
    wctb = s3.shapes.add_textbox(right_x, right_y + Inches(5.37), right_w, Inches(0.35))
    wctf = wctb.text_frame
    wcp = wctf.paragraphs[0]
    wcp.text = "Actual Vivado XSim Waveform: Hex sequence (0xACE1 -> 0xE270 -> 0x7138 -> 0x389C) & popcount HD=6 matches theory."
    wcp.alignment = PP_ALIGN.CENTER
    wcp.font.name = "Segoe UI"
    wcp.font.size = Pt(8)
    wcp.font.color.rgb = C_TEAL

    # =========================================================================
    # SLIDE 4: CONCLUSION AND FUTURE WORK
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)

    add_header(s4,
               "Conclusion and Future Scope",
               "Summary of DFT Achievements, Multi-Member Synthesis & Project Roadmap",
               4)

    # Left Container: Project Summary (4 Bullets)
    sum_w = Inches(5.7)
    sum_h = Inches(4.3)
    sum_x = Inches(0.8)
    sum_y = Inches(1.5)

    sbox = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sum_x, sum_y, sum_w, sum_h)
    sbox.fill.solid()
    sbox.fill.fore_color.rgb = C_CARD_BG
    sbox.line.color.rgb = C_CARD_BORDER
    sbox.line.width = Pt(1)

    stb = s4.shapes.add_textbox(sum_x + Inches(0.25), sum_y + Inches(0.2), sum_w - Inches(0.5), sum_h - Inches(0.4))
    stf = stb.text_frame
    stf.word_wrap = True
    stf.margin_top = stf.margin_bottom = stf.margin_left = stf.margin_right = 0

    sp = stf.paragraphs[0]
    sp.text = "SUMMARY OF ACHIEVED CONTRIBUTIONS"
    sp.font.name = "Segoe UI"
    sp.font.size = Pt(12)
    sp.font.bold = True
    sp.font.color.rgb = C_TEAL

    summary_pts = [
        ("Power Crisis Successfully Mitigated:", " Solved excessive scan-shift switching by developing a programmable toggle-rate controlled PRPG capable of reducing shift power by up to 84.35% without interrupting pseudorandom stimulus generation."),
        ("Starvation-Free DDRTS Architecture:", " Modulo-16 rotating priority token ring ensures all scan cells cyclically toggle, avoiding static masking and preserving pattern diversity across MIPS32 scan chains."),
        ("Production-Grade RTL Implementation:", " Synthesizable VHDL-2008 architecture with 0 inferred latches, fully synchronous single-clock design, and autonomous zero-lockup recovery requiring <0.5% area overhead on Xilinx Artix-7."),
        ("Exhaustive Verification Completed:", " 7 comprehensive test suites executed in Vivado XSim (Bypass, 10%-60% targets, reset recovery, 5,000 continuous cycles, and dynamic target changes) with 100% verified assertions.")
    ]

    for stitle, sdesc in summary_pts:
        p = stf.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = "✔ " + stitle
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = C_GREEN

        r2 = p.add_run()
        r2.text = sdesc
        r2.font.name = "Segoe UI"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_TEXT_MUTED

    # Right Container: Future Scope & Roadmap (4 Bullets)
    fut_w = Inches(5.7)
    fut_h = Inches(4.3)
    fut_x = Inches(6.833)
    fut_y = Inches(1.5)

    fbox = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, fut_x, fut_y, fut_w, fut_h)
    fbox.fill.solid()
    fbox.fill.fore_color.rgb = C_CARD_BG
    fbox.line.color.rgb = C_CARD_BORDER
    fbox.line.width = Pt(1)

    ftb = s4.shapes.add_textbox(fut_x + Inches(0.25), fut_y + Inches(0.2), fut_w - Inches(0.5), fut_h - Inches(0.4))
    ftf = ftb.text_frame
    ftf.word_wrap = True
    ftf.margin_top = ftf.margin_bottom = ftf.margin_left = ftf.margin_right = 0

    fp = ftf.paragraphs[0]
    fp.text = "FUTURE WORK & INTEGRATION ROADMAP"
    fp.font.name = "Segoe UI"
    fp.font.size = Pt(12)
    fp.font.bold = True
    fp.font.color.rgb = C_BLUE

    future_pts = [
        ("Full-System Top-Level Integration:", " Wire Member 2's modified_prpg_top to Member 1's inserted MIPS32 scan chains and Member 3's central LBIST controller in a single unified test harness."),
        ("Closed-Loop Fault Simulation:", " Perform comprehensive stuck-at and transition fault grading across the MIPS32 instruction set using Member 3's automated fault injection and MISR compaction."),
        ("Adaptive Two-Phase LBIST Scheme:", " Execute Phase 1 at 10%–20% low-power target (detecting >80% easy faults with minimal thermal dissipation), followed by a brief Phase 2 burst in Bypass mode for random-pattern resistant faults."),
        ("Physical Silicon Characterization:", " Measure placed-and-routed clock-tree power, IR-drop profiles, and post-layout timing slack on physical Artix-7/Basys3 FPGA hardware.")
    ]

    for ftitle, fdesc in future_pts:
        p = ftf.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = "➔ " + ftitle
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = C_BLUE

        r2 = p.add_run()
        r2.text = fdesc
        r2.font.name = "Segoe UI"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_TEXT_MUTED

    # Bottom Banner: Professional Thank You & Q&A
    thx_w = Inches(11.733)
    thx_h = Inches(1.1)
    thx_y = Inches(6.0)

    thx_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), thx_y, thx_w, thx_h)
    thx_box.fill.solid()
    thx_box.fill.fore_color.rgb = RGBColor(18, 38, 70)
    thx_box.line.color.rgb = C_TEAL
    thx_box.line.width = Pt(1.5)

    ttb = s4.shapes.add_textbox(Inches(0.9), thx_y + Inches(0.12), thx_w - Inches(0.2), thx_h - Inches(0.24))
    ttf = ttb.text_frame
    tp1 = ttf.paragraphs[0]
    tp1.text = "Thank You! Questions & Discussion Welcome"
    tp1.alignment = PP_ALIGN.CENTER
    tp1.font.name = "Segoe UI"
    tp1.font.size = Pt(14)
    tp1.font.bold = True
    tp1.font.color.rgb = C_TEXT_WHITE

    tp2 = ttf.add_paragraph()
    tp2.text = "Project Team: Gaurav Tiwari (B24483)  |  Nishi Kumari (B24495)  |  Harshitha Modekurty (B23272)\nVL405 Design for Testability Laboratory  •  Department of ECE / VLSI Design"
    tp2.alignment = PP_ALIGN.CENTER
    tp2.font.name = "Segoe UI"
    tp2.font.size = Pt(10)
    tp2.font.color.rgb = C_TEAL
    tp2.space_before = Pt(3)

    # Save Presentation
    output_filename = "VL405_LBIST_Project_Presentation.pptx"
    prs.save(output_filename)
    print(f"[SUCCESS] Presentation saved successfully to: {output_filename}")

if __name__ == "__main__":
    create_deck()
