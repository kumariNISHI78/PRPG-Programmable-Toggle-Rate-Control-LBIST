"""
Builds an academically styled, professional 3-slide PowerPoint presentation for VL405 DFT Laboratory Project.
Exact Requirements:
- 16:9 Widescreen (13.333" x 7.5")
- Bright, clean, white/light-grey background (Zero dark themes/gradients).
- Consistent professional palette: Navy Blue headings, Teal/Green solutions, Orange highlights, subtle Red problems.
- Slide 1: Introduction, Problem Statement, Objectives, and 3 Team Member Cards.
- Slide 2: Proposed LBIST Architecture as a compact, professional Flow Diagram (Controller -> PRPG -> Modifier -> MIPS32 Scan -> Capture -> MISR -> Signature Analysis) + 4-step Working Principle.
- Slide 3: Results, Observations and Conclusion (Experimental Table, Vivado Synthesis Table, Chart, Observations, Fault Coverage status, Future Work).
- 100% Native editable PowerPoint shapes, text boxes, tables, and arrows.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Academic Color Palette Definitions
    C_BG = RGBColor(250, 250, 252)          # Clean off-white background (#FAFAFC)
    C_WHITE = RGBColor(255, 255, 255)       # Card background (#FFFFFF)
    C_CARD_BORDER = RGBColor(226, 232, 240) # Subtle Card Border (#E2E8F0)
    C_BORDER_MID = RGBColor(203, 213, 225)  # Mid Border (#CBD5E1)
    
    # Typography Colors
    C_NAVY_HEADING = RGBColor(15, 37, 68)   # Deep Academic Navy (#0F2544)
    C_NAVY_SUB = RGBColor(30, 58, 138)      # Royal Navy (#1E3A8A)
    C_TEXT_DARK = RGBColor(33, 43, 54)      # Readable Charcoal Body (#212B36)
    C_TEXT_MUTED = RGBColor(99, 115, 129)   # Subtle Supporting Text (#637381)
    
    # Accent Colors (Consistent across all 3 slides)
    C_TEAL = RGBColor(13, 148, 136)         # Teal / Green (Proposed Solution / Member 2: #0D9488)
    C_BLUE = RGBColor(37, 99, 235)          # Vibrant Royal Blue (Core / Member 1: #2563EB)
    C_ORANGE = RGBColor(217, 119, 6)        # Orange / Amber (Highlights / Member 3: #D97706)
    C_RED = RGBColor(220, 38, 38)           # Subtle Red (Problem Statement: #DC2626)
    C_GREEN = RGBColor(5, 150, 105)         # Emerald Green (Power Savings: #059669)

    FONT_MAIN = "Calibri"

    def apply_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def render_header(slide, title_text, subtitle_text, slide_num):
        # Header text box
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.36), Inches(11.733), Inches(0.88))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = title_text
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(21)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY_HEADING

        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(10.5)
        p2.font.bold = True
        p2.font.color.rgb = C_NAVY_SUB
        p2.space_before = Pt(2)

        # Slide Number Badge
        num_box = slide.shapes.add_textbox(Inches(11.733), Inches(0.36), Inches(0.8), Inches(0.35))
        ntf = num_box.text_frame
        ntf.margin_left = ntf.margin_top = ntf.margin_right = ntf.margin_bottom = 0
        np = ntf.paragraphs[0]
        np.text = f"Slide {slide_num} / 3"
        np.alignment = PP_ALIGN.RIGHT
        np.font.name = FONT_MAIN
        np.font.size = Pt(11)
        np.font.bold = True
        np.font.color.rgb = C_TEXT_MUTED

        # Thin clean horizontal dividing rule
        rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.30), Inches(11.733), Inches(0.015))
        rule.fill.solid()
        rule.fill.fore_color.rgb = C_BORDER_MID
        rule.line.fill.background()

    # =========================================================================
    # SLIDE 1: INTRODUCTION AND PROJECT OVERVIEW
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s1)

    render_header(s1,
                  "Low-Power Scan-Based LBIST Using MIPS32 Architecture",
                  "VL405 – Design for Testability (DFT) Laboratory Project",
                  1)

    # 3 Compact Team Member Cards (Top Row)
    members_data = [
        ("Harshitha Modekurty", "B23272", "Member 1: MIPS32 Core & Scan Architecture", C_BLUE),
        ("Nishi Kumari", "B24495", "Member 2: PRPG & Toggle-Rate Control", C_TEAL),
        ("Gaurav Tiwari", "B24483", "Member 3: LBIST Controller & Fault Analysis", C_ORANGE)
    ]
    card_w = Inches(3.75)
    card_h = Inches(0.88)
    card_y = Inches(1.45)

    for idx, (name, roll, role, acc_color) in enumerate(members_data):
        card_x = Inches(0.8) + idx * (card_w + Inches(0.24))
        
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card_x, card_y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = acc_color
        card.line.width = Pt(1.5)

        tb = s1.shapes.add_textbox(card_x + Inches(0.18), card_y + Inches(0.12), card_w - Inches(0.36), card_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p = tf.paragraphs[0]
        p.text = f"{name} ({roll})"
        p.font.name = FONT_MAIN
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_HEADING

        p2 = tf.add_paragraph()
        p2.text = role
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = acc_color
        p2.font.bold = True
        p2.space_before = Pt(2)

    # Two Balanced Content Sections Below (Problem Statement vs. Proposed Solution & Objectives)
    sec_w = Inches(5.7)
    sec_h = Inches(4.75)
    sec_y = Inches(2.50)

    # Left Section: Introduction & Problem Statement
    sec1_x = Inches(0.8)
    box1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sec1_x, sec_y, sec_w, sec_h)
    box1.fill.solid()
    box1.fill.fore_color.rgb = C_WHITE
    box1.line.color.rgb = C_RED
    box1.line.width = Pt(1.5)

    tb1 = s1.shapes.add_textbox(sec1_x + Inches(0.25), sec_y + Inches(0.20), sec_w - Inches(0.5), sec_h - Inches(0.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_top = tf1.margin_bottom = tf1.margin_left = tf1.margin_right = 0

    p = tf1.paragraphs[0]
    p.text = "PROBLEM STATEMENT: SCAN-SHIFT POWER CRISIS"
    p.font.name = FONT_MAIN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_RED

    prob_points = [
        ("What is LBIST & Why Scan-Based Testing:", "Logic Built-In Self-Test (LBIST) integrates pattern generation and response compaction directly onto the silicon, eliminating reliance on multi-million dollar external ATE. Scan chains serialize flip-flops to ensure complete controllability and observability."),
        ("Excessive Switching Activity:", "Conventional LFSR pseudorandom patterns generate ~50% bit transitions. This is 2.5x to 10x higher than normal functional operation (5%-20%)."),
        ("The Ripple Effect in Scan Chains:", "Test vectors spend >99% of execution time shifting. Transitions ripple through every cascaded scan flip-flop, continuously charging/discharging parasitics."),
        ("IR-Drop & Thermal Degradation:", "Excessive current causes severe power-grid voltage droop (triggering false delay faults on good dies) and localized thermal hotspots that can permanently damage the packaging."),
        ("Dynamic Power Formula:", "P_dynamic = alpha · C_eff · V_DD^2 · f_shift  --> Regulating switching activity factor alpha directly cuts dynamic test power.")
    ]

    for title, desc in prob_points:
        p = tf1.add_paragraph()
        p.space_before = Pt(11)
        r1 = p.add_run()
        r1.text = "• " + title + " "
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY_HEADING

        r2 = p.add_run()
        r2.text = desc
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(9)
        r2.font.color.rgb = C_TEXT_DARK

    # Right Section: Proposed Solution & Main Objectives
    sec2_x = Inches(6.833)
    box2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sec2_x, sec_y, sec_w, sec_h)
    box2.fill.solid()
    box2.fill.fore_color.rgb = C_WHITE
    box2.line.color.rgb = C_TEAL
    box2.line.width = Pt(1.5)

    tb2 = s1.shapes.add_textbox(sec2_x + Inches(0.25), sec_y + Inches(0.20), sec_w - Inches(0.5), sec_h - Inches(0.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_top = tf2.margin_bottom = tf2.margin_left = tf2.margin_right = 0

    p = tf2.paragraphs[0]
    p.text = "PROPOSED SOLUTION & PROJECT OBJECTIVES"
    p.font.name = FONT_MAIN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    p_sol = tf2.add_paragraph()
    p_sol.space_before = Pt(6)
    p_sol_r1 = p_sol.add_run()
    p_sol_r1.text = "Proposed Approach: "
    p_sol_r1.font.name = FONT_MAIN
    p_sol_r1.font.size = Pt(9.5)
    p_sol_r1.font.bold = True
    p_sol_r1.font.color.rgb = C_NAVY_HEADING
    p_sol_r2 = p_sol.add_run()
    p_sol_r2.text = "A hardware-efficient programmable toggle-rate control technique that selectively modifies PRPG patterns to match desired scan-shift toggle limits (10%-60% or Bypass) without sacrificing fault coverage or test time."
    p_sol_r2.font.name = FONT_MAIN
    p_sol_r2.font.size = Pt(9)
    p_sol_r2.font.color.rgb = C_TEXT_DARK

    obj_header = tf2.add_paragraph()
    obj_header.space_before = Pt(8)
    obj_hr = obj_header.add_run()
    obj_hr.text = "Main Project Objectives:"
    obj_hr.font.name = FONT_MAIN
    obj_hr.font.size = Pt(10)
    obj_hr.font.bold = True
    obj_hr.font.color.rgb = C_NAVY_SUB

    objectives = [
        ("1. Pseudorandom Pattern Generation:", "Design a parameterizable 16-bit Galois LFSR with autonomous anti-lockup zero-recovery logic."),
        ("2. Programmable Pattern Modification:", "Implement a Dual-Domain Rotating Transition Suppressor (DDRTS) with modulo-16 token ring to eliminate scan starvation."),
        ("3. MIPS32 Scan Application:", "Partition and apply modified vectors to 16 parallel scan chains and serial scan input of synthesizable MIPS32 processor core."),
        ("4. Response Compaction & Analysis:", "Compact test responses via 16-bit Multiple-Input Signature Register (MISR) and evaluate on-chip switching activity, power reduction, and test effectiveness.")
    ]

    for o_title, o_desc in objectives:
        p = tf2.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = "✔ " + o_title + " "
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY_HEADING

        r2 = p.add_run()
        r2.text = o_desc
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(9)
        r2.font.color.rgb = C_TEXT_DARK

    p_val = tf2.add_paragraph()
    p_val.space_before = Pt(10)
    p_val_r1 = p_val.add_run()
    p_val_r1.text = "Target Innovation: "
    p_val_r1.font.name = FONT_MAIN
    p_val_r1.font.size = Pt(9.5)
    p_val_r1.font.bold = True
    p_val_r1.font.color.rgb = C_TEAL
    p_val_r2 = p_val.add_run()
    p_val_r2.text = "Enables arbitrary scan-shift power throttling (down to 10% activity) with zero test clock latency penalty and zero scan chain starvation."
    p_val_r2.font.name = FONT_MAIN
    p_val_r2.font.size = Pt(9)
    p_val_r2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 2: PROPOSED ARCHITECTURE AND WORKING FLOW (COMPACT FLOW DIAGRAM)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s2)

    render_header(s2,
                  "Proposed LBIST Architecture and Methodology",
                  "Compact Testing Flow Diagram & Hardware Working Principle",
                  2)

    # Master Container for Flow Diagram (Clean compact card)
    fd_x = Inches(0.8)
    fd_y = Inches(1.45)
    fd_w = Inches(11.733)
    fd_h = Inches(3.20)

    fd_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, fd_x, fd_y, fd_w, fd_h)
    fd_card.fill.solid()
    fd_card.fill.fore_color.rgb = C_WHITE
    fd_card.line.color.rgb = C_CARD_BORDER
    fd_card.line.width = Pt(1.5)

    # Top Control Unit (Block 1: LBIST Controller)
    ctrl_w = Inches(11.333)
    ctrl_h = Inches(0.80)
    ctrl_x = fd_x + Inches(0.2)
    ctrl_y = fd_y + Inches(0.15)

    ctrl_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, ctrl_x, ctrl_y, ctrl_w, ctrl_h)
    ctrl_box.fill.solid()
    ctrl_box.fill.fore_color.rgb = RGBColor(238, 242, 255) # Light Indigo
    ctrl_box.line.color.rgb = C_ORANGE
    ctrl_box.line.width = Pt(1.5)

    ctb = s2.shapes.add_textbox(ctrl_x + Inches(0.2), ctrl_y + Inches(0.08), ctrl_w - Inches(0.4), ctrl_h - Inches(0.16))
    ctf = ctb.text_frame
    ctf.word_wrap = True
    ctf.margin_top = ctf.margin_bottom = ctf.margin_left = ctf.margin_right = 0
    cp1 = ctf.paragraphs[0]
    cp1.text = "1. LBIST Controller (Member 3 – Gaurav Tiwari)"
    cp1.font.name = FONT_MAIN
    cp1.font.size = Pt(10)
    cp1.font.bold = True
    cp1.font.color.rgb = C_ORANGE
    cp1.alignment = PP_ALIGN.CENTER
    cp2 = ctf.add_paragraph()
    cp2.text = "FSM Master: Initializes test, loads seed, sets target rate (10%-60%/Bypass), orchestrates Shift vs. Capture modes, and clocks test sequence."
    cp2.font.name = FONT_MAIN
    cp2.font.size = Pt(8.5)
    cp2.font.color.rgb = C_TEXT_DARK
    cp2.alignment = PP_ALIGN.CENTER

    # Control Dispatch Downward Arrows (3 small arrows to indicate control dispatch)
    ctrl_arrows = [
        (ctrl_x + Inches(1.5), "rate_sel, seed_load"),
        (ctrl_x + Inches(5.6), "scan_enable, shift/capture clk"),
        (ctrl_x + Inches(9.8), "misr_en, golden_sig")
    ]
    for ax, alabel in ctrl_arrows:
        c_arr = s2.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, ax, ctrl_y + ctrl_h + Inches(0.02), Inches(0.18), Inches(0.22))
        c_arr.fill.solid()
        c_arr.fill.fore_color.rgb = C_ORANGE
        c_arr.line.fill.background()

    # 6 Datapath Pipeline Blocks (Blocks 2 to 7) in a clear Left-to-Right sequence
    flow_y = ctrl_y + ctrl_h + Inches(0.28)
    flow_blocks = [
        ("2. PRPG (LFSR)", "16-Bit Galois LFSR\nPoly: 0xB400, Seed: 0xACE1\nAutonomous Anti-Lockup", C_TEAL, "Member 2"),
        ("3. Pattern Modifier", "DDRTS Suppression Engine\nModulo-16 Token Ring\n10%-60% Fractional Dither", C_TEAL, "Member 2"),
        ("4. MIPS32 Scan Chains", "16 Parallel Scan Chains\nSequential Mux-DFF Insertion\nLoads scan_data[15:0]", C_BLUE, "Member 1"),
        ("5. Response Capture", "MIPS32 Core Execution\nALU, RegFile, PC capture\nFunctional combinational test", C_BLUE, "Member 1"),
        ("6. MISR Compactor", "16-Bit Signature Register\nMultiple-Input Compaction\nCompresses core responses", C_ORANGE, "Member 3"),
        ("7. Signature Analysis", "Golden Signature Comparator\nPass / Fail Status Output\nFault Detection Verification", C_ORANGE, "Member 3")
    ]

    blk_w = Inches(1.68)
    blk_h = Inches(1.65)
    blk_gap = Inches(0.25)
    start_x = fd_x + Inches(0.2)

    for i, (b_title, b_desc, b_color, b_owner) in enumerate(flow_blocks):
        bx = start_x + i * (blk_w + blk_gap)
        bbox = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, flow_y, blk_w, blk_h)
        bbox.fill.solid()
        bbox.fill.fore_color.rgb = C_WHITE
        bbox.line.color.rgb = b_color
        bbox.line.width = Pt(1.5)

        btb = s2.shapes.add_textbox(bx + Inches(0.06), flow_y + Inches(0.08), blk_w - Inches(0.12), blk_h - Inches(0.16))
        btf = btb.text_frame
        btf.word_wrap = True
        btf.margin_top = btf.margin_bottom = btf.margin_left = btf.margin_right = 0

        bp1 = btf.paragraphs[0]
        bp1.text = b_title
        bp1.font.name = FONT_MAIN
        bp1.font.size = Pt(8.5)
        bp1.font.bold = True
        bp1.font.color.rgb = b_color
        bp1.alignment = PP_ALIGN.CENTER

        bp2 = btf.add_paragraph()
        bp2.text = b_desc
        bp2.font.name = FONT_MAIN
        bp2.font.size = Pt(7.5)
        bp2.font.color.rgb = C_TEXT_DARK
        bp2.alignment = PP_ALIGN.CENTER
        bp2.space_before = Pt(3)

        bp3 = btf.add_paragraph()
        bp3.text = f"[{b_owner}]"
        bp3.font.name = FONT_MAIN
        bp3.font.size = Pt(7)
        bp3.font.bold = True
        bp3.font.color.rgb = b_color
        bp3.alignment = PP_ALIGN.CENTER
        bp3.space_before = Pt(3)

        # Draw connecting arrow to next block (between blocks 2->3, 3->4, 4->5, 5->6, 6->7)
        if i < len(flow_blocks) - 1:
            arr_x = bx + blk_w + Inches(0.04)
            arr = s2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arr_x, flow_y + Inches(0.68), Inches(0.17), Inches(0.24))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_BORDER_MID
            arr.line.fill.background()

    # Bottom Container: Working Principle (3-4 concise steps)
    wp_x = Inches(0.8)
    wp_y = Inches(4.82)
    wp_w = Inches(11.733)
    wp_h = Inches(2.35)

    wp_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, wp_x, wp_y, wp_w, wp_h)
    wp_card.fill.solid()
    wp_card.fill.fore_color.rgb = C_WHITE
    wp_card.line.color.rgb = C_NAVY_SUB
    wp_card.line.width = Pt(1.5)

    wptb = s2.shapes.add_textbox(wp_x + Inches(0.2), wp_y + Inches(0.12), wp_w - Inches(0.4), wp_h - Inches(0.24))
    wptf = wptb.text_frame
    wptf.word_wrap = True
    wptf.margin_top = wptf.margin_bottom = wptf.margin_left = wptf.margin_right = 0

    wpp = wptf.paragraphs[0]
    wpp.text = "WORKING PRINCIPLE (4-STEP OPERATING SEQUENCE)"
    wpp.font.name = FONT_MAIN
    wpp.font.size = Pt(11)
    wpp.font.bold = True
    wpp.font.color.rgb = C_NAVY_SUB

    steps = [
        ("Step 1: Test Initialization & Pattern Generation", "The LBIST Controller asserts reset and loads the initial seed (0xACE1). The 16-bit Galois LFSR autonomously advances each clock cycle to generate an exhaustive, pseudo-random bit sequence.", C_TEAL),
        ("Step 2: Toggle-Rate Modification", "The Programmable Pattern Modifier compares consecutive LFSR words against the programmed toggle limit. The modulo-16 token ring cyclically suppresses excess transitions, enforcing target switching activity (10%-60%) with zero scan starvation.", C_TEAL),
        ("Step 3: Scan Application & Response Capture", "During Scan Shift (scan_en = '1'), low-power modified patterns are shifted into the 16 parallel MIPS32 scan chains. Next, the controller pulses a single functional capture clock (scan_en = '0'), latching the combinational ALU/datapath response.", C_BLUE),
        ("Step 4: Response Compaction & Signature Analysis", "Captured responses are shifted out into the 16-bit MISR, which compacts multi-cycle responses into a unique test signature. The Signature Analyzer compares it against the golden reference, asserting PASS/FAIL.", C_ORANGE)
    ]

    for s_title, s_desc, s_color in steps:
        p = wptf.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + s_title + ": "
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9)
        r1.font.bold = True
        r1.font.color.rgb = s_color

        r2 = p.add_run()
        r2.text = s_desc
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 3: EXPERIMENTAL RESULTS, OBSERVATIONS AND CONCLUSION
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s3)

    render_header(s3,
                  "Results, Observations and Conclusion",
                  "Experimental Toggle Rates, Total On-Chip Power Reduction, Vivado Synthesis & Final Takeaways",
                  3)

    # LEFT SECTION: Experimental Results (Table, Synthesis, Chart)
    left_x = Inches(0.8)
    left_w = Inches(5.7)

    # 1. Experimental Toggle Rate Table Container
    tbox_y = Inches(1.45)
    tbox_h = Inches(3.20)
    tbox = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, tbox_y, left_w, tbox_h)
    tbox.fill.solid()
    tbox.fill.fore_color.rgb = C_WHITE
    tbox.line.color.rgb = C_CARD_BORDER
    tbox.line.width = Pt(1.5)

    ttb = s3.shapes.add_textbox(left_x + Inches(0.18), tbox_y + Inches(0.10), left_w - Inches(0.36), Inches(0.32))
    ttf = ttb.text_frame
    tp = ttf.paragraphs[0]
    tp.text = "MEASURED RESULTS: CONVENTIONAL VS. MODIFIED PRPG"
    tp.font.name = FONT_MAIN
    tp.font.size = Pt(9.5)
    tp.font.bold = True
    tp.font.color.rgb = C_NAVY_SUB

    # Results Table
    table_shape = s3.shapes.add_table(8, 5, left_x + Inches(0.12), tbox_y + Inches(0.40), left_w - Inches(0.24), Inches(2.15))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(1.05)
    tbl.columns[1].width = Inches(1.0)
    tbl.columns[2].width = Inches(1.0)
    tbl.columns[3].width = Inches(1.0)
    tbl.columns[4].width = Inches(1.41)

    headers = ["Target", "Conv Word", "Mod Word", "Mod Scan", "Total On-Chip Power"]
    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_SUB
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_MAIN
        p.font.size = Pt(8)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

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
            cell.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 0 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.CENTER
            p.font.name = FONT_MAIN
            p.font.size = Pt(7.5)
            if col_idx == 4 and "Saved" in val:
                p.font.bold = True
                p.font.color.rgb = C_GREEN
            elif col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_NAVY_HEADING
            else:
                p.font.color.rgb = C_TEXT_DARK

    # Clarification note on power
    ntb = s3.shapes.add_textbox(left_x + Inches(0.18), tbox_y + Inches(2.62), left_w - Inches(0.36), Inches(0.48))
    ntf = ntb.text_frame
    ntf.word_wrap = True
    ntf.margin_top = ntf.margin_bottom = ntf.margin_left = ntf.margin_right = 0
    np = ntf.paragraphs[0]
    np.text = "* Power reduction measures Total On-Chip Scan-Shift Power across all core scan chains during testing (not limited to isolated LBIST logic)."
    np.font.name = FONT_MAIN
    np.font.size = Pt(7.2)
    np.font.bold = True
    np.font.color.rgb = C_RED

    # 2. Vivado Hardware Synthesis Results Container
    sbox_y = Inches(4.78)
    sbox_h = Inches(2.35)
    sbox = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, sbox_y, left_w, sbox_h)
    sbox.fill.solid()
    sbox.fill.fore_color.rgb = C_WHITE
    sbox.line.color.rgb = C_BLUE
    sbox.line.width = Pt(1.5)

    stb = s3.shapes.add_textbox(left_x + Inches(0.18), sbox_y + Inches(0.10), left_w - Inches(0.36), Inches(0.30))
    stf = stb.text_frame
    sp = stf.paragraphs[0]
    sp.text = "VIVADO HARDWARE SYNTHESIS (synth_design Complete!)"
    sp.font.name = FONT_MAIN
    sp.font.size = Pt(9.5)
    sp.font.bold = True
    sp.font.color.rgb = C_BLUE

    # Vivado Resource Table
    vtable_shape = s3.shapes.add_table(2, 6, left_x + Inches(0.12), sbox_y + Inches(0.38), left_w - Inches(0.24), Inches(0.70))
    vtbl = vtable_shape.table
    vtbl.columns[0].width = Inches(1.15)
    vtbl.columns[1].width = Inches(0.85)
    vtbl.columns[2].width = Inches(0.85)
    vtbl.columns[3].width = Inches(0.85)
    vtbl.columns[4].width = Inches(0.85)
    vtbl.columns[5].width = Inches(0.89)

    vheaders = ["Run Status", "LUTs", "FFs", "BRAM", "URAM", "DSP"]
    for c_i, vh in enumerate(vheaders):
        cell = vtbl.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(238, 242, 255)
        p = cell.text_frame.paragraphs[0]
        p.text = vh
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_MAIN
        p.font.size = Pt(8)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_HEADING

    vvals = ["Complete!", "5,565", "1,287", "0", "0", "0"]
    for c_i, vv in enumerate(vvals):
        cell = vtbl.cell(1, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE
        p = cell.text_frame.paragraphs[0]
        p.text = vv
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_MAIN
        p.font.size = Pt(8.5)
        p.font.bold = True
        if c_i == 0:
            p.font.color.rgb = C_GREEN
        elif c_i in [1, 2]:
            p.font.color.rgb = C_BLUE
        else:
            p.font.color.rgb = C_TEXT_MUTED

    sntb = s3.shapes.add_textbox(left_x + Inches(0.18), sbox_y + Inches(1.18), left_w - Inches(0.36), Inches(1.05))
    sntf = sntb.text_frame
    sntf.word_wrap = True
    sntf.margin_top = sntf.margin_bottom = sntf.margin_left = sntf.margin_right = 0
    snp1 = sntf.paragraphs[0]
    snp1.text = "• Top-Level Synthesizability: Fully synthesized MIPS32 processor with inserted scan chains and LBIST controller in Vivado (synth_1 complete)."
    snp1.font.name = FONT_MAIN
    snp1.font.size = Pt(8)
    snp1.font.color.rgb = C_TEXT_DARK

    snp2 = sntf.add_paragraph()
    snp2.text = "• Logic Resource Overhead: Pure standard cell / slice implementation (5,565 LUTs, 1,287 FFs); zero dedicated BRAM or DSP blocks consumed."
    snp2.font.name = FONT_MAIN
    snp2.font.size = Pt(8)
    snp2.font.color.rgb = C_TEXT_DARK
    snp2.space_before = Pt(3)

    # RIGHT SECTION: Key Observations, Fault Coverage Status & Conclusion
    right_x = Inches(6.833)
    right_w = Inches(5.7)

    # 1. Total On-Chip Power Reduction Graph (Top)
    chart_y = Inches(1.45)
    chart_h = Inches(2.65)
    chart_path = "Analysis/slide3_compact_chart.png"
    if not os.path.exists(chart_path):
        chart_path = "Analysis/slide3_light_chart.png"
    if os.path.exists(chart_path):
        s3.shapes.add_picture(chart_path, right_x, chart_y, width=right_w, height=chart_h)

    # 2. Key Observations & Conclusion Container (Bottom)
    cbox_y = Inches(4.20)
    cbox_h = Inches(2.93)
    cbox = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, cbox_y, right_w, cbox_h)
    cbox.fill.solid()
    cbox.fill.fore_color.rgb = C_WHITE
    cbox.line.color.rgb = C_GREEN
    cbox.line.width = Pt(1.5)

    ctb = s3.shapes.add_textbox(right_x + Inches(0.2), cbox_y + Inches(0.12), right_w - Inches(0.4), cbox_h - Inches(0.24))
    ctf = ctb.text_frame
    ctf.word_wrap = True
    ctf.margin_top = ctf.margin_bottom = ctf.margin_left = ctf.margin_right = 0

    cp = ctf.paragraphs[0]
    cp.text = "KEY OBSERVATIONS, TEST EFFECTIVENESS & FUTURE WORK"
    cp.font.name = FONT_MAIN
    cp.font.size = Pt(10)
    cp.font.bold = True
    cp.font.color.rgb = C_GREEN

    concl_points = [
        ("Switching Activity & Power Control", "Pattern modifier tightly tracks target limits (10.29% measured vs 10.00% target). Slashes total on-chip scan-shift power by up to 84.35%, eliminating thermal hotspots and preventing false IR-drop delay faults."),
        ("MIPS32 Core & Scan Architecture Role", "Provides full controllability and observability of internal pipeline registers. Dual-mode scan multiplexers enable seamless shift ingestion and full-speed single-clock functional capture."),
        ("MISR Compaction & Test Effectiveness", "Continuous single-cycle pattern throughput (0 delay overhead) avoids test-time inflation. The 16-bit MISR compacts responses into a golden signature for rapid GO/NO-GO classification."),
        ("Fault Coverage Evaluation Status", "Single stuck-at fault injection mechanism architecturally implemented. Comprehensive multi-pattern fault coverage grading is scheduled for joint multi-module integration [Pending Full System Integration]."),
        ("Future Scope & Next Milestones", "1) Perform closed-loop stuck-at and transition fault simulation; 2) Resolve I/O pin constraints for place-and-route (impl_1 closure); 3) Post-layout timing & physical power characterization on Xilinx Artix-7.")
    ]

    for c_title, c_desc in concl_points:
        p = ctf.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = "✔ " + c_title + ": "
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(8.2)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY_HEADING

        r2 = p.add_run()
        r2.text = c_desc
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(7.8)
        r2.font.color.rgb = C_TEXT_DARK

    # Save presentation
    output_filename = "VL405_LBIST_Project_Presentation.pptx"
    prs.save(output_filename)
    print(f"[SUCCESS] Academic 3-Slide Presentation compiled to: {output_filename}")

if __name__ == "__main__":
    build_presentation()
