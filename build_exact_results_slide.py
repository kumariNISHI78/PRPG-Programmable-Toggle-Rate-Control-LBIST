import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_slide():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.50)
    blank_layout = prs.slide_layouts[6]

    FONT_MAIN = "Arial"
    C_NAVY_HEADING = RGBColor(23, 50, 77)    # #17324D
    C_NAVY_SUB     = RGBColor(82, 103, 125)  # #52677D
    C_TEXT_DARK    = RGBColor(30, 41, 59)    # #1E293B
    C_TEXT_MUTED   = RGBColor(100, 116, 139) # #64748B
    C_BLUE         = RGBColor(37, 99, 235)   # #2563EB
    C_WHITE        = RGBColor(255, 255, 255)
    C_BG_PAGE      = RGBColor(250, 252, 255)
    C_CARD_BORDER  = RGBColor(226, 232, 240)
    C_BORDER_MID   = RGBColor(203, 213, 225)
    
    C_PILL_BLUE    = RGBColor(30, 58, 138)   # Deep Blue
    C_PILL_GREEN   = RGBColor(21, 128, 61)   # Forest Green
    C_PILL_ORANGE  = RGBColor(194, 65, 12)   # Dark Orange
    C_PILL_TEAL    = RGBColor(15, 118, 110)  # Teal

    s = prs.slides.add_slide(blank_layout)

    # Background
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG_PAGE
    bg.line.fill.background()

    # Header
    left_m = Inches(0.8)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_m, Inches(0.36), Inches(0.08), Inches(0.56))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_BLUE
    bar.line.fill.background()

    tb = s.shapes.add_textbox(left_m + Inches(0.18), Inches(0.32), Inches(11.4), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p1 = tf.paragraphs[0]
    p1.text = "COMPILED PROJECT RESULTS & PERFORMANCE ANALYSIS"
    p1.font.name = FONT_MAIN
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY_HEADING

    p2 = tf.add_paragraph()
    p2.text = "32-bit PRPG • Four-lane scan architecture • Programmable activity control • Integrated synthesis and LBIST analysis"
    p2.font.name = FONT_MAIN
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_NAVY_SUB
    p2.space_before = Pt(3)

    div = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_m, Inches(1.18), Inches(11.733), Inches(0.01))
    div.fill.solid()
    div.fill.fore_color.rgb = RGBColor(226, 232, 240)
    div.line.fill.background()

    def add_pill(x, y, w, h, text, col):
        p_shape = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        p_shape.fill.solid()
        p_shape.fill.fore_color.rgb = col
        p_shape.line.fill.background()
        tf_ = p_shape.text_frame
        tf_.margin_top = tf_.margin_bottom = tf_.margin_left = tf_.margin_right = 0
        p = tf_.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_MAIN
        p.font.size = Pt(8.2)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        return p_shape

    col_w = Inches(5.70)
    left_x = Inches(0.80)
    right_x = Inches(6.833)

    # =========================================================================
    # CARD 1 (Top Left): 1. PRPG, LFSR & SCAN-ACTIVITY RESULTS
    # =========================================================================
    c1_y = Inches(1.26)
    c1_h = Inches(2.74)
    box1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, c1_y, col_w, c1_h)
    box1.fill.solid()
    box1.fill.fore_color.rgb = C_WHITE
    box1.line.color.rgb = RGBColor(167, 243, 208)
    box1.line.width = Pt(1.5)

    add_pill(left_x + Inches(0.14), c1_y + Inches(0.08), Inches(3.60), Inches(0.24), "1. PRPG, LFSR & SCAN-ACTIVITY RESULTS", C_PILL_GREEN)

    # Polynomial Equation
    eq_tb = s.shapes.add_textbox(left_x + Inches(0.14), c1_y + Inches(0.34), col_w - Inches(0.28), Inches(0.20))
    eq_tf = eq_tb.text_frame
    eq_tf.margin_top = eq_tf.margin_bottom = eq_tf.margin_left = eq_tf.margin_right = 0
    ep = eq_tf.paragraphs[0]
    ep.alignment = PP_ALIGN.CENTER
    ep.text = "P(x) = x³² + x²² + x² + x + 1"
    ep.font.name = FONT_MAIN
    ep.font.size = Pt(11)
    ep.font.bold = True
    ep.font.color.rgb = C_NAVY_HEADING

    sub_tb = s.shapes.add_textbox(left_x + Inches(0.14), c1_y + Inches(0.54), col_w - Inches(0.28), Inches(0.16))
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
        b_shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, flow_y, fb_w, fb_h)
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
            arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, ax + Inches(0.02), flow_y + Inches(0.04), farr_w - Inches(0.04), Inches(0.12))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_PILL_GREEN
            arr.line.fill.background()

    # Table: 8 rows x 4 columns
    tbl_y = c1_y + Inches(0.96)
    tbl_h = Inches(1.50)
    table_shape = s.shapes.add_table(8, 4, left_x + Inches(0.14), tbl_y, col_w - Inches(0.28), tbl_h)
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
    tn_tb = s.shapes.add_textbox(left_x + Inches(0.14), c1_y + Inches(2.50), col_w - Inches(0.28), Inches(0.18))
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
    box2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, c1_y, col_w, c1_h)
    box2.fill.solid()
    box2.fill.fore_color.rgb = C_WHITE
    box2.line.color.rgb = RGBColor(191, 219, 254)
    box2.line.width = Pt(1.5)

    add_pill(right_x + Inches(0.14), c1_y + Inches(0.08), Inches(3.60), Inches(0.24), "2. MIPS32 CORE & SCAN ARCHITECTURE", C_PILL_BLUE)

    m2_tb = s.shapes.add_textbox(right_x + Inches(0.18), c1_y + Inches(0.38), col_w - Inches(0.36), Inches(1.56))
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
        mb = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, m2m_start_x + i * (m2m_w + m2m_gap), m2m_y, m2m_w, m2m_h)
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
    box3 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, c3_y, col_w, c3_h)
    box3.fill.solid()
    box3.fill.fore_color.rgb = C_WHITE
    box3.line.color.rgb = C_CARD_BORDER
    box3.line.width = Pt(1.5)

    add_pill(left_x + Inches(0.14), c3_y + Inches(0.08), Inches(3.60), Inches(0.24), "3. INTEGRATED FPGA SYNTHESIS (VIVADO)", C_PILL_TEAL)

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
        mb = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, vm_start_x + idx * (vm_w + vm_gap), vm_y, vm_w, vm_h)
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
    sntb = s.shapes.add_textbox(left_x + Inches(0.18), c3_y + Inches(1.00), col_w - Inches(0.36), Inches(1.32))
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
    box4 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, c3_y, col_w, c3_h)
    box4.fill.solid()
    box4.fill.fore_color.rgb = C_WHITE
    box4.line.color.rgb = RGBColor(254, 215, 170)
    box4.line.width = Pt(1.5)

    add_pill(right_x + Inches(0.14), c3_y + Inches(0.08), Inches(3.80), Inches(0.24), "4. LBIST CONTROLLER, MISR & FAULT ANALYSIS", C_PILL_ORANGE)

    m4_tb = s.shapes.add_textbox(right_x + Inches(0.18), c3_y + Inches(0.36), col_w - Inches(0.36), Inches(1.56))
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
    alias_box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x + Inches(0.18), c3_y + Inches(1.98), col_w - Inches(0.36), Inches(0.30))
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
    foot_tb = s.shapes.add_textbox(left_m, Inches(6.50), Inches(11.733), Inches(0.18))
    foot_tf = foot_tb.text_frame
    foot_tf.margin_top = foot_tf.margin_bottom = foot_tf.margin_left = foot_tf.margin_right = 0
    fp_ = foot_tf.paragraphs[0]
    fp_.alignment = PP_ALIGN.CENTER
    fp_.text = "Scan-lane transition reduction and dynamic-power reduction are different metrics; fault coverage is a modeled stuck-at result."
    fp_.font.name = FONT_MAIN
    fp_.font.size = Pt(6.5)
    fp_.font.color.rgb = C_TEXT_MUTED

    # Bottom Banner (with VL405 project subtitle)
    thx_y = Inches(6.70)
    thx_h = Inches(0.56)
    thx_w = Inches(11.733)
    thx_box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_m, thx_y, thx_w, thx_h)
    thx_box.fill.solid()
    thx_box.fill.fore_color.rgb = RGBColor(238, 242, 255)
    thx_box.line.color.rgb = C_BLUE
    thx_box.line.width = Pt(1.5)

    ttb = s.shapes.add_textbox(left_m + Inches(0.1), thx_y + Inches(0.06), thx_w - Inches(0.2), thx_h - Inches(0.12))
    ttf = ttb.text_frame
    ttf.margin_top = ttf.margin_bottom = ttf.margin_left = ttf.margin_right = 0
    tp1 = ttf.paragraphs[0]
    tp1.text = "Thank You! Questions & Discussion Welcome"
    tp1.alignment = PP_ALIGN.CENTER
    tp1.font.name = FONT_MAIN
    tp1.font.size = Pt(10.5)
    tp1.font.bold = True
    tp1.font.color.rgb = C_NAVY_HEADING

    tp2 = ttf.add_paragraph()
    tp2.text = "VL405 Design for Testability Laboratory Project"
    tp2.alignment = PP_ALIGN.CENTER
    tp2.font.name = FONT_MAIN
    tp2.font.size = Pt(8.2)
    tp2.font.bold = True
    tp2.font.color.rgb = C_NAVY_SUB
    tp2.space_before = Pt(2)

    # Save
    prs.save("VL405_LBIST_Final_Results_Slide.pptx")
    print("[SUCCESS] Recreated exact results slide: VL405_LBIST_Final_Results_Slide.pptx")

if __name__ == "__main__":
    build_slide()

