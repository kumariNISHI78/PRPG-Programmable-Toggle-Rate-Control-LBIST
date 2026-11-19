import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_standalone_results_slide():
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
    C_PILL_GREEN   = RGBColor(21, 128, 61)   # Forest Green
    C_PILL_PURPLE  = RGBColor(109, 40, 217)  # Violet
    C_PILL_ORANGE  = RGBColor(194, 65, 12)   # Dark Orange

    def apply_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG_PAGE
        bg.line.fill.background()
        return bg

    def render_header(slide, title_text, subtitle_text):
        left_m = Inches(0.8)
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_m, Inches(0.36), Inches(0.08), Inches(0.56))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_BLUE
        bar.line.fill.background()

        tb = slide.shapes.add_textbox(left_m + Inches(0.18), Inches(0.32), Inches(11.4), Inches(0.85))
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
        p.font.size = Pt(8.2)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        return pill

    # Build Slide
    s = prs.slides.add_slide(blank_layout)
    apply_slide_background(s)

    render_header(s,
                  "Compiled Project Results & Performance Analysis",
                  "Comprehensive DFT evaluation: MIPS32 scan architecture, PRPG toggle control, 100% fault coverage & Vivado synthesis")

    col_w = Inches(5.70)
    left_x = Inches(0.80)
    right_x = Inches(6.833)

    # -------------------------------------------------------------------------
    # CARD 1 (Top Left): PRPG & TOGGLE-RATE CONTROL RESULTS
    # -------------------------------------------------------------------------
    c1_y = Inches(1.34)
    c1_h = Inches(2.68)
    box1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, c1_y, col_w, c1_h)
    box1.fill.solid()
    box1.fill.fore_color.rgb = C_WHITE
    box1.line.color.rgb = RGBColor(167, 243, 208)
    box1.line.width = Pt(1.5)

    add_pill_badge(s, left_x + Inches(0.18), c1_y + Inches(0.10), Inches(3.6), Inches(0.28), "PRPG & TOGGLE-RATE CONTROL RESULTS", C_PILL_GREEN)

    # LFSR Characteristic Polynomial Box
    eq_tb = s.shapes.add_textbox(left_x + Inches(0.16), c1_y + Inches(0.40), col_w - Inches(0.32), Inches(0.24))
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
    table_shape = s.shapes.add_table(8, 5, left_x + Inches(0.14), c1_y + Inches(0.66), col_w - Inches(0.28), Inches(1.64))
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
    n1_tb = s.shapes.add_textbox(left_x + Inches(0.16), c1_y + Inches(2.34), col_w - Inches(0.32), Inches(0.28))
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
    box2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, c2_y, col_w, c2_h)
    box2.fill.solid()
    box2.fill.fore_color.rgb = C_WHITE
    box2.line.color.rgb = C_CARD_BORDER
    box2.line.width = Pt(1.5)

    add_pill_badge(s, left_x + Inches(0.18), c2_y + Inches(0.10), Inches(3.6), Inches(0.28), "INTEGRATED FPGA SYNTHESIS (VIVADO)", C_PILL_BLUE)

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
        mp2.font.size = Pt(9.2)
        mp2.font.bold = True
        mp2.font.color.rgb = m_col
        mp2.space_before = Pt(2)

    sntb = s.shapes.add_textbox(left_x + Inches(0.18), c2_y + Inches(1.16), col_w - Inches(0.36), Inches(1.16))
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
    box3 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, c3_y, col_w, c3_h)
    box3.fill.solid()
    box3.fill.fore_color.rgb = C_WHITE
    box3.line.color.rgb = RGBColor(191, 219, 254)
    box3.line.width = Pt(1.5)

    add_pill_badge(s, right_x + Inches(0.18), c3_y + Inches(0.10), Inches(3.8), Inches(0.28), "MIPS32 CORE & SCAN ARCHITECTURE RESULTS", C_PILL_BLUE)

    m1_tb = s.shapes.add_textbox(right_x + Inches(0.20), c3_y + Inches(0.42), col_w - Inches(0.40), c3_h - Inches(0.48))
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
    box4 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, c4_y, col_w, c4_h)
    box4.fill.solid()
    box4.fill.fore_color.rgb = C_WHITE
    box4.line.color.rgb = RGBColor(254, 215, 170)
    box4.line.width = Pt(1.5)

    add_pill_badge(s, right_x + Inches(0.18), c4_y + Inches(0.10), Inches(3.8), Inches(0.28), "LBIST CONTROLLER & FAULT COVERAGE ANALYSIS", C_PILL_ORANGE)

    m3_tb = s.shapes.add_textbox(right_x + Inches(0.20), c4_y + Inches(0.42), col_w - Inches(0.40), c4_h - Inches(0.48))
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
    thx_box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), thx_y, thx_w, thx_h)
    thx_box.fill.solid()
    thx_box.fill.fore_color.rgb = RGBColor(238, 242, 255)
    thx_box.line.color.rgb = C_BLUE
    thx_box.line.width = Pt(1.5)

    ttb = s.shapes.add_textbox(Inches(0.9), thx_y + Inches(0.06), thx_w - Inches(0.2), thx_h - Inches(0.12))
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

    # Save standalone presentation
    out_file = "VL405_LBIST_Final_Results_Slide.pptx"
    prs.save(out_file)
    print(f"[SUCCESS] Standalone Results Slide generated: {out_file}")

if __name__ == "__main__":
    build_standalone_results_slide()
