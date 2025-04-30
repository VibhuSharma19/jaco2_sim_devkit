#!/usr/bin/python3

import os
from launch import LaunchDescription
from moveit_configs_utils import MoveItConfigsBuilder
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    is_sim = LaunchConfiguration("is_sim")
    
    is_sim_arg = DeclareLaunchArgument(
        "is_sim",
        default_value="True"
    )

    jaco2_moveit_dir = get_package_share_directory('jaco2_moveit_config')

    moveit_config = (
        MoveItConfigsBuilder("jaco2", package_name="jaco2_moveit_config")
        .robot_description_semantic(file_path=os.path.join(jaco2_moveit_dir,"config","jaco2.srdf"))
        .trajectory_execution(file_path=os.path.join(jaco2_moveit_dir,"config","moveit_controllers.yaml"))
        .joint_limits(file_path="config/joint_limits.yaml")
        .robot_description_kinematics(file_path=os.path.join(jaco2_moveit_dir,"config","kinematics_ikfast.yaml"))
        .planning_pipelines(
            pipelines=["ompl", "pilz_industrial_motion_planner", "stomp"],
            default_planning_pipeline= "pilz_industrial_motion_planner",
        )
        .planning_scene_monitor(
            publish_robot_description=False,
            publish_robot_description_semantic=True,
            publish_planning_scene=True,
        )
        .pilz_cartesian_limits(file_path=os.path.join(jaco2_moveit_dir,"config","pilz_cartesian_limits.yaml"))
        .sensors_3d(file_path= os.path.join(jaco2_moveit_dir, "config","sensors_3d.yaml"))
        .to_moveit_configs()
    )

    octomap_config = {'octomap_frame': 'rgbd_camera', 
                      'octomap_resolution': 0.05,
                      'max_range': 15.0}

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict(),
                    octomap_config, 
                    {"use_sim_time": is_sim},
                    {'use_monitor': True},  
                    {'use_robot_state_monitor': True},
                    {'use_scene_monitor': True},
                    {'use_geometry_monitor': True},],
    )

    # RViz
    rviz_config = os.path.join(
        jaco2_moveit_dir,
            "config",
            "moveit.rviz",
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="log",
        arguments=["-d", rviz_config],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            moveit_config.trajectory_execution,
            moveit_config.planning_pipelines,
            moveit_config.planning_scene_monitor,
            moveit_config.sensors_3d,
            {"use_sim_time": is_sim},
        ],
    )

    return LaunchDescription(
        [
            SetEnvironmentVariable('LD_PRELOAD', '/usr/lib/x86_64-linux-gnu/liboctomap.so'),
            is_sim_arg,
            move_group_node, 
            rviz_node
        ]
    )