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

    # PROPOSED APPROACH & OBJECTIVES (Right Card)
    prop_x = start_x + prob_w + Inches(0.24)
    prop_w = intro_w - prob_w - Inches(0.24)

    prbox = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, prop_x, sec_y, prop_w, sec_h)
    prbox.fill.solid()
    prbox.fill.fore_color.rgb = RGBColor(240, 253, 244)
    prbox.line.color.rgb = RGBColor(187, 247, 208)
    prbox.line.width = Pt(1.5)

    add_pill_badge(s1, prop_x + Inches(0.18), sec_y + Inches(0.14), Inches(3.2), Inches(0.34), "PROPOSED APPROACH & OBJECTIVES", C_PILL_GREEN)

    # Core concept inner box
    concept_y = sec_y + Inches(0.56)
    concept_h = Inches(0.68)
    c_inner = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, prop_x + Inches(0.18), concept_y, prop_w - Inches(0.36), concept_h)
    c_inner.fill.solid()
    c_inner.fill.fore_color.rgb = C_WHITE
    c_inner.line.color.rgb = RGBColor(209, 250, 229)
    c_inner.line.width = Pt(1)

    ctb = s1.shapes.add_textbox(prop_x + Inches(0.30), concept_y + Inches(0.12), prop_w - Inches(0.60), concept_h - Inches(0.24))
    ctf = ctb.text_frame
    ctf.word_wrap = True
    ctf.margin_top = ctf.margin_bottom = ctf.margin_left = ctf.margin_right = 0
    cp = ctf.paragraphs[0]
    cp.text = "Programmable toggle-rate control modifies PRPG-generated patterns to reduce unnecessary scan-shift transitions."
    cp.font.name = FONT_MAIN
    cp.font.size = Pt(9.5)
    cp.font.bold = True
    cp.font.color.rgb = C_NAVY_HEADING

    # 4 Numbered Objectives
    objs = [
        "Generate pseudorandom patterns using an LFSR-based PRPG.",
        "Control switching activity with a programmable pattern modifier.",
        "Apply modified patterns to the MIPS32 scan chains.",
        "Evaluate toggle rate, scan activity, power and test effectiveness."
    ]

    obj_start_y = concept_y + concept_h + Inches(0.14)
    obj_gap = Inches(0.55)

    for i, obj_txt in enumerate(objs):
        oy = obj_start_y + i * obj_gap

        # Number badge
        nb = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, prop_x + Inches(0.22), oy, Inches(0.34), Inches(0.34))
        nb.fill.solid()
        nb.fill.fore_color.rgb = C_WHITE
        nb.line.color.rgb = RGBColor(167, 243, 208)
        nb.line.width = Pt(1)
        np_ = nb.text_frame.paragraphs[0]
        np_.text = str(i + 1)
        np_.alignment = PP_ALIGN.CENTER
        np_.font.name = FONT_MAIN
        np_.font.size = Pt(9.5)
        np_.font.bold = True
        np_.font.color.rgb = C_PILL_GREEN

        # Text
        otb = s1.shapes.add_textbox(prop_x + Inches(0.68), oy - Inches(0.02), prop_w - Inches(0.90), Inches(0.38))
        otf = otb.text_frame
        otf.word_wrap = True
        otf.margin_top = otf.margin_bottom = otf.margin_left = otf.margin_right = 0
        op = otf.paragraphs[0]
        op.text = obj_txt
        op.font.name = FONT_MAIN
        op.font.size = Pt(9.2)
        op.font.color.rgb = C_TEXT_DARK

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
    # SLIDE 3: INTEGRATED RESULTS & COMPLETE PROJECT CONCLUSION (ALL 3 MEMBERS)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s3)

    render_header(s3,
                  "Experimental Results and Complete Project Conclusion",
                  "Compiled outcomes: MIPS32 scan architecture, PRPG toggle control, 100% fault coverage, and Vivado synthesis",
                  3)

    col_w = Inches(5.7)

    # -------------------------------------------------------------------------
    # LEFT COLUMN: Member 2 Toggle Results & Vivado Full-System Synthesis
    # -------------------------------------------------------------------------
    left_x = Inches(0.8)

    # 1. Member 2: LFSR Equation & Measured Toggle-Rate Results Card
    tbl_y = Inches(1.34)
    tbl_h = Inches(2.68)
    tbox = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, tbl_y, col_w, tbl_h)
    tbox.fill.solid()
    tbox.fill.fore_color.rgb = C_WHITE
    tbox.line.color.rgb = C_CARD_BORDER
    tbox.line.width = Pt(1.5)

    add_pill_badge(s3, left_x + Inches(0.18), tbl_y + Inches(0.10), Inches(3.4), Inches(0.28), "MEMBER 2: PRPG TOGGLE-RATE & POWER RESULTS", C_PILL_GREEN)

    # LFSR Characteristic Polynomial Equation Header
    eq_tb = s3.shapes.add_textbox(left_x + Inches(0.16), tbl_y + Inches(0.40), col_w - Inches(0.32), Inches(0.26))
    eq_tf = eq_tb.text_frame
    eq_tf.word_wrap = True
    eq_tf.margin_top = eq_tf.margin_bottom = eq_tf.margin_left = eq_tf.margin_right = 0
    eq_p = eq_tf.paragraphs[0]
    r_eq_lbl = eq_p.add_run()
    r_eq_lbl.text = "LFSR Polynomial: "
    r_eq_lbl.font.name = FONT_MAIN
    r_eq_lbl.font.size = Pt(7.8)
    r_eq_lbl.font.bold = True
    r_eq_lbl.font.color.rgb = C_NAVY_HEADING

    r_eq_val = eq_p.add_run()
    r_eq_val.text = "P(x) = x¹⁶ + x¹⁴ + x¹³ + x¹¹ + 1   [Poly: 0xB400, Seed: 0xACE1]"
    r_eq_val.font.name = FONT_MAIN
    r_eq_val.font.size = Pt(7.6)
    r_eq_val.font.bold = True
    r_eq_val.font.color.rgb = C_BLUE

    # Results Table (Compact 8 rows x 5 cols)
    table_shape = s3.shapes.add_table(8, 5, left_x + Inches(0.14), tbl_y + Inches(0.68), col_w - Inches(0.28), Inches(1.64))
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

    # Clarification note below table
    notetb = s3.shapes.add_textbox(left_x + Inches(0.16), tbl_y + Inches(2.36), col_w - Inches(0.32), Inches(0.28))
    notetf = notetb.text_frame
    notetf.word_wrap = True
    notetf.margin_top = notetf.margin_bottom = notetf.margin_left = notetf.margin_right = 0
    notep = notetf.paragraphs[0]
    notep.text = "DDRTS pattern modifier reduces total on-chip scan-shift power by up to 84.35% with only 82 LUTs, 57 FFs."
    notep.font.name = FONT_MAIN
    notep.font.size = Pt(6.8)
    notep.font.color.rgb = C_TEXT_MUTED

    # 2. Full Integrated System Synthesis Summary (All 3 Members Combined)
    syn_y = Inches(4.12)
    syn_h = Inches(2.36)
    syn_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, syn_y, col_w, syn_h)
    syn_box.fill.solid()
    syn_box.fill.fore_color.rgb = C_WHITE
    syn_box.line.color.rgb = C_CARD_BORDER
    syn_box.line.width = Pt(1.5)

    add_pill_badge(s3, left_x + Inches(0.18), syn_y + Inches(0.10), Inches(3.4), Inches(0.28), "FULL-SYSTEM FPGA SYNTHESIS (VIVADO)", C_PILL_BLUE)

    # 4 Metric Blocks inside Synthesis Card
    vmetrics = [
        ("Run status", "Complete", C_PILL_GREEN),
        ("LUTs", "5,565", C_PILL_BLUE),
        ("Flip-flops", "1,287", C_PILL_BLUE),
        ("BRAM / URAM / DSP", "0 / 0 / 0", C_TEXT_DARK)
    ]
    vm_w = Inches(1.24)
    vm_h = Inches(0.70)
    vm_gap = Inches(0.12)
    vm_start_x = left_x + Inches(0.16)
    vm_y = syn_y + Inches(0.42)

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
        mp2.font.size = Pt(9.5)
        mp2.font.bold = True
        mp2.font.color.rgb = m_col
        mp2.space_before = Pt(2)

    # Synthesis Key Notes
    sntb = s3.shapes.add_textbox(left_x + Inches(0.18), syn_y + Inches(1.18), col_w - Inches(0.36), Inches(1.10))
    sntf = sntb.text_frame
    sntf.word_wrap = True
    sntf.margin_top = sntf.margin_bottom = sntf.margin_left = sntf.margin_right = 0
    snp1 = sntf.paragraphs[0]
    snp1.text = "• Integrated SoC Architecture: Combines Member 1 (MIPS32 CPU & Scan Chains), Member 2 (16-bit PRPG Modifier), and Member 3 (LBIST FSM & 16-bit MISR)."
    snp1.font.name = FONT_MAIN
    snp1.font.size = Pt(7.5)
    snp1.font.color.rgb = C_TEXT_DARK

    snp2 = sntf.add_paragraph()
    snp2.text = "• FPGA Resource Footprint: Synthesized on AMD Xilinx Artix-7 (xc7a35tcsg324-1) consuming 5,565 LUTs (26.8%) and 1,287 FFs (3.1%); 0 dedicated BRAM/DSP blocks."
    snp2.font.name = FONT_MAIN
    snp2.font.size = Pt(7.5)
    snp2.font.color.rgb = C_TEXT_DARK
    snp2.space_before = Pt(2)

    snp3 = sntf.add_paragraph()
    snp3.text = "• Vivado Power Scaling: Demonstrates monotonic dynamic power reduction down to 59 mW (28.9% chip dynamic power cut) across toggle targets with 100% static stability."
    snp3.font.name = FONT_MAIN
    snp3.font.size = Pt(7.5)
    snp3.font.color.rgb = C_TEXT_DARK
    snp3.space_before = Pt(2)

    # -------------------------------------------------------------------------
    # RIGHT COLUMN: All-Members Verified Results & Project Conclusion
    # -------------------------------------------------------------------------
    right_x = Inches(6.833)

    # 1. Member 1 & Member 3 Verified Results Card (Top)
    mem_y = Inches(1.34)
    mem_h = Inches(2.68)
    mem_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, mem_y, col_w, mem_h)
    mem_box.fill.solid()
    mem_box.fill.fore_color.rgb = C_WHITE
    mem_box.line.color.rgb = RGBColor(167, 243, 208)
    mem_box.line.width = Pt(1.5)

    add_pill_badge(s3, right_x + Inches(0.18), mem_y + Inches(0.10), Inches(3.6), Inches(0.28), "MEMBER 1 & 3 VERIFIED CONTRIBUTIONS", C_PILL_BLUE)

    mtb = s3.shapes.add_textbox(right_x + Inches(0.20), mem_y + Inches(0.42), col_w - Inches(0.40), mem_h - Inches(0.48))
    mtf = mtb.text_frame
    mtf.word_wrap = True
    mtf.margin_top = mtf.margin_bottom = mtf.margin_left = mtf.margin_right = 0

    member_results = [
        ("Member 1 (Harshitha) — MIPS32 Core & Scan Partitioning:",
         " Synthesizable 32-bit MIPS CPU core with 1,024 scanned state bits (32-bit PC + 31 32-bit registers r1–r31); organized into 4 balanced scan chains × 256 cells; achieves 100% internal test controllability and observability with +7.29 ns timing slack.",
         C_BLUE),
        ("Member 3 (Gaurav) — LBIST Controller & Fault Analysis:",
         " Autonomous 4-phase test sequencing FSM (Reset → Shift → Capture → Compact); 100.0% fault coverage achieved (2,048 / 2,048 modeled stuck-at faults detected across all scan cells with zero aliasing); 16-bit MISR compacts responses into golden signature for on-chip PASS/FAIL evaluation without external ATE.",
         C_PILL_ORANGE)
    ]

    for i, (mhd, mdesc, mcol) in enumerate(member_results):
        p = mtf.add_paragraph()
        if i > 0:
            p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + mhd
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(7.8)
        r1.font.bold = True
        r1.font.color.rgb = mcol

        r2 = p.add_run()
        r2.text = mdesc
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(7.3)
        r2.font.color.rgb = C_TEXT_DARK

    # 2. Comprehensive Project Conclusion & Impact Card (Bottom)
    fut_y = Inches(4.12)
    fut_h = Inches(2.36)
    fut_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, fut_y, col_w, fut_h)
    fut_box.fill.solid()
    fut_box.fill.fore_color.rgb = C_WHITE
    fut_box.line.color.rgb = RGBColor(191, 219, 254)
    fut_box.line.width = Pt(1.5)

    add_pill_badge(s3, right_x + Inches(0.18), fut_y + Inches(0.10), Inches(3.6), Inches(0.28), "OVERALL PROJECT CONCLUSION & IMPACT", C_PILL_BLUE)

    ftb = s3.shapes.add_textbox(right_x + Inches(0.20), fut_y + Inches(0.42), col_w - Inches(0.40), fut_h - Inches(0.48))
    ftf = ftb.text_frame
    ftf.word_wrap = True
    ftf.margin_top = ftf.margin_bottom = ftf.margin_left = ftf.margin_right = 0

    fut_items = [
        ("Complete Autonomous LBIST Flow:",
         " Successfully demonstrated unified on-chip testing integrating PRPG pattern generation (M2), scan-shift execution on MIPS32 (M1), and MISR signature compaction with 100% fault coverage (M3)."),
        ("Resolved Scan Power Crisis:",
         " Programmable toggle suppression cuts scan switching activity by up to 84.35%, effectively preventing test-induced IR-drop delay faults and thermal hotspots during manufacturing sort."),
        ("Zero External ATE Dependency:",
         " The self-contained LBIST architecture executes complete self-test on-chip, significantly reducing test equipment costs for production and mission-critical field diagnostics."),
        ("Next Steps & Future Work:",
         " Transition delay fault grading, physical FPGA board-level validation, and post-layout timing closure.")
    ]

    for i, (fhd, fdesc) in enumerate(fut_items):
        p = ftf.add_paragraph()
        if i > 0:
            p.space_before = Pt(3)
        r1 = p.add_run()
        r1.text = "• " + fhd
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(7.8)
        r1.font.bold = True
        r1.font.color.rgb = C_PILL_BLUE

        r2 = p.add_run()
        r2.text = fdesc
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(7.3)
        r2.font.color.rgb = C_TEXT_DARK

    # -------------------------------------------------------------------------
    # BOTTOM FULL-WIDTH BANNER: Thank You! Questions & Discussion Welcome
    # -------------------------------------------------------------------------
    thx_y = Inches(6.58)
    thx_h = Inches(0.58)
    thx_w = Inches(11.733)
    thx_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), thx_y, thx_w, thx_h)
    thx_box.fill.solid()
    thx_box.fill.fore_color.rgb = RGBColor(238, 242, 255) # Light Indigo (#EEF2FF)
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
