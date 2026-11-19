import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.50)
    blank_layout = prs.slide_layouts[6]

    # Typography & Palette
    FONT_MAIN = "Arial"
    C_NAVY_HEADING = RGBColor(23, 50, 77)    # #17324D
    C_NAVY_SUB     = RGBColor(82, 103, 125)  # #52677D
    C_TEXT_DARK    = RGBColor(30, 41, 59)    # #1E293B
    C_TEXT_MUTED   = RGBColor(100, 116, 139) # #64748B
    C_BLUE         = RGBColor(37, 99, 235)   # #2563EB
    C_WHITE        = RGBColor(255, 255, 255)
    C_BG_PAGE      = RGBColor(250, 252, 255) # Light bright canvas
    C_CARD_BORDER  = RGBColor(226, 232, 240) # Slate border
    C_BORDER_MID   = RGBColor(203, 213, 225)
    
    # Pill colors
    C_PILL_BLUE    = RGBColor(30, 58, 138)   # Deep Blue
    C_PILL_RED     = RGBColor(185, 28, 28)   # Deep Red
    C_PILL_GREEN   = RGBColor(21, 128, 61)   # Forest Green
    C_PILL_PURPLE  = RGBColor(109, 40, 217)  # Violet
    C_PILL_ORANGE  = RGBColor(194, 65, 12)   # Dark Orange

    def apply_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG_PAGE
        bg.line.fill.background()
        return bg

    def render_header(slide, title_text, subtitle_text, slide_num):
        left_m = Inches(0.8)
        # Vertical accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_m, Inches(0.36), Inches(0.08), Inches(0.56))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_BLUE
        bar.line.fill.background()

        # Title & Subtitle box
        tb = slide.shapes.add_textbox(left_m + Inches(0.18), Inches(0.32), Inches(10.6), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p1 = tf.paragraphs[0]
        p1.text = title_text
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(21)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY_HEADING

        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_NAVY_SUB
        p2.space_before = Pt(3)

        # Page Number
        ptb = slide.shapes.add_textbox(Inches(11.8), Inches(0.35), Inches(0.73), Inches(0.35))
        ptf = ptb.text_frame
        ptf.margin_top = ptf.margin_bottom = ptf.margin_left = ptf.margin_right = 0
        pp = ptf.paragraphs[0]
        pp.text = f"{slide_num} / 3"
        pp.alignment = PP_ALIGN.RIGHT
        pp.font.name = FONT_MAIN
        pp.font.size = Pt(11)
        pp.font.bold = True
        pp.font.color.rgb = C_NAVY_SUB

        # Divider line
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_m, Inches(1.24), Inches(11.733), Inches(0.01))
        div.fill.solid()
        div.fill.fore_color.rgb = RGBColor(226, 232, 240)
        div.line.fill.background()

    def add_pill_badge(slide, x, y, w, h, text, color):
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        pill.fill.solid()
        pill.fill.fore_color.rgb = color
        pill.line.fill.background()
        tf = pill.text_frame
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_MAIN
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        return pill

    # =========================================================================
    # SLIDE 1: INTRODUCTION AND PROJECT OVERVIEW
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s1)

    render_header(s1,
                  "Low-Power Scan-Based LBIST Using MIPS32 Architecture",
                  "VL405 — Design for Testability (DFT) Laboratory Project",
                  1)

    # 3 Team Member Cards
    team_data = [
        ("Harshitha Modekurty (B23272)", "MIPS32 Core & Scan Architecture",
         RGBColor(239, 246, 255), RGBColor(191, 219, 254), C_NAVY_HEADING, C_BLUE),
        ("Nishi Kumari (B24495)", "PRPG & Toggle-Rate Control",
         RGBColor(240, 253, 250), RGBColor(153, 246, 228), RGBColor(19, 78, 74), RGBColor(13, 148, 136)),
        ("Gaurav Tiwari (B24483)", "LBIST Controller & Fault Analysis",
         RGBColor(255, 247, 237), RGBColor(254, 215, 170), RGBColor(124, 45, 18), RGBColor(234, 88, 12))
    ]

    card_y = Inches(1.36)
    card_h = Inches(0.78)
    card_w = Inches(3.75)
    gap = Inches(0.24)
    start_x = Inches(0.8)

    for i, (name, role, bg_col, border_col, text_col, sub_col) in enumerate(team_data):
        cx = start_x + i * (card_w + gap)
        cbox = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_w, card_h)
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = bg_col
        cbox.line.color.rgb = border_col
        cbox.line.width = Pt(1.5)

        tb = s1.shapes.add_textbox(cx + Inches(0.15), card_y + Inches(0.10), card_w - Inches(0.3), card_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p1 = tf.paragraphs[0]
        p1.text = name
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(10.5)
        p1.font.bold = True
        p1.font.color.rgb = text_col

        p2 = tf.add_paragraph()
        p2.text = role
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(9)
        p2.font.bold = True
        p2.font.color.rgb = sub_col
        p2.space_before = Pt(3)

    # Full-width INTRODUCTION Strip
    intro_y = Inches(2.26)
    intro_h = Inches(0.68)
    intro_w = Inches(11.733)
    ibox = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, intro_y, intro_w, intro_h)
    ibox.fill.solid()
    ibox.fill.fore_color.rgb = C_WHITE
    ibox.line.color.rgb = C_CARD_BORDER
    ibox.line.width = Pt(1.5)

    add_pill_badge(s1, start_x + Inches(0.15), intro_y + Inches(0.14), Inches(1.6), Inches(0.40), "INTRODUCTION", C_BLUE)

    itb = s1.shapes.add_textbox(start_x + Inches(1.92), intro_y + Inches(0.12), intro_w - Inches(2.08), Inches(0.45))
    itf = itb.text_frame
    itf.word_wrap = True
    itf.margin_top = itf.margin_bottom = itf.margin_left = itf.margin_right = 0
    ip = itf.paragraphs[0]
    ip.text = "Logic Built-In Self-Test (LBIST) enables on-chip testing using pseudorandom patterns and response compaction. Scan-based testing improves controllability and observability for complex designs such as a MIPS32 processor."
    ip.font.name = FONT_MAIN
    ip.font.size = Pt(8.8)
    ip.font.color.rgb = C_TEXT_DARK

    # Bottom Two Balanced Sections
    sec_y = Inches(3.06)
    sec_h = Inches(4.18)

    # PROBLEM STATEMENT (Left Card)
    prob_w = Inches(4.30)
    pbox = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, sec_y, prob_w, sec_h)
    pbox.fill.solid()
    pbox.fill.fore_color.rgb = RGBColor(255, 245, 245)
    pbox.line.color.rgb = RGBColor(254, 202, 202)
    pbox.line.width = Pt(1.5)

    add_pill_badge(s1, start_x + Inches(0.18), sec_y + Inches(0.14), Inches(2.1), Inches(0.34), "PROBLEM STATEMENT", C_PILL_RED)

    ptb = s1.shapes.add_textbox(start_x + Inches(0.22), sec_y + Inches(0.58), prob_w - Inches(0.44), sec_h - Inches(0.70))
    ptf = ptb.text_frame
    ptf.word_wrap = True
    ptf.margin_top = ptf.margin_bottom = ptf.margin_left = ptf.margin_right = 0

    prob_items = [
        ("High switching activity:", " Conventional LFSR patterns can produce frequent transitions during scan shifting."),
        ("Power impact:", " High scan-shift activity increases dynamic power and may cause IR-drop and delay variation."),
        ("Thermal stress:", " Excessive test activity can create local heating and false test failures.")
    ]

    for i, (hd, body) in enumerate(prob_items):
        p = ptf.add_paragraph()
        if i > 0:
            p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = hd
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = C_PILL_RED

        r2 = p.add_run()
        r2.text = body
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(8.8)
        r2.font.color.rgb = C_TEXT_DARK

    # PROPOSED APPROACH & OBJECTIVES (Right Card - Unified Across All 3 Pillars)
    prop_x = start_x + prob_w + Inches(0.24)
    prop_w = intro_w - prob_w - Inches(0.24)

    prbox = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, prop_x, sec_y, prop_w, sec_h)
    prbox.fill.solid()
    prbox.fill.fore_color.rgb = RGBColor(240, 253, 244)
    prbox.line.color.rgb = RGBColor(187, 247, 208)
    prbox.line.width = Pt(1.5)

    add_pill_badge(s1, prop_x + Inches(0.18), sec_y + Inches(0.14), Inches(3.2), Inches(0.34), "PROPOSED APPROACH & OBJECTIVES", C_PILL_GREEN)

    # Core Concept Summary Box (Unified Solution)
    concept_y = sec_y + Inches(0.54)
    concept_h = Inches(0.56)
    c_inner = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, prop_x + Inches(0.18), concept_y, prop_w - Inches(0.36), concept_h)
    c_inner.fill.solid()
    c_inner.fill.fore_color.rgb = C_WHITE
    c_inner.line.color.rgb = RGBColor(209, 250, 229)
    c_inner.line.width = Pt(1)

    ctb = s1.shapes.add_textbox(prop_x + Inches(0.26), concept_y + Inches(0.08), prop_w - Inches(0.52), concept_h - Inches(0.16))
    ctf = ctb.text_frame
    ctf.word_wrap = True
    ctf.margin_top = ctf.margin_bottom = ctf.margin_left = ctf.margin_right = 0
    cp = ctf.paragraphs[0]
    cp.text = "Unified Strategy: Integrate activity-throttled LFSR pattern generation with balanced MIPS32 scan chains and autonomous MISR response compaction for complete on-chip self-test."
    cp.font.name = FONT_MAIN
    cp.font.size = Pt(8.6)
    cp.font.bold = True
    cp.font.color.rgb = C_NAVY_HEADING

    # 4 Comprehensive Objectives Across All 3 Pillars + Evaluation
    pillars = [
        ("MIPS32 Core & Balanced Scan Architecture:",
         " Partition 1,024 processor state registers into 4 balanced scan chains (256 cells each) to maximize test controllability and observability while minimizing shift latency.",
         C_BLUE),
        ("PRPG & Programmable Toggle-Rate Control:",
         " Implement a 16-bit LFSR PRPG with DDRTS pattern modification to dynamically regulate scan-shift transitions (10%–60% targets), eliminating IR-drop and thermal stress.",
         C_PILL_GREEN),
        ("Autonomous LBIST Controller & MISR Compactor:",
         " Coordinate 4-phase test execution (Reset → Shift → Capture → Compact) via an on-chip FSM, compacting responses into a 16-bit MISR signature for autonomous PASS/FAIL evaluation.",
         C_PILL_ORANGE),
        ("Full-System Verification & Power Closure:",
         " Evaluate scan toggle activity, verify 100% stuck-at fault coverage (2,048 faults), and achieve complete FPGA synthesis closure on AMD Xilinx Artix-7.",
         C_PILL_PURPLE)
    ]

    obj_start_y = concept_y + concept_h + Inches(0.12)
    obj_gap = Inches(0.70)

    for i, (hd, body, col) in enumerate(pillars):
        oy = obj_start_y + i * obj_gap

        # Number Badge
        nb = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, prop_x + Inches(0.20), oy, Inches(0.32), Inches(0.32))
        nb.fill.solid()
        nb.fill.fore_color.rgb = C_WHITE
        nb.line.color.rgb = col
        nb.line.width = Pt(1.5)
        np_ = nb.text_frame.paragraphs[0]
        np_.text = str(i + 1)
        np_.alignment = PP_ALIGN.CENTER
        np_.font.name = FONT_MAIN
        np_.font.size = Pt(9.5)
        np_.font.bold = True
        np_.font.color.rgb = col

        # Text Box
        otb = s1.shapes.add_textbox(prop_x + Inches(0.62), oy - Inches(0.04), prop_w - Inches(0.80), Inches(0.64))
        otf = otb.text_frame
        otf.word_wrap = True
        otf.margin_top = otf.margin_bottom = otf.margin_left = otf.margin_right = 0
        p = otf.paragraphs[0]
        r1 = p.add_run()
        r1.text = hd
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = col

        r2 = p.add_run()
        r2.text = body
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(7.8)
        r2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 2: PROPOSED ARCHITECTURE AND METHODOLOGY
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s2)

    render_header(s2,
                  "Proposed LBIST Architecture and Methodology",
                  "Overall test flow and hardware working principle",
                  2)

    # Top Flowchart Container
    arch_y = Inches(1.36)
    arch_h = Inches(3.22)
    arch_w = Inches(11.733)
    abox = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, arch_y, arch_w, arch_h)
    abox.fill.solid()
    abox.fill.fore_color.rgb = C_WHITE
    abox.line.color.rgb = C_CARD_BORDER
    abox.line.width = Pt(1.5)

    add_pill_badge(s2, start_x + Inches(0.18), arch_y + Inches(0.12), Inches(2.7), Inches(0.34), "OVERALL LBIST ARCHITECTURE", C_BLUE)

    # LBIST Controller (FSM) Top Box
    fsm_w = Inches(3.50)
    fsm_h = Inches(0.52)
    fsm_x = start_x + (arch_w - fsm_w) / 2
    fsm_y = arch_y + Inches(0.40)

    fsm_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, fsm_x, fsm_y, fsm_w, fsm_h)
    fsm_box.fill.solid()
    fsm_box.fill.fore_color.rgb = RGBColor(245, 243, 255)
    fsm_box.line.color.rgb = RGBColor(196, 181, 253)
    fsm_box.line.width = Pt(1.5)

    ftb = s2.shapes.add_textbox(fsm_x, fsm_y + Inches(0.08), fsm_w, Inches(0.36))
    ftf = ftb.text_frame
    ftf.margin_top = ftf.margin_bottom = ftf.margin_left = ftf.margin_right = 0
    fp = ftf.paragraphs[0]
    fp.text = "LBIST Controller (FSM)"
    fp.alignment = PP_ALIGN.CENTER
    fp.font.name = FONT_MAIN
    fp.font.size = Pt(11)
    fp.font.bold = True
    fp.font.color.rgb = C_PILL_PURPLE

    # Central drop line from Controller to bus
    drop_x = start_x + arch_w / 2
    drop_y1 = fsm_y + fsm_h
    bus_y = drop_y1 + Inches(0.32)

    vline = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, drop_x - Inches(0.01), drop_y1, Inches(0.02), Inches(0.32))
    vline.fill.solid()
    vline.fill.fore_color.rgb = C_PILL_PURPLE
    vline.line.fill.background()

    # Horizontal Purple Control Bus
    bus_x1 = start_x + Inches(1.15)
    bus_x2 = start_x + arch_w - Inches(1.18)
    bus_w = bus_x2 - bus_x1

    hbus = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, bus_x1, bus_y, bus_w, Inches(0.02))
    hbus.fill.solid()
    hbus.fill.fore_color.rgb = C_PILL_PURPLE
    hbus.line.fill.background()

    # 4 Drop points from Bus to Datapath Blocks
    drop_targets = [
        (bus_x1 - Inches(0.06), "seed / enable"),
        (start_x + Inches(2.99), "target rate"),
        (start_x + Inches(5.04), "scan / test clock"),
        (start_x + Inches(9.20), "MISR enable")
    ]

    for dx, label in drop_targets:
        darr = s2.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, dx, bus_y, Inches(0.12), Inches(0.24))
        darr.fill.solid()
        darr.fill.fore_color.rgb = C_PILL_PURPLE
        darr.line.fill.background()

        lbl_tb = s2.shapes.add_textbox(dx - Inches(0.74), bus_y - Inches(0.24), Inches(1.60), Inches(0.22))
        lbl_tf = lbl_tb.text_frame
        lbl_tf.margin_top = lbl_tf.margin_bottom = lbl_tf.margin_left = lbl_tf.margin_right = 0
        lbl_p = lbl_tf.paragraphs[0]
        lbl_p.text = label
        lbl_p.alignment = PP_ALIGN.CENTER
        lbl_p.font.name = FONT_MAIN
        lbl_p.font.size = Pt(7.5)
        lbl_p.font.bold = True
        lbl_p.font.color.rgb = C_PILL_PURPLE

    # 6 Datapath Blocks (Horizontal Flow)
    dp_y = bus_y + Inches(0.26)
    dp_h = Inches(0.95)

    blocks = [
        ("PRPG\n(LFSR)", "Pseudorandom\npatterns", RGBColor(240, 253, 244), RGBColor(167, 243, 208), C_PILL_GREEN),
        ("Pattern\nModifier", "Toggle-rate\ncontrol", RGBColor(240, 253, 250), RGBColor(153, 246, 228), RGBColor(13, 148, 136)),
        ("MIPS32\nScan Chains", "Circuit under\ntest (CUT)", RGBColor(239, 246, 255), RGBColor(191, 219, 254), C_BLUE),
        ("Response\nCapture", "Capture test\nresponse", RGBColor(255, 247, 237), RGBColor(254, 215, 170), RGBColor(234, 88, 12)),
        ("MISR\n(16-bit)", "Response\ncompaction", RGBColor(255, 251, 235), RGBColor(253, 230, 138), RGBColor(202, 138, 4)),
        ("Signature\nAnalysis", "PASS / FAIL\nstatus", RGBColor(245, 243, 255), RGBColor(196, 181, 253), C_PILL_PURPLE)
    ]

    bw = Inches(1.66)
    arr_w = Inches(0.20)
    dp_start_x = start_x + Inches(0.28)
    dp_gap = (arch_w - Inches(0.56) - (len(blocks) * bw) - ((len(blocks) - 1) * arr_w)) / (len(blocks) - 1)

    for i, (hd, sub, bg, brd, txt_col) in enumerate(blocks):
        bx = dp_start_x + i * (bw + arr_w + dp_gap)
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, dp_y, bw, dp_h)
        box.fill.solid()
        box.fill.fore_color.rgb = bg
        box.line.color.rgb = brd
        box.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(bx + Inches(0.04), dp_y + Inches(0.06), bw - Inches(0.08), dp_h - Inches(0.12))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p1 = tf.paragraphs[0]
        p1.text = hd
        p1.alignment = PP_ALIGN.CENTER
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = txt_col

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.alignment = PP_ALIGN.CENTER
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(7)
        p2.font.color.rgb = C_TEXT_MUTED
        p2.space_before = Pt(2)

        # Flow Arrow to next block
        if i < len(blocks) - 1:
            arr_x = bx + bw + dp_gap / 2
            arr = s2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arr_x, dp_y + Inches(0.38), arr_w, Inches(0.22))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_BLUE
            arr.line.fill.background()

    # Bottom Two Flow Cards
    bot_y = Inches(4.70)
    bot_h = Inches(2.54)
    bot_w = Inches(5.70)

    # 1. WORKING PRINCIPLE (Left Card)
    wp_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, bot_y, bot_w, bot_h)
    wp_box.fill.solid()
    wp_box.fill.fore_color.rgb = C_WHITE
    wp_box.line.color.rgb = C_CARD_BORDER
    wp_box.line.width = Pt(1.5)

    add_pill_badge(s2, start_x + Inches(0.18), bot_y + Inches(0.12), Inches(2.2), Inches(0.34), "WORKING PRINCIPLE", C_BLUE)

    wp_steps = [
        ("Initialize", "Reset LBIST and load the PRPG seed."),
        ("Generate & modify", "Generate patterns and regulate toggle rate."),
        ("Scan & capture", "Shift patterns into scan chains and capture response."),
        ("Compact & analyze", "MISR compacts response; compare final signature.")
    ]

    wp_start_y = bot_y + Inches(0.56)
    step_gap = Inches(0.46)

    for i, (stitle, sdesc) in enumerate(wp_steps):
        sy = wp_start_y + i * step_gap

        # Step badge
        sb = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x + Inches(0.20), sy, Inches(0.30), Inches(0.30))
        sb.fill.solid()
        sb.fill.fore_color.rgb = C_BLUE
        sb.line.fill.background()
        sp_ = sb.text_frame.paragraphs[0]
        sp_.text = str(i + 1)
        sp_.alignment = PP_ALIGN.CENTER
        sp_.font.name = FONT_MAIN
        sp_.font.size = Pt(8.5)
        sp_.font.bold = True
        sp_.font.color.rgb = C_WHITE

        # Step text
        stb = s2.shapes.add_textbox(start_x + Inches(0.58), sy - Inches(0.02), bot_w - Inches(0.70), Inches(0.36))
        stf = stb.text_frame
        stf.word_wrap = True
        stf.margin_top = stf.margin_bottom = stf.margin_left = stf.margin_right = 0
        p = stf.paragraphs[0]
        r1 = p.add_run()
        r1.text = stitle + "   "
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY_HEADING

        r2 = p.add_run()
        r2.text = sdesc
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(8)
        r2.font.color.rgb = C_TEXT_DARK

    # 2. KEY COMPONENTS (Right Card)
    kc_x = start_x + bot_w + Inches(0.333)
    kc_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, kc_x, bot_y, bot_w, bot_h)
    kc_box.fill.solid()
    kc_box.fill.fore_color.rgb = C_CARD_BORDER
    kc_box.line.width = Pt(1.5)

    add_pill_badge(s2, kc_x + Inches(0.18), bot_y + Inches(0.12), Inches(2.0), Inches(0.34), "KEY COMPONENTS", C_BLUE)

    comp_items = [
        ("LBIST Controller", "Test sequencing and control signals"),
        ("PRPG + Modifier", "Pattern generation and toggle-rate control"),
        ("MIPS32 Scan Chains", "Apply test patterns to the CUT"),
        ("MISR + Analyzer", "Response compaction and PASS/FAIL")
    ]

    for i, (cname, cdesc) in enumerate(comp_items):
        cy = wp_start_y + i * step_gap
        ctb = s2.shapes.add_textbox(kc_x + Inches(0.20), cy, bot_w - Inches(0.40), Inches(0.36))
        ctf = ctb.text_frame
        ctf.word_wrap = True
        ctf.margin_top = ctf.margin_bottom = ctf.margin_left = ctf.margin_right = 0
        p = ctf.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{cname:<22}"
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY_HEADING

        r2 = p.add_run()
        r2.text = cdesc
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(8)
        r2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # =========================================================================
    # SLIDE 3: COMPILED PROJECT RESULTS & PERFORMANCE ANALYSIS (ALL MODULES)
    # Anonymous: Zero names mentioned (already on Slide 1). Rich compiled results.
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s3)

    render_header(s3,
                  "Compiled Project Results & Performance Analysis",
                  "Comprehensive DFT evaluation: MIPS32 scan architecture, PRPG toggle control, 100% fault coverage & Vivado synthesis",
                  3)

    col_w = Inches(5.70)
    left_x = Inches(0.80)
    right_x = Inches(6.833)

    # -------------------------------------------------------------------------
    # CARD 1 (Top Left): PRPG & TOGGLE-RATE CONTROL RESULTS
    # -------------------------------------------------------------------------
    c1_y = Inches(1.34)
    c1_h = Inches(2.68)
    box1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, c1_y, col_w, c1_h)
    box1.fill.solid()
    box1.fill.fore_color.rgb = C_WHITE
    box1.line.color.rgb = RGBColor(167, 243, 208)
    box1.line.width = Pt(1.5)

    add_pill_badge(s3, left_x + Inches(0.18), c1_y + Inches(0.10), Inches(3.6), Inches(0.28), "PRPG & TOGGLE-RATE CONTROL RESULTS", C_PILL_GREEN)

    # LFSR Characteristic Polynomial Box
    eq_tb = s3.shapes.add_textbox(left_x + Inches(0.16), c1_y + Inches(0.40), col_w - Inches(0.32), Inches(0.24))
    eq_tf = eq_tb.text_frame
    eq_tf.word_wrap = True
    eq_tf.margin_top = eq_tf.margin_bottom = eq_tf.margin_left = eq_tf.margin_right = 0
    eq_p = eq_tf.paragraphs[0]
    r_eq_lbl = eq_p.add_run()
    r_eq_lbl.text = "LFSR Polynomial: "
    r_eq_lbl.font.name = FONT_MAIN
    r_eq_lbl.font.size = Pt(7.6)
    r_eq_lbl.font.bold = True
    r_eq_lbl.font.color.rgb = C_NAVY_HEADING

    r_eq_val = eq_p.add_run()
    r_eq_val.text = "P(x) = x¹⁶ + x¹⁴ + x¹³ + x¹¹ + 1   [Mask: 0xB400, Seed: 0xACE1]"
    r_eq_val.font.name = FONT_MAIN
    r_eq_val.font.size = Pt(7.5)
    r_eq_val.font.bold = True
    r_eq_val.font.color.rgb = C_BLUE

    # Table (8 rows x 5 cols)
    table_shape = s3.shapes.add_table(8, 5, left_x + Inches(0.14), c1_y + Inches(0.66), col_w - Inches(0.28), Inches(1.64))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(1.05)
    tbl.columns[1].width = Inches(1.0)
    tbl.columns[2].width = Inches(1.0)
    tbl.columns[3].width = Inches(1.0)
    tbl.columns[4].width = Inches(1.37)

    headers = ["Target", "Conv. word", "Mod. word", "Mod. scan", "Power saved"]
    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(15, 37, 68)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_MAIN
        p.font.size = Pt(7.2)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    table_data = [
        ("Bypass", "48.50%", "49.00%", "38.44%", "Baseline"),
        ("10%", "54.04%", "10.29%", "8.67%", "84.35%"),
        ("20%", "55.00%", "19.92%", "9.92%", "81.76%"),
        ("30%", "49.54%", "29.88%", "17.31%", "64.64%"),
        ("40%", "47.79%", "36.21%", "18.65%", "63.85%"),
        ("50%", "48.33%", "44.08%", "18.40%", "60.33%"),
        ("60%", "49.54%", "49.13%", "30.98%", "37.44%")
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
            p.font.size = Pt(7.0)
            if col_idx == 4 and "%" in val:
                p.font.bold = True
                p.font.color.rgb = C_PILL_GREEN
            elif col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_NAVY_HEADING
            else:
                p.font.color.rgb = C_TEXT_DARK

    # Summary note below table
    n1_tb = s3.shapes.add_textbox(left_x + Inches(0.16), c1_y + Inches(2.34), col_w - Inches(0.32), Inches(0.28))
    n1_tf = n1_tb.text_frame
    n1_tf.word_wrap = True
    n1_tf.margin_top = n1_tf.margin_bottom = n1_tf.margin_left = n1_tf.margin_right = 0
    np1 = n1_tf.paragraphs[0]
    np1.text = "• Peak reduction: 84.35% total scan power cut • Core logic: 82 LUTs, 57 FFs • Zero-lockup over 5,000 cycles."
    np1.font.name = FONT_MAIN
    np1.font.size = Pt(6.8)
    np1.font.color.rgb = C_TEXT_MUTED

    # -------------------------------------------------------------------------
    # CARD 2 (Bottom Left): FULL-SYSTEM FPGA SYNTHESIS & POWER CLOSURE
    # -------------------------------------------------------------------------
    c2_y = Inches(4.12)
    c2_h = Inches(2.38)
    box2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, c2_y, col_w, c2_h)
    box2.fill.solid()
    box2.fill.fore_color.rgb = C_WHITE
    box2.line.color.rgb = C_CARD_BORDER
    box2.line.width = Pt(1.5)

    add_pill_badge(s3, left_x + Inches(0.18), c2_y + Inches(0.10), Inches(3.6), Inches(0.28), "INTEGRATED FPGA SYNTHESIS (VIVADO)", C_PILL_BLUE)

    vmetrics = [
        ("Run status", "Complete", C_PILL_GREEN),
        ("LUTs", "5,565 (26.8%)", C_PILL_BLUE),
        ("Flip-flops", "1,287 (3.1%)", C_PILL_BLUE),
        ("BRAM / DSP", "0 / 0 / 0", C_TEXT_DARK)
    ]
    vm_w = Inches(1.24)
    vm_h = Inches(0.68)
    vm_gap = Inches(0.12)
    vm_start_x = left_x + Inches(0.16)
    vm_y = c2_y + Inches(0.42)

    for idx, (m_lbl, m_val, m_col) in enumerate(vmetrics):
        mb = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, vm_start_x + idx * (vm_w + vm_gap), vm_y, vm_w, vm_h)
        mb.fill.solid()
        mb.fill.fore_color.rgb = RGBColor(248, 250, 252)
        mb.line.color.rgb = C_BORDER_MID
        mb.line.width = Pt(1)

        mbtf = mb.text_frame
        mbtf.word_wrap = True
        mbtf.margin_top = mbtf.margin_bottom = mbtf.margin_left = mbtf.margin_right = 0
        mp1 = mbtf.paragraphs[0]
        mp1.text = m_lbl
        mp1.alignment = PP_ALIGN.CENTER
        mp1.font.name = FONT_MAIN
        mp1.font.size = Pt(6.8)
        mp1.font.color.rgb = C_TEXT_MUTED

        mp2 = mbtf.add_paragraph()
        mp2.text = m_val
        mp2.alignment = PP_ALIGN.CENTER
        mp2.font.name = FONT_MAIN
        mp2.font.size = Pt(9.2)
        mp2.font.bold = True
        mp2.font.color.rgb = m_col
        mp2.space_before = Pt(2)

    sntb = s3.shapes.add_textbox(left_x + Inches(0.18), c2_y + Inches(1.16), col_w - Inches(0.36), Inches(1.16))
    sntf = sntb.text_frame
    sntf.word_wrap = True
    sntf.margin_top = sntf.margin_bottom = sntf.margin_left = sntf.margin_right = 0

    syn_bullets = [
        ("Unified SoC Integration:", " Successfully integrates MIPS32 CPU Core, 4 Scan Chains, 16-bit PRPG Modifier, and LBIST Controller + MISR into a single synthesizable top entity."),
        ("Resource Efficiency:", " Synthesized on AMD Xilinx Artix-7 (xc7a35tcsg324-1) with 5,565 LUTs, 1,287 FFs, and 0 BRAM/DSP blocks (pure distributed logic implementation)."),
        ("Vivado Dynamic Power Scaling:", " Activity-driven power analysis shows dynamic chip power dropping from 83 mW (bypass) to 59 mW (10% target), saving 28.9% chip-level dynamic power."),
        ("Clocking & Reset Design:", " Single synchronous 50 MHz clock domain with active-low reset and zero inferred latches across all sequential elements.")
    ]

    for i, (hd, body) in enumerate(syn_bullets):
        p = sntf.add_paragraph()
        if i > 0:
            p.space_before = Pt(2)
        r1 = p.add_run()
        r1.text = "• " + hd
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(7.3)
        r1.font.bold = True
        r1.font.color.rgb = C_PILL_BLUE

        r2 = p.add_run()
        r2.text = body
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(7.0)
        r2.font.color.rgb = C_TEXT_DARK

    # -------------------------------------------------------------------------
    # CARD 3 (Top Right): MIPS32 CORE & SCAN CHAIN ARCHITECTURE RESULTS
    # -------------------------------------------------------------------------
    c3_y = Inches(1.34)
    c3_h = Inches(2.68)
    box3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, c3_y, col_w, c3_h)
    box3.fill.solid()
    box3.fill.fore_color.rgb = C_WHITE
    box3.line.color.rgb = RGBColor(191, 219, 254)
    box3.line.width = Pt(1.5)

    add_pill_badge(s3, right_x + Inches(0.18), c3_y + Inches(0.10), Inches(3.8), Inches(0.28), "MIPS32 CORE & SCAN ARCHITECTURE RESULTS", C_PILL_BLUE)

    m1_tb = s3.shapes.add_textbox(right_x + Inches(0.20), c3_y + Inches(0.42), col_w - Inches(0.40), c3_h - Inches(0.48))
    m1_tf = m1_tb.text_frame
    m1_tf.word_wrap = True
    m1_tf.margin_top = m1_tf.margin_bottom = m1_tf.margin_left = m1_tf.margin_right = 0

    m1_bullets = [
        ("1,024 Scanned Architectural Flops:", " Exactly 1,024 state bits scanned: 32-bit Program Counter (PC) plus 31 32-bit general-purpose registers (r1–r31); r0 hardwired to zero with no storage overhead."),
        ("4 Balanced Scan Chains:", " State partitioned into 4 balanced chains of 256 flip-flops each; requires exactly 256 shift cycles + 1 capture cycle per vector (1,025 clocks for full load/unload)."),
        ("100% Controllability & Observability:", " Direct sequential scan insertion eliminates sequential feedback depth, providing complete test accessibility to ALU, register file, and control logic."),
        ("FPGA Timing Closure:", " Out-of-context routing completed with +7.291 ns worst setup slack and +0.119 ns hold slack at 50 MHz (20 ns clock) with 0 failing endpoints."),
        ("ISA Instruction Subset:", " Single-cycle execution verified for ALU ops (ADDU, SUBU, AND, OR, XOR, NOR, SLT), Memory (LW, SW), and Control flow (BEQ, BNE, J, JAL).")
    ]

    for i, (hd, body) in enumerate(m1_bullets):
        p = m1_tf.add_paragraph()
        if i > 0:
            p.space_before = Pt(2.5)
        r1 = p.add_run()
        r1.text = "• " + hd
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(7.4)
        r1.font.bold = True
        r1.font.color.rgb = C_BLUE

        r2 = p.add_run()
        r2.text = body
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(7.0)
        r2.font.color.rgb = C_TEXT_DARK

    # -------------------------------------------------------------------------
    # CARD 4 (Bottom Right): LBIST CONTROLLER, MISR & FAULT COVERAGE ANALYSIS
    # -------------------------------------------------------------------------
    c4_y = Inches(4.12)
    c4_h = Inches(2.38)
    box4 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, c4_y, col_w, c4_h)
    box4.fill.solid()
    box4.fill.fore_color.rgb = C_WHITE
    box4.line.color.rgb = RGBColor(254, 215, 170)
    box4.line.width = Pt(1.5)

    add_pill_badge(s3, right_x + Inches(0.18), c4_y + Inches(0.10), Inches(3.8), Inches(0.28), "LBIST CONTROLLER & FAULT COVERAGE ANALYSIS", C_PILL_ORANGE)

    m3_tb = s3.shapes.add_textbox(right_x + Inches(0.20), c4_y + Inches(0.42), col_w - Inches(0.40), c4_h - Inches(0.48))
    m3_tf = m3_tb.text_frame
    m3_tf.word_wrap = True
    m3_tf.margin_top = m3_tf.margin_bottom = m3_tf.margin_left = m3_tf.margin_right = 0

    m3_bullets = [
        ("100.0% Stuck-At Fault Coverage:", " Detected 2,048 / 2,048 modeled stuck-at faults across all 4 chains × 256 cells × 2 polarities (s-a-0 and s-a-1) with zero undetected faults."),
        ("Zero-Aliasing Response Compaction:", " 16-bit Multi-Input Signature Register (MISR) compacts output responses into a deterministic golden signature with 0 signature aliasing."),
        ("Autonomous 4-Phase Test Sequencing:", " Dedicated FSM manages complete test flow: Synchronous Reset → Scan Shift (L=256) → Single-Cycle Capture → Signature Compaction."),
        ("Zero External ATE Dependency:", " Generates internal PASS / FAIL flag directly on-chip, enabling low-cost manufacturing testing and autonomous in-field diagnostic self-test."),
        ("Thermal & IR-Drop Protection:", " High defect detection is preserved while toggle suppression eliminates scan-shift power spikes, preventing test-induced false failures.")
    ]

    for i, (hd, body) in enumerate(m3_bullets):
        p = m3_tf.add_paragraph()
        if i > 0:
            p.space_before = Pt(2.5)
        r1 = p.add_run()
        r1.text = "• " + hd
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(7.4)
        r1.font.bold = True
        r1.font.color.rgb = C_PILL_ORANGE

        r2 = p.add_run()
        r2.text = body
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(7.0)
        r2.font.color.rgb = C_TEXT_DARK

    # -------------------------------------------------------------------------
    # BOTTOM FULL-WIDTH BANNER: Thank You! Questions & Discussion Welcome
    # -------------------------------------------------------------------------
    thx_y = Inches(6.58)
    thx_h = Inches(0.58)
    thx_w = Inches(11.733)
    thx_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), thx_y, thx_w, thx_h)
    thx_box.fill.solid()
    thx_box.fill.fore_color.rgb = RGBColor(238, 242, 255)
    thx_box.line.color.rgb = C_BLUE
    thx_box.line.width = Pt(1.5)

    ttb = s3.shapes.add_textbox(Inches(0.9), thx_y + Inches(0.06), thx_w - Inches(0.2), thx_h - Inches(0.12))
    ttf = ttb.text_frame
    ttf.word_wrap = True
    ttf.margin_top = ttf.margin_bottom = ttf.margin_left = ttf.margin_right = 0
    tp1 = ttf.paragraphs[0]
    tp1.text = "Thank You! Questions & Discussion Welcome"
    tp1.alignment = PP_ALIGN.CENTER
    tp1.font.name = FONT_MAIN
    tp1.font.size = Pt(11)
    tp1.font.bold = True
    tp1.font.color.rgb = C_NAVY_HEADING

    tp2 = ttf.add_paragraph()
    tp2.text = "VL405 Design for Testability Laboratory Project  •  Department of Electronics & Communication Engineering"
    tp2.alignment = PP_ALIGN.CENTER
    tp2.font.name = FONT_MAIN
    tp2.font.size = Pt(8.5)
    tp2.font.bold = True
    tp2.font.color.rgb = C_NAVY_SUB
    tp2.space_before = Pt(2)

    # Save presentation
    output_filename = "VL405_LBIST_Project_Presentation.pptx"
    prs.save(output_filename)
    print(f"[SUCCESS] Exact 3-Slide Presentation compiled to: {output_filename}")

if __name__ == "__main__":
    build_presentation()
