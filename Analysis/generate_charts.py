#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
Project   : Scan-Based LBIST with Programmable Toggle-Rate Control
File      : generate_charts.py
Role      : Member 2 - Performance Visualization (Zero Dependency SVG Generator)
Standard  : Python 3 Standard Library (Pure SVG generation)
--------------------------------------------------------------------------------
"""

import os

results_dir = os.path.join(os.path.dirname(__file__), "..", "Simulation_Results")
os.makedirs(results_dir, exist_ok=True)
legacy_dir = os.path.join(os.path.dirname(__file__), "..", "Simulation", "results")
os.makedirs(legacy_dir, exist_ok=True)

# Data from simulation
targets = ["10%", "20%", "30%", "40%", "50%", "60%", "Bypass"]
target_vals = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 100.0]
word_rates = [10.00, 19.98, 29.62, 38.70, 46.17, 48.75, 52.28]
scan_rates = [7.38, 9.50, 13.96, 18.66, 25.07, 28.24, 50.42]
power_savings = [84.99, 81.04, 71.93, 63.28, 52.57, 45.52, 0.00]

def generate_comparison_chart_svg():
    width = 800
    height = 450
    margin_l = 80
    margin_r = 40
    margin_t = 60
    margin_b = 60
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">')
    
    # Title
    svg.append(f'<text x="{width/2}" y="32" font-size="18" font-weight="bold" text-anchor="middle" fill="#1e293b">Target vs. Measured Toggle Rates (Word vs. Scan Chain)</text>')
    
    # Grid lines and Y-axis labels (0% to 60%)
    for pct in range(0, 70, 10):
        y = margin_t + plot_h - (pct / 60.0) * plot_h
        svg.append(f'<line x1="{margin_l}" y1="{y}" x2="{width-margin_r}" y2="{y}" stroke="#e2e8f0" stroke-width="1"/>')
        svg.append(f'<text x="{margin_l - 12}" y="{y + 4}" font-size="12" text-anchor="end" fill="#64748b">{pct}%</text>')
        
    # X-axis
    svg.append(f'<line x1="{margin_l}" y1="{margin_t+plot_h}" x2="{width-margin_r}" y2="{margin_t+plot_h}" stroke="#475569" stroke-width="2"/>')
    svg.append(f'<line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{margin_t+plot_h}" stroke="#475569" stroke-width="2"/>')
    
    num_bars = len(targets)
    group_w = plot_w / num_bars
    bar_w = 26
    
    for i, t in enumerate(targets):
        cx = margin_l + i * group_w + group_w / 2
        # Target bar (gray dashed)
        t_val = min(target_vals[i], 60.0)
        h_t = (t_val / 60.0) * plot_h
        y_t = margin_t + plot_h - h_t
        
        # Word Rate bar (blue)
        w_val = min(word_rates[i], 60.0)
        h_w = (w_val / 60.0) * plot_h
        y_w = margin_t + plot_h - h_w
        bx_w = cx - bar_w - 4
        svg.append(f'<rect x="{bx_w}" y="{y_w}" width="{bar_w}" height="{h_w}" fill="#2563eb" rx="3"/>')
        svg.append(f'<text x="{bx_w + bar_w/2}" y="{y_w - 6}" font-size="11" font-weight="600" text-anchor="middle" fill="#1d4ed8">{word_rates[i]:.1f}%</text>')
        
        # Scan Rate bar (emerald green)
        s_val = min(scan_rates[i], 60.0)
        h_s = (s_val / 60.0) * plot_h
        y_s = margin_t + plot_h - h_s
        bx_s = cx + 4
        svg.append(f'<rect x="{bx_s}" y="{y_s}" width="{bar_w}" height="{h_s}" fill="#059669" rx="3"/>')
        svg.append(f'<text x="{bx_s + bar_w/2}" y="{y_s - 6}" font-size="11" font-weight="600" text-anchor="middle" fill="#047857">{scan_rates[i]:.1f}%</text>')
        
        # X-label
        svg.append(f'<text x="{cx}" y="{margin_t + plot_h + 24}" font-size="13" font-weight="bold" text-anchor="middle" fill="#334155">{t}</text>')
        svg.append(f'<text x="{cx}" y="{margin_t + plot_h + 40}" font-size="11" text-anchor="middle" fill="#64748b">Target</text>')

    # Legend
    svg.append(f'<rect x="{width - 290}" y="45" width="16" height="16" fill="#2563eb" rx="2"/>')
    svg.append(f'<text x="{width - 266}" y="58" font-size="12" fill="#334155">Modified Word Toggle Rate</text>')
    svg.append(f'<rect x="{width - 290}" y="68" width="16" height="16" fill="#059669" rx="2"/>')
    svg.append(f'<text x="{width - 266}" y="81" font-size="12" fill="#334155">Scan-Chain Shift Toggle Rate</text>')
    
    svg.append('</svg>')
    
    filepath = os.path.join(results_dir, "toggle_rate_comparison.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Saved: {filepath}")

def generate_power_curve_svg():
    width = 800
    height = 420
    margin_l = 80
    margin_r = 50
    margin_t = 60
    margin_b = 60
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">')
    
    # Title
    svg.append(f'<text x="{width/2}" y="32" font-size="18" font-weight="bold" text-anchor="middle" fill="#1e293b">Scan-Shift Dynamic Power Reduction Factor (α Saving)</text>')
    
    # Y-axis (0% to 100%)
    for pct in range(0, 110, 20):
        y = margin_t + plot_h - (pct / 100.0) * plot_h
        svg.append(f'<line x1="{margin_l}" y1="{y}" x2="{width-margin_r}" y2="{y}" stroke="#e2e8f0" stroke-width="1"/>')
        svg.append(f'<text x="{margin_l - 12}" y="{y + 4}" font-size="12" text-anchor="end" fill="#64748b">{pct}%</text>')
        
    svg.append(f'<line x1="{margin_l}" y1="{margin_t+plot_h}" x2="{width-margin_r}" y2="{margin_t+plot_h}" stroke="#475569" stroke-width="2"/>')
    svg.append(f'<line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{margin_t+plot_h}" stroke="#475569" stroke-width="2"/>')
    
    # Points and line
    pts = []
    coords = []
    step_x = plot_w / (len(targets) - 1)
    
    for i, p in enumerate(power_savings):
        x = margin_l + i * step_x
        y = margin_t + plot_h - (p / 100.0) * plot_h
        coords.append((x, y, p, targets[i]))
        pts.append(f"{x},{y}")
        
    # Area fill
    poly_pts = f"{margin_l},{margin_t+plot_h} " + " ".join(pts) + f" {width-margin_r},{margin_t+plot_h}"
    svg.append(f'<polygon points="{poly_pts}" fill="#dbeafe" opacity="0.6"/>')
    svg.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#2563eb" stroke-width="3.5" stroke-linecap="round"/>')
    
    for x, y, p, name in coords:
        svg.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#1d4ed8" stroke="#ffffff" stroke-width="2.5"/>')
        label_y = y - 12 if p > 10 else y - 12
        svg.append(f'<text x="{x}" y="{label_y}" font-size="12" font-weight="bold" text-anchor="middle" fill="#1e40af">{p:.1f}%</text>')
        svg.append(f'<text x="{x}" y="{margin_t + plot_h + 24}" font-size="12" font-weight="600" text-anchor="middle" fill="#334155">{name}</text>')
        
    svg.append('</svg>')
    
    filepath = os.path.join(results_dir, "power_reduction_curve.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Saved: {filepath}")

generate_comparison_chart_svg()
generate_power_curve_svg()

import shutil
for f in ["toggle_rate_comparison.svg", "power_reduction_curve.svg"]:
    shutil.copy2(os.path.join(results_dir, f), os.path.join(legacy_dir, f))

