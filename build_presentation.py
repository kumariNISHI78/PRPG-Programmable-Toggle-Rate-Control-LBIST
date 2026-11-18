"""
Builds an academically styled, professional 3-slide PowerPoint presentation for VL405 DFT Laboratory Project.
Exact Requirements from User Reference Images:
- Slide 1: Introduction, Problem Statement, Proposed Approach & Objectives, 3 Team Member Cards.
- Slide 2: Proposed LBIST Architecture Flow Diagram (Overall Architecture, Working Principle, Key Components).
- Slide 3: Results & Conclusion combined on 1 page (Measured Toggle-Rate Table, Vivado Synthesis Summary, Key Achievements, Future Scope & Integration). No graphs or waveforms. Exact verified results.
- 100% Native editable PowerPoint shapes, text boxes, and tables.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Academic Palette
    C_BG = RGBColor(250, 250, 252)          # Off-white background (#FAFAFC)
    C_WHITE = RGBColor(255, 255, 255)       # Card background (#FFFFFF)
    C_CARD_BORDER = RGBColor(226, 232, 240) # Card Border (#E2E8F0)
    C_BORDER_MID = RGBColor(203, 213, 225)  # Mid Border (#CBD5E1)
    
    # Typography Colors
    C_NAVY_HEADING = RGBColor(15, 37, 68)   # Deep Navy (#0F2544)
    C_NAVY_SUB = RGBColor(75, 85, 99)       # Subtitle Slate (#4B5563)
    C_TEXT_DARK = RGBColor(31, 41, 55)      # Body Dark (#1F2937)
    C_TEXT_MUTED = RGBColor(107, 114, 128)  # Supporting Text (#6B7280)
    
    # Pill & Accent Colors
    C_PILL_BLUE = RGBColor(29, 78, 216)     # Primary Blue Pill (#1D4ED8)
    C_PILL_GREEN = RGBColor(5, 150, 105)    # Green Pill (#059669)
    C_PILL_RED = RGBColor(220, 38, 38)      # Red Pill (#DC2626)
    
    # Border & Component Accents
    C_BLUE = RGBColor(37, 99, 235)          # Member 1 / MIPS32 (#2563EB)
    C_TEAL = RGBColor(13, 148, 136)         # Member 2 / PRPG (#0D9488)
    C_ORANGE = RGBColor(217, 119, 6)        # Member 3 / Controller (#D97706)
    C_PURPLE = RGBColor(124, 58, 237)       # FSM Controller / Analysis (#7C3AED)
    C_AMBER_DARK = RGBColor(180, 83, 9)     # MISR (#B45309)

    FONT_MAIN = "Calibri"

    def apply_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def render_header(slide, title_text, subtitle_text, slide_num):
        # Vertical Blue Accent Bar before title (Exact match to reference)
        vbar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.36), Inches(0.08), Inches(0.56))
        vbar.fill.solid()
        vbar.fill.fore_color.rgb = C_PILL_BLUE
        vbar.line.fill.background()

        # Title and Subtitle text box
        header_box = slide.shapes.add_textbox(Inches(0.98), Inches(0.32), Inches(10.6), Inches(0.85))
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
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_NAVY_SUB
        p2.space_before = Pt(2)

        # Slide Number Badge
        num_box = slide.shapes.add_textbox(Inches(11.8), Inches(0.35), Inches(0.733), Inches(0.35))
        ntf = num_box.text_frame
        ntf.margin_left = ntf.margin_top = ntf.margin_right = ntf.margin_bottom = 0
        np = ntf.paragraphs[0]
        np.text = f"{slide_num} / 3"
        np.alignment = PP_ALIGN.RIGHT
        np.font.name = FONT_MAIN
        np.font.size = Pt(11)
        np.font.bold = True
        np.font.color.rgb = C_TEXT_MUTED

        # Thin clean horizontal dividing rule
        rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.24), Inches(11.733), Inches(0.015))
        rule.fill.solid()
        rule.fill.fore_color.rgb = C_BORDER_MID
        rule.line.fill.background()

    def add_pill_badge(slide, left, top, width, height, text, bg_color):
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        pill.fill.solid()
        pill.fill.fore_color.rgb = bg_color
        pill.line.fill.background()
        ptf = pill.text_frame
        ptf.word_wrap = False
        ptf.margin_left = ptf.margin_right = ptf.margin_top = ptf.margin_bottom = 0
        pp = ptf.paragraphs[0]
        pp.text = text
        pp.alignment = PP_ALIGN.CENTER
        pp.font.name = FONT_MAIN
        pp.font.size = Pt(9)
        pp.font.bold = True
        pp.font.color.rgb = C_WHITE
        return pill

    # =========================================================================
    # SLIDE 1: INTRODUCTION AND PROJECT OVERVIEW (Reference Image 1)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s1)

    render_header(s1,
                  "Low-Power Scan-Based LBIST Using MIPS32 Architecture",
                  "VL405 — Design for Testability (DFT) Laboratory Project",
                  1)

    # 3 Member Cards (Top Row)
    members_data = [
        ("Harshitha Modekurty (B23272)", "MIPS32 Core & Scan Architecture", C_BLUE),
        ("Nishi Kumari (B24495)", "PRPG & Toggle-Rate Control", C_TEAL),
        ("Gaurav Tiwari (B24483)", "LBIST Controller & Fault Analysis", C_ORANGE)
    ]
    card_w = Inches(3.75)
    card_h = Inches(0.78)
    card_y = Inches(1.36)

    for idx, (name, role, acc_color) in enumerate(members_data):
        card_x = Inches(0.8) + idx * (card_w + Inches(0.24))
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card_x, card_y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = acc_color
        card.line.width = Pt(1.5)

        tb = s1.shapes.add_textbox(card_x + Inches(0.15), card_y + Inches(0.10), card_w - Inches(0.3), card_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p = tf.paragraphs[0]
        p.text = name
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_MAIN
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_HEADING

        p2 = tf.add_paragraph()
        p2.text = role
        p2.alignment = PP_ALIGN.CENTER
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(9)
        p2.font.color.rgb = acc_color
        p2.font.bold = True
        p2.space_before = Pt(2)

    # Full-Width Introduction Banner Strip
    intro_y = Inches(2.26)
    intro_w = Inches(11.733)
    intro_h = Inches(0.68)
    intro_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), intro_y, intro_w, intro_h)
    intro_card.fill.solid()
    intro_card.fill.fore_color.rgb = C_WHITE
    intro_card.line.color.rgb = C_CARD_BORDER
    intro_card.line.width = Pt(1.5)

    add_pill_badge(s1, Inches(0.95), intro_y + Inches(0.14), Inches(1.6), Inches(0.40), "INTRODUCTION", C_PILL_BLUE)

    itb = s1.shapes.add_textbox(Inches(2.72), intro_y + Inches(0.12), Inches(9.65), Inches(0.45))
    itf = itb.text_frame
    itf.word_wrap = True
    itf.margin_top = itf.margin_bottom = itf.margin_left = itf.margin_right = 0
    ip = itf.paragraphs[0]
    ip.text = "Logic Built-In Self-Test (LBIST) enables on-chip testing using pseudorandom patterns and response compaction. Scan-based testing improves controllability and observability for complex designs such as a MIPS32 processor."
    ip.font.name = FONT_MAIN
    ip.font.size = Pt(9.2)
    ip.font.color.rgb = C_TEXT_DARK

    # Bottom Left: Problem Statement Card
    prob_x = Inches(0.8)
    prob_y = Inches(3.06)
    prob_w = Inches(4.3)
    prob_h = Inches(4.18)

    pbox = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, prob_x, prob_y, prob_w, prob_h)
    pbox.fill.solid()
    pbox.fill.fore_color.rgb = RGBColor(255, 245, 245) # Soft pinkish-white matching ref
    pbox.line.color.rgb = RGBColor(252, 165, 165)
    pbox.line.width = Pt(1.5)

    add_pill_badge(s1, prob_x + Inches(0.18), prob_y + Inches(0.14), Inches(2.1), Inches(0.34), "PROBLEM STATEMENT", C_PILL_RED)

    ptb = s1.shapes.add_textbox(prob_x + Inches(0.22), prob_y + Inches(0.58), prob_w - Inches(0.44), prob_h - Inches(0.70))
    ptf = ptb.text_frame
    ptf.word_wrap = True
    ptf.margin_top = ptf.margin_bottom = ptf.margin_left = ptf.margin_right = 0

    prob_items = [
        ("High switching activity:", " Conventional LFSR patterns can produce frequent transitions during scan shifting."),
        ("Power impact:", " High scan-shift activity increases dynamic power and may cause IR-drop and delay variation."),
        ("Thermal stress:", " Excessive test activity can create local heating and false test failures."),
        ("Dynamic Power Formula:", " P_dynamic = α · C_eff · V_DD² · f_shift  --> Controlling activity factor α directly cuts test power.")
    ]

    for i, (hd, desc) in enumerate(prob_items):
        p = ptf.add_paragraph()
        if i > 0:
            p.space_before = Pt(12)
        r1 = p.add_run()
        r1.text = hd
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = C_PILL_RED if i < 3 else C_NAVY_HEADING

        r2 = p.add_run()
        r2.text = desc
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(9)
        r2.font.color.rgb = C_TEXT_DARK

    # Bottom Right: Proposed Approach & Objectives Card
    sol_x = Inches(5.34)
    sol_y = Inches(3.06)
    sol_w = Inches(7.193)
    sol_h = Inches(4.18)

    sbox = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sol_x, sol_y, sol_w, sol_h)
    sbox.fill.solid()
    sbox.fill.fore_color.rgb = RGBColor(240, 253, 244) # Soft light-green matching ref
    sbox.line.color.rgb = RGBColor(167, 243, 208)
    sbox.line.width = Pt(1.5)

    add_pill_badge(s1, sol_x + Inches(0.18), sol_y + Inches(0.14), Inches(3.2), Inches(0.34), "PROPOSED APPROACH & OBJECTIVES", C_PILL_GREEN)

    # Sub-card inside Proposed Approach
    subcard_y = sol_y + Inches(0.56)
    subcard_w = sol_w - Inches(0.36)
    subcard_h = Inches(0.68)
    sc = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sol_x + Inches(0.18), subcard_y, subcard_w, subcard_h)
    sc.fill.solid()
    sc.fill.fore_color.rgb = C_WHITE
    sc.line.color.rgb = C_BORDER_MID
    sc.line.width = Pt(1)

    sctb = s1.shapes.add_textbox(sol_x + Inches(0.30), subcard_y + Inches(0.12), subcard_w - Inches(0.24), subcard_h - Inches(0.24))
    sctf = sctb.text_frame
    sctf.word_wrap = True
    sctf.margin_top = sctf.margin_bottom = sctf.margin_left = sctf.margin_right = 0
    scp = sctf.paragraphs[0]
    scp.text = "Programmable toggle-rate control modifies PRPG-generated patterns to reduce unnecessary scan-shift transitions."
    scp.font.name = FONT_MAIN
    scp.font.size = Pt(9.5)
    scp.font.bold = True
    scp.font.color.rgb = C_TEXT_DARK

    # 4 Numbered Items (1 to 4)
    obj_items = [
        "Generate pseudorandom patterns using an LFSR-based PRPG.",
        "Control switching activity with a programmable pattern modifier.",
        "Apply modified patterns to the MIPS32 scan chains.",
        "Evaluate toggle rate, scan activity, power and test effectiveness."
    ]

    for idx, obj_txt in enumerate(obj_items):
        oy = sol_y + Inches(1.38) + idx * Inches(0.55)
        # Number badge
        nb = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sol_x + Inches(0.22), oy, Inches(0.34), Inches(0.34))
        nb.fill.solid()
        nb.fill.fore_color.rgb = C_WHITE
        nb.line.color.rgb = C_PILL_GREEN
        nb.line.width = Pt(1.5)
        nbtf = nb.text_frame
        nbp = nbtf.paragraphs[0]
        nbp.text = str(idx + 1)
        nbp.alignment = PP_ALIGN.CENTER
        nbp.font.name = FONT_MAIN
        nbp.font.size = Pt(9.5)
        nbp.font.bold = True
        nbp.font.color.rgb = C_PILL_GREEN

        # Text box next to number badge
        otb = s1.shapes.add_textbox(sol_x + Inches(0.68), oy - Inches(0.02), subcard_w - Inches(0.55), Inches(0.38))
        otf = otb.text_frame
        otf.word_wrap = True
        otf.margin_top = otf.margin_bottom = otf.margin_left = otf.margin_right = 0
        op = otf.paragraphs[0]
        op.text = obj_txt
        op.font.name = FONT_MAIN
        op.font.size = Pt(9)
        op.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 2: PROPOSED ARCHITECTURE AND WORKING FLOW (Reference Image 2)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s2)

    render_header(s2,
                  "Proposed LBIST Architecture and Methodology",
                  "Overall test flow and hardware working principle",
                  2)

    # Master Architecture Container (Top Section)
    arch_x = Inches(0.8)
    arch_y = Inches(1.36)
    arch_w = Inches(11.733)
    arch_h = Inches(3.22)

    acard = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, arch_x, arch_y, arch_w, arch_h)
    acard.fill.solid()
    acard.fill.fore_color.rgb = C_WHITE
    acard.line.color.rgb = C_CARD_BORDER
    acard.line.width = Pt(1.5)

    add_pill_badge(s2, arch_x + Inches(0.18), arch_y + Inches(0.12), Inches(2.7), Inches(0.34), "OVERALL LBIST ARCHITECTURE", C_PILL_BLUE)

    # Center Top Block: LBIST Controller (FSM)
    fsm_w = Inches(3.5)
    fsm_h = Inches(0.52)
    fsm_x = arch_x + (arch_w - fsm_w) / 2
    fsm_y = arch_y + Inches(0.40)

    fsm_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, fsm_x, fsm_y, fsm_w, fsm_h)
    fsm_box.fill.solid()
    fsm_box.fill.fore_color.rgb = RGBColor(245, 243, 255) # Light purple
    fsm_box.line.color.rgb = C_PURPLE
    fsm_box.line.width = Pt(1.5)

    fsmtb = s2.shapes.add_textbox(fsm_x, fsm_y + Inches(0.08), fsm_w, fsm_h - Inches(0.16))
    fsmtf = fsmtb.text_frame
    fsmp = fsmtf.paragraphs[0]
    fsmp.text = "LBIST Controller (FSM)"
    fsmp.alignment = PP_ALIGN.CENTER
    fsmp.font.name = FONT_MAIN
    fsmp.font.size = Pt(10.5)
    fsmp.font.bold = True
    fsmp.font.color.rgb = C_NAVY_HEADING

    # Control Signal Distribution Horizontal Purple Line
    bus_y = fsm_y + fsm_h + Inches(0.32)
    bus_x1 = arch_x + Inches(1.15)
    bus_x2 = arch_x + Inches(10.55)
    
    # Stem from Controller down to bus
    stem = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, fsm_x + fsm_w / 2 - Inches(0.01), fsm_y + fsm_h, Inches(0.02), Inches(0.32))
    stem.fill.solid()
    stem.fill.fore_color.rgb = C_PURPLE
    stem.line.fill.background()

    # Bus line
    bus = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, bus_x1, bus_y, bus_x2 - bus_x1, Inches(0.02))
    bus.fill.solid()
    bus.fill.fore_color.rgb = C_PURPLE
    bus.line.fill.background()

    # 4 Control Drop Arrows with exact labels matching Reference Image 2
    drops = [
        (arch_x + Inches(1.15), "seed / enable"),
        (arch_x + Inches(3.05), "target rate"),
        (arch_x + Inches(5.10), "scan / test clock"),
        (arch_x + Inches(8.80), "MISR enable")
    ]

    for dx, dlabel in drops:
        # Drop line from bus
        d_line = s2.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, dx - Inches(0.06), bus_y, Inches(0.12), Inches(0.24))
        d_line.fill.solid()
        d_line.fill.fore_color.rgb = C_PURPLE
        d_line.line.fill.background()

        # Text label above drop line (cleanly centered in gap)
        ltb = s2.shapes.add_textbox(dx - Inches(0.8), bus_y - Inches(0.24), Inches(1.6), Inches(0.22))
        ltf = ltb.text_frame
        ltf.margin_top = ltf.margin_bottom = ltf.margin_left = ltf.margin_right = 0
        lp = ltf.paragraphs[0]
        lp.text = dlabel
        lp.alignment = PP_ALIGN.CENTER
        lp.font.name = FONT_MAIN
        lp.font.size = Pt(7.5)
        lp.font.bold = True
        lp.font.color.rgb = C_PURPLE

    # 6 Datapath Blocks in a Horizontal Row
    row_y = bus_y + Inches(0.26)
    blk_w = Inches(1.66)
    blk_h = Inches(0.95)
    blk_gap = Inches(0.28)
    row_start_x = arch_x + Inches(0.22)

    blocks_data = [
        ("PRPG", "(LFSR)", "Pseudorandom\npatterns", C_PILL_GREEN, RGBColor(240, 253, 244)),
        ("Pattern", "Modifier", "Toggle-rate\ncontrol", C_TEAL, RGBColor(240, 253, 250)),
        ("MIPS32", "Scan Chains", "Circuit under\ntest (CUT)", C_BLUE, RGBColor(239, 246, 255)),
        ("Response", "Capture", "Capture test\nresponse", C_ORANGE, RGBColor(255, 251, 235)),
        ("MISR", "(16-bit)", "Response\ncompaction", C_AMBER_DARK, RGBColor(255, 251, 235)),
        ("Signature", "Analysis", "PASS / FAIL", C_PURPLE, RGBColor(245, 243, 255))
    ]

    for i, (l1, l2, desc, b_color, bg_tint) in enumerate(blocks_data):
        bx = row_start_x + i * (blk_w + blk_gap)
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, row_y, blk_w, blk_h)
        box.fill.solid()
        box.fill.fore_color.rgb = bg_tint
        box.line.color.rgb = b_color
        box.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(bx + Inches(0.04), row_y + Inches(0.06), blk_w - Inches(0.08), blk_h - Inches(0.12))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p1 = tf.paragraphs[0]
        p1.text = f"{l1} {l2}"
        p1.alignment = PP_ALIGN.CENTER
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY_HEADING

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.alignment = PP_ALIGN.CENTER
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(7.5)
        p2.font.color.rgb = C_TEXT_MUTED
        p2.space_before = Pt(2)

        # Horizontal connecting arrow between blocks
        if i < len(blocks_data) - 1:
            arr_x = bx + blk_w + Inches(0.04)
            arr = s2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arr_x, row_y + Inches(0.38), Inches(0.20), Inches(0.22))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_BORDER_MID
            arr.line.fill.background()

    # Bottom Row: 2 Balanced Cards (Working Principle & Key Components)
    bot_y = Inches(4.70)
    bot_h = Inches(2.54)

    # Bottom Left: Working Principle Card
    wp_w = Inches(5.7)
    wp_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, arch_x, bot_y, wp_w, bot_h)
    wp_box.fill.solid()
    wp_box.fill.fore_color.rgb = C_WHITE
    wp_box.line.color.rgb = C_CARD_BORDER
    wp_box.line.width = Pt(1.5)

    add_pill_badge(s2, arch_x + Inches(0.18), bot_y + Inches(0.12), Inches(2.2), Inches(0.34), "WORKING PRINCIPLE", C_PILL_BLUE)

    wp_steps = [
        ("1", "Initialize", "Reset LBIST and load the PRPG seed.", C_PILL_BLUE),
        ("2", "Generate & modify", "Generate patterns and regulate toggle rate.", C_PILL_GREEN),
        ("3", "Scan & capture", "Shift patterns into scan chains and capture response.", C_BLUE),
        ("4", "Compact & analyze", "MISR compacts response; compare final signature.", C_ORANGE)
    ]

    for idx, (num, tag, detail, s_col) in enumerate(wp_steps):
        sy = bot_y + Inches(0.56) + idx * Inches(0.46)
        
        # Badge
        b = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, arch_x + Inches(0.20), sy, Inches(0.30), Inches(0.30))
        b.fill.solid()
        b.fill.fore_color.rgb = s_col
        b.line.fill.background()
        btf = b.text_frame
        bp = btf.paragraphs[0]
        bp.text = num
        bp.alignment = PP_ALIGN.CENTER
        bp.font.name = FONT_MAIN
        bp.font.size = Pt(8.5)
        bp.font.bold = True
        bp.font.color.rgb = C_WHITE

        # Text
        stb = s2.shapes.add_textbox(arch_x + Inches(0.58), sy - Inches(0.02), wp_w - Inches(0.70), Inches(0.36))
        stf = stb.text_frame
        stf.word_wrap = True
        stf.margin_top = stf.margin_bottom = stf.margin_left = stf.margin_right = 0
        sp = stf.paragraphs[0]
        r1 = sp.add_run()
        r1.text = tag + "   "
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY_HEADING

        r2 = sp.add_run()
        r2.text = detail
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(8.2)
        r2.font.color.rgb = C_TEXT_DARK

    # Bottom Right: Key Components Card
    kc_x = Inches(6.833)
    kc_w = Inches(5.7)
    kc_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, kc_x, bot_y, kc_w, bot_h)
    kc_box.fill.solid()
    kc_box.fill.fore_color.rgb = C_WHITE
    kc_box.line.color.rgb = C_CARD_BORDER
    kc_box.line.width = Pt(1.5)

    add_pill_badge(s2, kc_x + Inches(0.18), bot_y + Inches(0.12), Inches(2.0), Inches(0.34), "KEY COMPONENTS", C_PILL_BLUE)

    kc_items = [
        ("LBIST Controller", "Test sequencing and control signals"),
        ("PRPG + Modifier", "Pattern generation and toggle-rate control"),
        ("MIPS32 Scan Chains", "Apply test patterns to the CUT"),
        ("MISR + Analyzer", "Response compaction and PASS/FAIL")
    ]

    for idx, (comp, role) in enumerate(kc_items):
        ky = bot_y + Inches(0.56) + idx * Inches(0.46)
        ktb = s2.shapes.add_textbox(kc_x + Inches(0.20), ky, kc_w - Inches(0.40), Inches(0.36))
        ktf = ktb.text_frame
        ktf.word_wrap = True
        ktf.margin_top = ktf.margin_bottom = ktf.margin_left = ktf.margin_right = 0
        kp = ktf.paragraphs[0]
        r1 = kp.add_run()
        r1.text = f"{comp:<22} "
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY_HEADING

        r2 = kp.add_run()
        r2.text = role
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(8.2)
        r2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 3: EXPERIMENTAL RESULTS AND CONCLUSION (Combined Page 3 & 4)
    # Exact results only. No graphs or waveforms. 
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s3)

    render_header(s3,
                  "Experimental Results and Conclusion",
                  "Toggle-rate control, scan-shift activity, Vivado synthesis summary and final scope",
                  3)

    col_w = Inches(5.7)

    # -------------------------------------------------------------------------
    # LEFT COLUMN: Results Table & Vivado Synthesis Summary
    # -------------------------------------------------------------------------
    left_x = Inches(0.8)

    # 1. Measured Toggle-Rate Results Card
    tbl_y = Inches(1.36)
    tbl_h = Inches(3.26)
    tbox = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, tbl_y, col_w, tbl_h)
    tbox.fill.solid()
    tbox.fill.fore_color.rgb = C_WHITE
    tbox.line.color.rgb = C_CARD_BORDER
    tbox.line.width = Pt(1.5)

    add_pill_badge(s3, left_x + Inches(0.18), tbl_y + Inches(0.12), Inches(3.0), Inches(0.34), "MEASURED TOGGLE-RATE RESULTS", C_PILL_BLUE)

    # Results Table (Exact verified numbers)
    table_shape = s3.shapes.add_table(8, 5, left_x + Inches(0.14), tbl_y + Inches(0.52), col_w - Inches(0.28), Inches(2.20))
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
        p.font.size = Pt(8)
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
            p.font.size = Pt(7.5)
            if col_idx == 4 and "%" in val:
                p.font.bold = True
                p.font.color.rgb = C_PILL_GREEN
            elif col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_NAVY_HEADING
            else:
                p.font.color.rgb = C_TEXT_DARK

    # Clarification note below table
    notetb = s3.shapes.add_textbox(left_x + Inches(0.18), tbl_y + Inches(2.78), col_w - Inches(0.36), Inches(0.42))
    notetf = notetb.text_frame
    notetf.word_wrap = True
    notetf.margin_top = notetf.margin_bottom = notetf.margin_left = notetf.margin_right = 0
    notep = notetf.paragraphs[0]
    notep.text = "Power-saving values are reported for total on-chip scan-shift power in the supplied results."
    notep.font.name = FONT_MAIN
    notep.font.size = Pt(7.5)
    notep.font.color.rgb = C_TEXT_MUTED

    # 2. Vivado Synthesis Summary Card
    syn_y = Inches(4.74)
    syn_h = Inches(2.50)
    syn_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, syn_y, col_w, syn_h)
    syn_box.fill.solid()
    syn_box.fill.fore_color.rgb = C_WHITE
    syn_box.line.color.rgb = C_CARD_BORDER
    syn_box.line.width = Pt(1.5)

    add_pill_badge(s3, left_x + Inches(0.18), syn_y + Inches(0.12), Inches(3.0), Inches(0.34), "VIVADO SYNTHESIS SUMMARY", C_PILL_BLUE)

    # 4 Metric Blocks inside Synthesis Card
    vmetrics = [
        ("Run status", "Complete", C_PILL_GREEN),
        ("LUTs", "5,565", C_PILL_BLUE),
        ("Flip-flops", "1,287", C_PILL_BLUE),
        ("BRAM / URAM / DSP", "0 / 0 / 0", C_TEXT_DARK)
    ]
    vm_w = Inches(1.24)
    vm_h = Inches(0.90)
    vm_gap = Inches(0.12)
    vm_start_x = left_x + Inches(0.16)
    vm_y = syn_y + Inches(0.54)

    for idx, (m_lbl, m_val, m_col) in enumerate(vmetrics):
        mx = vm_start_x + idx * (vm_w + vm_gap)
        mb = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, mx, vm_y, vm_w, vm_h)
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
        mp1.font.size = Pt(7.5)
        mp1.font.color.rgb = C_TEXT_MUTED

        mp2 = mbtf.add_paragraph()
        mp2.text = m_val
        mp2.alignment = PP_ALIGN.CENTER
        mp2.font.name = FONT_MAIN
        mp2.font.size = Pt(11)
        mp2.font.bold = True
        mp2.font.color.rgb = m_col
        mp2.space_before = Pt(4)

    # Synthesis Key Notes
    sntb = s3.shapes.add_textbox(left_x + Inches(0.20), syn_y + Inches(1.54), col_w - Inches(0.40), Inches(0.85))
    sntf = sntb.text_frame
    sntf.word_wrap = True
    sntf.margin_top = sntf.margin_bottom = sntf.margin_left = sntf.margin_right = 0
    snp = sntf.paragraphs[0]
    snp.text = "• Implementation: Vivado synthesis completed with 5,565 LUTs, 1,287 FFs, and 0 dedicated memory/DSP blocks for the top-level MIPS32 + Scan LBIST core."
    snp.font.name = FONT_MAIN
    snp.font.size = Pt(8)
    snp.font.color.rgb = C_TEXT_DARK

    snp2 = sntf.add_paragraph()
    snp2.text = "• Verification Status: Behavioral simulation & out-of-context RTL synthesis verified; place-and-route I/O closure scheduled for hardware integration."
    snp2.font.name = FONT_MAIN
    snp2.font.size = Pt(8)
    snp2.font.color.rgb = C_TEXT_DARK
    snp2.space_before = Pt(3)

    # -------------------------------------------------------------------------
    # RIGHT COLUMN: Key Project Achievements & Future Scope (Merged from Page 4)
    # -------------------------------------------------------------------------
    right_x = Inches(6.833)

    # 1. Key Project Achievements Card (Top)
    ach_y = Inches(1.36)
    ach_h = Inches(3.26)
    ach_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, ach_y, col_w, ach_h)
    ach_box.fill.solid()
    ach_box.fill.fore_color.rgb = C_WHITE
    ach_box.line.color.rgb = RGBColor(167, 243, 208)
    ach_box.line.width = Pt(1.5)

    add_pill_badge(s3, right_x + Inches(0.18), ach_y + Inches(0.12), Inches(3.0), Inches(0.34), "KEY PROJECT ACHIEVEMENTS", C_PILL_GREEN)

    atb = s3.shapes.add_textbox(right_x + Inches(0.22), ach_y + Inches(0.54), col_w - Inches(0.44), ach_h - Inches(0.66))
    atf = atb.text_frame
    atf.word_wrap = True
    atf.margin_top = atf.margin_bottom = atf.margin_left = atf.margin_right = 0

    ach_items = [
        ("Programmable toggle-rate control:", " Modified PRPG patterns were evaluated at target settings from 10% to 60%."),
        ("Reduced scan-shift activity:", " The reported modified scan toggle rate reached 8.67% at the 10% target setting."),
        ("Reported power reduction:", " The supplied results report up to 84.35% reduction in total on-chip scan-shift power at the 10% setting."),
        ("Vivado synthesis:", " Synthesis completed with 5,565 LUTs, 1,287 flip-flops, and zero BRAM, URAM, and DSP usage.")
    ]

    for i, (ahd, adesc) in enumerate(ach_items):
        p = atf.add_paragraph()
        if i > 0:
            p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = "• " + ahd
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = C_PILL_GREEN

        r2 = p.add_run()
        r2.text = adesc
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(8.2)
        r2.font.color.rgb = C_TEXT_DARK

    # 2. Future Scope & Integration Card (Bottom)
    fut_y = Inches(4.74)
    fut_h = Inches(2.50)
    fut_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, fut_y, col_w, fut_h)
    fut_box.fill.solid()
    fut_box.fill.fore_color.rgb = C_WHITE
    fut_box.line.color.rgb = RGBColor(191, 219, 254)
    fut_box.line.width = Pt(1.5)

    add_pill_badge(s3, right_x + Inches(0.18), fut_y + Inches(0.12), Inches(3.0), Inches(0.34), "FUTURE SCOPE & INTEGRATION", C_PILL_BLUE)

    ftb = s3.shapes.add_textbox(right_x + Inches(0.22), fut_y + Inches(0.52), col_w - Inches(0.44), fut_h - Inches(0.60))
    ftf = ftb.text_frame
    ftf.word_wrap = True
    ftf.margin_top = ftf.margin_bottom = ftf.margin_left = ftf.margin_right = 0

    fut_items = [
        ("Complete fault-coverage analysis:", " Evaluate stuck-at and transition-fault coverage using the integrated LBIST flow."),
        ("Validate signature checking:", " Run fault-free and fault-injected tests and verify MISR signatures against golden references."),
        ("Implementation closure:", " Complete timing analysis and place-and-route evaluation for the integrated design."),
        ("Further power evaluation:", " Compare scan-shift activity and power across target rates and test configurations.")
    ]

    for i, (fhd, fdesc) in enumerate(fut_items):
        p = ftf.add_paragraph()
        if i > 0:
            p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = "• " + fhd
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = C_PILL_BLUE

        r2 = p.add_run()
        r2.text = fdesc
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(8.2)
        r2.font.color.rgb = C_TEXT_DARK

    # Save presentation
    output_filename = "VL405_LBIST_Project_Presentation.pptx"
    prs.save(output_filename)
    print(f"[SUCCESS] Exact 3-Slide Presentation compiled to: {output_filename}")

if __name__ == "__main__":
    build_presentation()
