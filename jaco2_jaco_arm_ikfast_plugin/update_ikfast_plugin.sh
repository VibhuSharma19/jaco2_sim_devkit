search_mode=OPTIMIZE_MAX_JOINT
srdf_filename=jaco2.srdf
robot_name_in_srdf=jaco2
moveit_config_pkg=jaco2_moveit_config
robot_name=jaco2
planning_group_name=jaco_arm
ikfast_plugin_pkg=jaco2_jaco_arm_ikfast_plugin
base_link_name=world
eef_link_name=jaco2_end_effector
ikfast_output_path=/home/v/Documents/jaco2_jaco_arm_ikfast_plugin/src/jaco2_jaco_arm_ikfast_solver.cpp

ros2 run moveit_kinematics create_ikfast_moveit_plugin.py\
  --search_mode=$search_mode\
  --srdf_filename=$srdf_filename\
  --robot_name_in_srdf=$robot_name_in_srdf\
  --moveit_config_pkg=$moveit_config_pkg\
  $robot_name\
  $planning_group_name\
  $ikfast_plugin_pkg\
  $base_link_name\
  $eef_link_name\
  $ikfast_output_path
