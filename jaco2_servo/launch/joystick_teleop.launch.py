#!/usr/bin/python3

import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch_param_builder import ParameterBuilder
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():

   jaco2_moveit_dir = get_package_share_directory('jaco2_moveit_config')
   moveit_config = (
        MoveItConfigsBuilder("jaco2", package_name="jaco2_moveit_config")
        .robot_description_semantic(file_path=os.path.join(jaco2_moveit_dir,"config","jaco2.srdf"))
        .trajectory_execution(file_path=os.path.join(jaco2_moveit_dir,"config","moveit_controllers.yaml"))
        .joint_limits(file_path="config/joint_limits.yaml")
        .robot_description_kinematics(file_path=os.path.join(jaco2_moveit_dir,"config","kinematics.yaml"))
        .to_moveit_configs()
    )
   
   servo_params = {
      "moveit_servo": ParameterBuilder("jaco2_servo")
      .yaml("config/servo_params.yaml")
      .to_dict()
   }

   acceleration_filter_update_period = {"update_period": 0.01}
   planning_group_name = {"planning_group_name": "jaco_arm"}

   rviz_config_file = os.path.join(
        get_package_share_directory("jaco2_servo"),
        "config",
        "servo.rviz",
    )
   rviz_node = launch_ros.actions.Node(
       package="rviz2",
       executable="rviz2",
       output="log",
       arguments=["-d", rviz_config_file],
       parameters=[
           moveit_config.robot_description,
           moveit_config.robot_description_semantic,
           {"use_sim_time": True},
       ],
   )

   teleop_node = launch_ros.actions.Node(
        package="jaco2_servo",
        executable="joy_teleop",
        output="screen",
    )
   
   joy_node = launch_ros.actions.Node(
        package="joy",
        executable="joy_node",
        output="screen",
        parameters=[{"dev": "/dev/input/js2"}],
    )
   
   servo_node = launch_ros.actions.Node(
        package="moveit_servo",
        executable="servo_node",
        parameters=[
            servo_params,
            acceleration_filter_update_period,
            planning_group_name,
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            moveit_config.planning_scene_monitor,
            {"use_sim_time": True},
        ],
        output="screen",
   )
   
   return launch.LaunchDescription([
      rviz_node,
      servo_node,
      teleop_node,
      joy_node,
   ])