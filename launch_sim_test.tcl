open_project "Member_2_PRPG_Toggle_Control.xpr"
set_property -name {xsim.simulate.runtime} -value {1000ns} -objects [get_filesets sim_1]
launch_simulation -simset sim_1 -mode behavioral
close_project
exit

