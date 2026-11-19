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
    C_PILL_TEAL    = RGBColor(15, 118, 110)  # Teal

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
    # Matches build_exact_results_slide.py exactly.
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s3)

    # Header for Slide 3
    left_m = Inches(0.8)
    bar3 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_m, Inches(0.36), Inches(0.08), Inches(0.56))
    bar3.fill.solid()
    bar3.fill.fore_color.rgb = C_BLUE
    bar3.line.fill.background()

    tb3 = s3.shapes.add_textbox(left_m + Inches(0.18), Inches(0.32), Inches(11.4), Inches(0.85))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.margin_top = tf3.margin_bottom = tf3.margin_left = tf3.margin_right = 0
    p1_3 = tf3.paragraphs[0]
    p1_3.text = "COMPILED PROJECT RESULTS & PERFORMANCE ANALYSIS"
    p1_3.font.name = FONT_MAIN
    p1_3.font.size = Pt(20)
    p1_3.font.bold = True
    p1_3.font.color.rgb = C_NAVY_HEADING

    p2_3 = tf3.add_paragraph()
    p2_3.text = "32-bit PRPG • Four-lane scan architecture • Programmable activity control • Integrated synthesis and LBIST analysis"
    p2_3.font.name = FONT_MAIN
    p2_3.font.size = Pt(9.5)
    p2_3.font.color.rgb = C_NAVY_SUB
    p2_3.space_before = Pt(3)

    div3 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_m, Inches(1.18), Inches(11.733), Inches(0.01))
    div3.fill.solid()
    div3.fill.fore_color.rgb = RGBColor(226, 232, 240)
    div3.line.fill.background()

    col_w = Inches(5.70)
    left_x = Inches(0.80)
    right_x = Inches(6.833)

    # =========================================================================
    # CARD 1 (Top Left): 1. PRPG, LFSR & SCAN-ACTIVITY RESULTS
    # =========================================================================
    c1_y = Inches(1.26)
    c1_h = Inches(2.74)
    box1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, c1_y, col_w, c1_h)
    box1.fill.solid()
    box1.fill.fore_color.rgb = C_WHITE
    box1.line.color.rgb = RGBColor(167, 243, 208)
    box1.line.width = Pt(1.5)

    add_pill_badge(s3, left_x + Inches(0.14), c1_y + Inches(0.08), Inches(3.60), Inches(0.24), "1. PRPG, LFSR & SCAN-ACTIVITY RESULTS", C_PILL_GREEN)

    # Polynomial Equation
    eq_tb = s3.shapes.add_textbox(left_x + Inches(0.14), c1_y + Inches(0.34), col_w - Inches(0.28), Inches(0.20))
    eq_tf = eq_tb.text_frame
    eq_tf.margin_top = eq_tf.margin_bottom = eq_tf.margin_left = eq_tf.margin_right = 0
    ep = eq_tf.paragraphs[0]
    ep.alignment = PP_ALIGN.CENTER
    ep.text = "P(x) = x³² + x²² + x² + x + 1"
    ep.font.name = FONT_MAIN
    ep.font.size = Pt(11)
    ep.font.bold = True
    ep.font.color.rgb = C_NAVY_HEADING

    sub_tb = s3.shapes.add_textbox(left_x + Inches(0.14), c1_y + Inches(0.54), col_w - Inches(0.28), Inches(0.16))
    sub_tf = sub_tb.text_frame
    sub_tf.margin_top = sub_tf.margin_bottom = sub_tf.margin_left = sub_tf.margin_right = 0
    sp = sub_tf.paragraphs[0]
    sp.alignment = PP_ALIGN.CENTER
    sp.text = "32-bit Galois LFSR  |  Seed loading  |  All-zero detection and automatic recovery"
    sp.font.name = FONT_MAIN
    sp.font.size = Pt(7.0)
    sp.font.color.rgb = C_TEXT_MUTED

    # 5 Flow Blocks
    fblocks = ["Seed", "32-bit LFSR", "Pattern modifier", "Four-lane adapter", "Scan inputs"]
    fb_w = Inches(0.88)
    fb_h = Inches(0.20)
    farr_w = Inches(0.14)
    total_flow_w = len(fblocks) * fb_w + (len(fblocks) - 1) * farr_w
    flow_start_x = left_x + (col_w - total_flow_w) / 2
    flow_y = c1_y + Inches(0.72)

    for i, blk in enumerate(fblocks):
        bx = flow_start_x + i * (fb_w + farr_w)
        b_shp = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, flow_y, fb_w, fb_h)
        b_shp.fill.solid()
        b_shp.fill.fore_color.rgb = RGBColor(240, 253, 244)
        b_shp.line.color.rgb = RGBColor(187, 247, 208)
        b_shp.line.width = Pt(1)
        btf = b_shp.text_frame
        btf.margin_top = btf.margin_bottom = btf.margin_left = btf.margin_right = 0
        bp = btf.paragraphs[0]
        bp.alignment = PP_ALIGN.CENTER
        bp.text = blk
        bp.font.name = FONT_MAIN
        bp.font.size = Pt(6.5)
        bp.font.bold = True
        bp.font.color.rgb = RGBColor(19, 78, 74)

        if i < len(fblocks) - 1:
            ax = bx + fb_w
            arr = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, ax + Inches(0.02), flow_y + Inches(0.04), farr_w - Inches(0.04), Inches(0.12))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_PILL_GREEN
            arr.line.fill.background()

    # Table: 8 rows x 4 columns
    tbl_y = c1_y + Inches(0.96)
    tbl_h = Inches(1.50)
    table_shape = s3.shapes.add_table(8, 4, left_x + Inches(0.14), tbl_y, col_w - Inches(0.28), tbl_h)
    tbl = table_shape.table
    tbl.columns[0].width = Inches(0.85)
    tbl.columns[1].width = Inches(1.45)
    tbl.columns[2].width = Inches(1.55)
    tbl.columns[3].width = Inches(1.57)

    headers = ["Mode", "Measured scan activity", "Switching ratio versus Bypass", "Reduction versus Bypass"]
    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.margin_top = Inches(0.01)
        cell.margin_bottom = Inches(0.01)
        cell.margin_left = Inches(0.02)
        cell.margin_right = Inches(0.02)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(15, 37, 68)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_MAIN
        p.font.size = Pt(6.8)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    table_data = [
        ("10%", "4%", "8%", "92%"),
        ("20%", "9%", "18%", "82%"),
        ("30%", "14%", "28%", "72%"),
        ("40%", "19%", "38%", "62%"),
        ("50%", "24%", "48%", "52%"),
        ("60%", "29%", "58%", "42%"),
        ("Bypass", "50%", "100%", "0%")
    ]

    for row_idx, row in enumerate(table_data):
        for col_idx, val in enumerate(row):
            cell = tbl.cell(row_idx + 1, col_idx)
            cell.margin_top = Inches(0.01)
            cell.margin_bottom = Inches(0.01)
            cell.margin_left = Inches(0.02)
            cell.margin_right = Inches(0.02)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 0 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.CENTER
            p.font.name = FONT_MAIN
            p.font.size = Pt(6.8)
            if col_idx == 3 and val != "0%":
                p.font.bold = True
                p.font.color.rgb = C_PILL_GREEN
            elif col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_NAVY_HEADING
            else:
                p.font.color.rgb = C_TEXT_DARK

    # Table sub-note
    tn_tb = s3.shapes.add_textbox(left_x + Inches(0.14), c1_y + Inches(2.50), col_w - Inches(0.28), Inches(0.18))
    tn_tf = tn_tb.text_frame
    tn_tf.margin_top = tn_tf.margin_bottom = tn_tf.margin_left = tn_tf.margin_right = 0
    tp_ = tn_tf.paragraphs[0]
    tp_.alignment = PP_ALIGN.CENTER
    tp_.text = "4 patterns × 4 scan lanes × 256 cells = 4,096 lane-shift opportunities."
    tp_.font.name = FONT_MAIN
    tp_.font.size = Pt(6.2)
    tp_.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # CARD 2 (Top Right): 2. MIPS32 CORE & SCAN ARCHITECTURE
    # =========================================================================
    box2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, c1_y, col_w, c1_h)
    box2.fill.solid()
    box2.fill.fore_color.rgb = C_WHITE
    box2.line.color.rgb = RGBColor(191, 219, 254)
    box2.line.width = Pt(1.5)

    add_pill_badge(s3, right_x + Inches(0.14), c1_y + Inches(0.08), Inches(3.60), Inches(0.24), "2. MIPS32 CORE & SCAN ARCHITECTURE", C_PILL_BLUE)

    m2_tb = s3.shapes.add_textbox(right_x + Inches(0.18), c1_y + Inches(0.38), col_w - Inches(0.36), Inches(1.56))
    m2_tf = m2_tb.text_frame
    m2_tf.word_wrap = True
    m2_tf.margin_top = m2_tf.margin_bottom = m2_tf.margin_left = m2_tf.margin_right = 0

    m2_bullets = [
        "1,024 scanned architectural state bits: 32-bit Program Counter and 31 general-purpose registers.",
        "Four balanced scan chains, each containing 256 flip-flops.",
        "Each test vector requires 256 shift cycles followed by one capture cycle.",
        "At 50 megahertz: +7.291 nanoseconds setup slack and +0.119 nanoseconds hold slack; zero failing endpoints."
    ]

    for i, btext in enumerate(m2_bullets):
        p = m2_tf.add_paragraph()
        if i > 0:
            p.space_before = Pt(4)
        r = p.add_run()
        r.text = "• " + btext
        r.font.name = FONT_MAIN
        r.font.size = Pt(7.4)
        r.font.color.rgb = C_TEXT_DARK

    # 3 Metric boxes at bottom of Card 2
    m2_metrics = [
        ("Scanned bits", "1,024"),
        ("Scan chains", "4"),
        ("Cells per chain", "256")
    ]
    m2m_w = Inches(1.66)
    m2m_h = Inches(0.54)
    m2m_gap = Inches(0.18)
    m2m_start_x = right_x + Inches(0.18)
    m2m_y = c1_y + Inches(2.04)

    for i, (mlbl, mval) in enumerate(m2_metrics):
        mb = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, m2m_start_x + i * (m2m_w + m2m_gap), m2m_y, m2m_w, m2m_h)
        mb.fill.solid()
        mb.fill.fore_color.rgb = RGBColor(248, 250, 252)
        mb.line.color.rgb = C_BORDER_MID
        mb.line.width = Pt(1)
        mtf = mb.text_frame
        mtf.margin_top = mtf.margin_bottom = mtf.margin_left = mtf.margin_right = 0
        p_1 = mtf.paragraphs[0]
        p_1.alignment = PP_ALIGN.CENTER
        p_1.text = mlbl
        p_1.font.name = FONT_MAIN
        p_1.font.size = Pt(6.8)
        p_1.font.color.rgb = C_TEXT_MUTED

        p_2 = mtf.add_paragraph()
        p_2.alignment = PP_ALIGN.CENTER
        p_2.text = mval
        p_2.font.name = FONT_MAIN
        p_2.font.size = Pt(10)
        p_2.font.bold = True
        p_2.font.color.rgb = C_BLUE
        p_2.space_before = Pt(2)

    # =========================================================================
    # CARD 3 (Bottom Left): 3. INTEGRATED FPGA SYNTHESIS (VIVADO)
    # =========================================================================
    c3_y = Inches(4.10)
    c3_h = Inches(2.38)
    box3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, c3_y, col_w, c3_h)
    box3.fill.solid()
    box3.fill.fore_color.rgb = C_WHITE
    box3.line.color.rgb = C_CARD_BORDER
    box3.line.width = Pt(1.5)

    add_pill_badge(s3, left_x + Inches(0.14), c3_y + Inches(0.08), Inches(3.60), Inches(0.24), "3. INTEGRATED FPGA SYNTHESIS (VIVADO)", C_PILL_TEAL)

    # 4 Metric Blocks
    vmetrics = [
        ("Run status", "Complete", C_PILL_GREEN),
        ("Look-up tables", "5,565 (26.8%)", C_PILL_BLUE),
        ("Flip-flops", "1,287 (3.1%)", C_PILL_BLUE),
        ("Block RAM / DSP", "0 / 0 / 0", C_TEXT_DARK)
    ]
    vm_w = Inches(1.24)
    vm_h = Inches(0.56)
    vm_gap = Inches(0.12)
    vm_start_x = left_x + Inches(0.16)
    vm_y = c3_y + Inches(0.38)

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
        mp2.font.size = Pt(9.0)
        mp2.font.bold = True
        mp2.font.color.rgb = m_col
        mp2.space_before = Pt(2)

    # Bullets for Synthesis
    sntb = s3.shapes.add_textbox(left_x + Inches(0.18), c3_y + Inches(1.00), col_w - Inches(0.36), Inches(1.32))
    sntf = sntb.text_frame
    sntf.word_wrap = True
    sntf.margin_top = sntf.margin_bottom = sntf.margin_left = sntf.margin_right = 0

    syn_bullets = [
        "Unified integration: MIPS32 core, four scan chains, 16-bit PRPG modifier, LBIST controller and MISR.",
        "Synthesized for AMD Artix-7 device xc7a35tcsg324-1.",
        "Activity-driven dynamic-power estimate: 83 milliwatts in Bypass mode → 59 milliwatts at the 10% target (28.9% reduction).",
        "Single synchronous 50 megahertz clock domain with active-low reset."
    ]

    for i, btext in enumerate(syn_bullets):
        p = sntf.add_paragraph()
        if i > 0:
            p.space_before = Pt(3.5)
        r = p.add_run()
        r.text = "• " + btext
        r.font.name = FONT_MAIN
        r.font.size = Pt(7.3)
        r.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # CARD 4 (Bottom Right): 4. LBIST CONTROLLER, MISR & FAULT ANALYSIS
    # =========================================================================
    box4 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, c3_y, col_w, c3_h)
    box4.fill.solid()
    box4.fill.fore_color.rgb = C_WHITE
    box4.line.color.rgb = RGBColor(254, 215, 170)
    box4.line.width = Pt(1.5)

    add_pill_badge(s3, right_x + Inches(0.14), c3_y + Inches(0.08), Inches(3.80), Inches(0.24), "4. LBIST CONTROLLER, MISR & FAULT ANALYSIS", C_PILL_ORANGE)

    m4_tb = s3.shapes.add_textbox(right_x + Inches(0.18), c3_y + Inches(0.36), col_w - Inches(0.36), Inches(1.56))
    m4_tf = m4_tb.text_frame
    m4_tf.word_wrap = True
    m4_tf.margin_top = m4_tf.margin_bottom = m4_tf.margin_left = m4_tf.margin_right = 0

    m4_bullets = [
        "100% modeled stuck-at fault coverage: 2,048 of 2,048 faults detected across four chains × 256 cells × two polarities (stuck-at-0 and stuck-at-1).",
        "32-bit Multi-Input Signature Register with four scan-output inputs; all-ones seed.",
        "MISR feedback polynomial: x³² + x²² + x² + x + 1.",
        "Test sequence: synchronous reset → scan shift (256 cycles) → single-cycle capture → signature compaction.",
        "Final signature matches golden signature → PASS; otherwise → FAIL."
    ]

    for i, btext in enumerate(m4_bullets):
        p = m4_tf.add_paragraph()
        if i > 0:
            p.space_before = Pt(2.5)
        r = p.add_run()
        r.text = "• " + btext
        r.font.name = FONT_MAIN
        r.font.size = Pt(7.1)
        r.font.color.rgb = C_TEXT_DARK

    # Aliasing probability box at bottom of Card 4
    alias_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x + Inches(0.18), c3_y + Inches(1.98), col_w - Inches(0.36), Inches(0.30))
    alias_box.fill.solid()
    alias_box.fill.fore_color.rgb = RGBColor(255, 247, 237)
    alias_box.line.color.rgb = RGBColor(254, 215, 170)
    alias_box.line.width = Pt(1)

    ab_tf = alias_box.text_frame
    ab_tf.margin_top = ab_tf.margin_bottom = ab_tf.margin_left = ab_tf.margin_right = 0
    ap = ab_tf.paragraphs[0]
    ap.alignment = PP_ALIGN.CENTER
    ap.text = "Theoretical aliasing probability for a 32-bit signature: 1 / 2³² ≈ 2.3 × 10⁻¹⁰"
    ap.font.name = FONT_MAIN
    ap.font.size = Pt(7.2)
    ap.font.bold = True
    ap.font.color.rgb = C_PILL_ORANGE

    # Sub-footnote below cards
    foot_tb = s3.shapes.add_textbox(left_m, Inches(6.52), Inches(11.733), Inches(0.18))
    foot_tf = foot_tb.text_frame
    foot_tf.margin_top = foot_tf.margin_bottom = foot_tf.margin_left = foot_tf.margin_right = 0
    fp_ = foot_tf.paragraphs[0]
    fp_.alignment = PP_ALIGN.CENTER
    fp_.text = "Scan-lane transition reduction and dynamic-power reduction are different metrics; fault coverage is a modeled stuck-at result."
    fp_.font.name = FONT_MAIN
    fp_.font.size = Pt(6.5)
    fp_.font.color.rgb = C_TEXT_MUTED

    # Bottom Banner
    thx_y = Inches(6.74)
    thx_h = Inches(0.48)
    thx_w = Inches(11.733)
    thx_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_m, thx_y, thx_w, thx_h)
    thx_box.fill.solid()
    thx_box.fill.fore_color.rgb = RGBColor(238, 242, 255)
    thx_box.line.color.rgb = C_BLUE
    thx_box.line.width = Pt(1.5)

    ttb = s3.shapes.add_textbox(left_m + Inches(0.1), thx_y + Inches(0.12), thx_w - Inches(0.2), thx_h - Inches(0.24))
    ttf = ttb.text_frame
    ttf.margin_top = ttf.margin_bottom = ttf.margin_left = ttf.margin_right = 0
    tp1 = ttf.paragraphs[0]
    tp1.text = "THANK YOU  •  QUESTIONS & DISCUSSION WELCOME"
    tp1.alignment = PP_ALIGN.CENTER
    tp1.font.name = FONT_MAIN
    tp1.font.size = Pt(10)
    tp1.font.bold = True
    tp1.font.color.rgb = C_NAVY_HEADING

    # Save presentation
    output_filename = "VL405_LBIST_Project_Presentation.pptx"
    prs.save(output_filename)
    print(f"[SUCCESS] Exact 3-Slide Presentation compiled to: {output_filename}")

if __name__ == "__main__":
    build_presentation()
