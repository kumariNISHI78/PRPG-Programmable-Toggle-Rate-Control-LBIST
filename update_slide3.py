with open('build_presentation.py', 'r', encoding='utf-8') as f:
    content = f.read()

idx1 = content.find('    # Right Side: Performance Graph + Actual Vivado Waveform Screenshot')
idx2 = content.find('    # =========================================================================\n    # SLIDE 4: CONCLUSION AND FUTURE WORK')

assert idx1 != -1 and idx2 != -1, f"Indices not found: {idx1}, {idx2}"

replacement = """    # Right Side: Performance Graph & Key Verification Metrics (Waveform Removed)
    right_x = Inches(7.0)
    right_y = Inches(1.5)
    right_w = Inches(5.533)

    # 1. Performance Chart (Expanded Height, Clean Light Theme)
    chart_path = "Analysis/slide3_light_chart.png"
    if not os.path.exists(chart_path):
        chart_path = "Analysis/slide3_performance_chart.png"
    if os.path.exists(chart_path):
        s3.shapes.add_picture(chart_path, right_x, right_y, width=right_w, height=Inches(3.3))

    # 2. Key Metrics Verification Dashboard (Clean White Card)
    mcard_y = right_y + Inches(3.45)
    mcard_h = Inches(2.25)
    mcard = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, mcard_y, right_w, mcard_h)
    mcard.fill.solid()
    mcard.fill.fore_color.rgb = C_CARD_BG
    mcard.line.color.rgb = C_CARD_BORDER
    mcard.line.width = Pt(1.5)

    mtb = s3.shapes.add_textbox(right_x + Inches(0.2), mcard_y + Inches(0.12), right_w - Inches(0.4), mcard_h - Inches(0.24))
    mtf = mtb.text_frame
    mtf.word_wrap = True
    mtf.margin_top = mtf.margin_bottom = mtf.margin_left = mtf.margin_right = 0

    mp = mtf.paragraphs[0]
    mp.text = "SIMULATION VERIFICATION HIGHLIGHTS"
    mp.font.name = "Segoe UI"
    mp.font.size = Pt(11)
    mp.font.bold = True
    mp.font.color.rgb = C_SUBTITLE_BLUE

    metric_items = [
        ("84.35% Peak Power Reduction", "At 10% target, scan chain transitions drop from 55.37% down to 8.67%, saving 84.35% shift power.", C_GREEN),
        ("0.29% Target Tracking Error", "Sigma-delta fractional dither hits 10.29% word toggle rate closely tracking the 10.00% target.", C_BLUE),
        ("0 Latency Delay Penalty", "Single-cycle synchronous output generates modified test patterns every clock with 0 delay overhead.", C_TITLE_NAVY)
    ]

    for m_hdr, m_desc, m_clr in metric_items:
        p = mtf.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = "✔ " + m_hdr + ": "
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(9)
        r1.font.bold = True
        r1.font.color.rgb = m_clr

        r2 = p.add_run()
        r2.text = m_desc
        r2.font.name = "Segoe UI"
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = C_TEXT_DARK

"""

new_content = content[:idx1] + replacement + content[idx2:]

with open('build_presentation.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated build_presentation.py cleanly!")
