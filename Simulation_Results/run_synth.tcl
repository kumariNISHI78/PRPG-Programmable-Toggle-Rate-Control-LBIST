# Vivado Batch Synthesis Test
set origin_dir "C:/Users/Nishi Kumari/.gemini/antigravity/scratch/Member_2_PRPG_Toggle_Control"
create_project -in_memory -part xc7a35tcpg236-1

read_vhdl -vhdl2008 "$origin_dir/RTL/lfsr_prpg.vhd"
read_vhdl -vhdl2008 "$origin_dir/RTL/hamming_distance.vhd"
read_vhdl -vhdl2008 "$origin_dir/RTL/conventional_prpg.vhd"
read_vhdl -vhdl2008 "$origin_dir/RTL/toggle_rate_controller.vhd"
read_vhdl -vhdl2008 "$origin_dir/RTL/pattern_modifier.vhd"
read_vhdl -vhdl2008 "$origin_dir/RTL/modified_prpg_top.vhd"

synth_design -top modified_prpg_top -part xc7a35tcpg236-1

report_utilization -file "$origin_dir/Simulation/results/synth_utilization.rpt"
report_timing_summary -file "$origin_dir/Simulation/results/synth_timing.rpt"
puts "SYNTHESIS_COMPLETED_SUCCESSFULLY"
exit

