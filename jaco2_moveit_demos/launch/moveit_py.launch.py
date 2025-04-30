#!/usr/bin/python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node, SetParameter
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

   jaco2_moveit_dir = get_package_share_directory('jaco2_moveit_config')

   moveit_config = (
        MoveItConfigsBuilder("jaco2", package_name="jaco2_moveit_config")
        .robot_description_semantic(file_path=os.path.join(jaco2_moveit_dir,"config","jaco2.srdf"))
        .trajectory_execution(file_path=os.path.join(jaco2_moveit_dir,"config","moveit_controllers.yaml"))
        .joint_limits(file_path="config/joint_limits.yaml")
        .robot_description_kinematics(file_path=os.path.join(jaco2_moveit_dir,"config","kinematics.yaml"))
        .planning_pipelines(
            pipelines=["ompl", "pilz_industrial_motion_planner", "chomp"],
            default_planning_pipeline= "pilz_industrial_motion_planner",
        )
        .planning_scene_monitor(
            publish_robot_description=False,
            publish_robot_description_semantic=True,
            publish_planning_scene=True,
        )
        .pilz_cartesian_limits(file_path=os.path.join(jaco2_moveit_dir,"config","pilz_cartesian_limits.yaml"))
        .moveit_cpp(file_path= os.path.join(get_package_share_directory('jaco2_moveit_demos'), 'config', 'moveitpy_planning_params.yaml'))
        .to_moveit_configs()
    )
   
   arg = DeclareLaunchArgument(name='exe')

   moveitpy_node = Node(
       executable=LaunchConfiguration("exe"),
       package="jaco2_moveit_demos",
       output="both",
       parameters=[moveit_config.to_dict(), 
                   {"use_sim_time": True},],
   )

   rviz_config = os.path.join(
       jaco2_moveit_dir,
           "config",
           "moveitpy_planning.rviz",
   )

   rviz_node = Node(
       package="rviz2",
       executable="rviz2",
       output="both",
       arguments=["-d", rviz_config],
       parameters=[
           moveit_config.robot_description,
           moveit_config.robot_description_semantic,
           moveit_config.robot_description_kinematics,
           moveit_config.joint_limits,
           moveit_config.trajectory_execution,
           moveit_config.planning_pipelines,
           moveit_config.planning_scene_monitor,
           {"use_sim_time": True},
       ],
   )

   return LaunchDescription([
       moveitpy_node,
       arg,
       rviz_node
   ])