# ==============================================================================
# Vivado Project Generation Script: Member_2_PRPG_Toggle_Control
# Project: Scan-Based LBIST with Programmable Toggle-Rate Control (MIPS32 Architecture)
# Role   : Member 2 - PRPG and Toggle-Rate Control
# Target : Xilinx Artix-7 xc7a35tcpg236-1 (Basys3 / Nexys A7 Compatible)
# ==============================================================================

set project_name "Member_2_PRPG_Toggle_Control"
set origin_dir [file normalize [file dirname [info script]]]
set part_name "xc7a35tcpg236-1"

puts "==> Creating Vivado Project: $project_name in $origin_dir"
create_project -force $project_name "$origin_dir" -part $part_name

# Set Project Properties
set_property target_language VHDL [current_project]
set_property simulator_language Mixed [current_project]
set_property default_lib work [current_project]

# Add RTL Design Sources (VHDL-2008)
puts "==> Adding Synthesizable RTL Sources..."
add_files -norecurse -fileset sources_1 [list \
    "$origin_dir/RTL/lfsr_prpg.vhd" \
    "$origin_dir/RTL/hamming_distance.vhd" \
    "$origin_dir/RTL/conventional_prpg.vhd" \
    "$origin_dir/RTL/toggle_rate_controller.vhd" \
    "$origin_dir/RTL/pattern_modifier.vhd" \
    "$origin_dir/RTL/modified_prpg_top.vhd" \
    "$origin_dir/RTL/scan_chain_model.vhd" \
]

# Set VHDL 2008 Standard on RTL Sources
set_property file_type {VHDL 2008} [get_files -of_objects [get_filesets sources_1]]

# Set Top-Level RTL Module
set_property top modified_prpg_top [current_fileset]
update_compile_order -fileset sources_1

# Add Simulation Testbenches
puts "==> Adding Simulation Testbenches..."
add_files -norecurse -fileset sim_1 [list \
    "$origin_dir/Testbench/tb_modified_prpg_top.vhd" \
    "$origin_dir/Testbench/tb_conventional_prpg.vhd" \
    "$origin_dir/Testbench/tb_pattern_modifier.vhd" \
]

# Set VHDL 2008 Standard on Simulation Sources
set_property file_type {VHDL 2008} [get_files -of_objects [get_filesets sim_1]]

# Set Top Simulation Module
set_property top tb_modified_prpg_top [get_filesets sim_1]
set_property top_lib work [get_filesets sim_1]
update_compile_order -fileset sim_1

puts "==> Project Creation Completed Successfully."
puts "==> Project file located at: $origin_dir/$project_name.xpr"

# Optional: Run Out-of-Context Synthesis to generate utilization and timing reports
puts "==> Running RTL Synthesis for Utilization and Timing Analysis..."
synth_design -top modified_prpg_top -part $part_name -mode out_of_context

# Report Utilization and Timing into Simulation_Results directory
file mkdir "$origin_dir/Simulation_Results"
report_utilization -file "$origin_dir/Simulation_Results/synth_utilization.rpt"
report_timing_summary -file "$origin_dir/Simulation_Results/synth_timing.rpt"

puts "==> Synthesis and Reports Generation Finished Successfully!"
exit

