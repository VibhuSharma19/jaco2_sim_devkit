#!/usr/bin/python3

from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import ExecuteProcess
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():

    jaco = get_package_share_directory("jaco2_description")
    jaco_moveit = get_package_share_directory("jaco2_moveit_config")

    moveit_config = (
        MoveItConfigsBuilder(robot_name="jaco2", package_name="jaco2_moveit_config")
        .planning_pipelines(pipelines=["ompl", "pilz_industrial_motion_planner", "stomp"], default_planning_pipeline="pilz_industrial_motion_planner")
        .robot_description(file_path=os.path.join(jaco, "urdf", "jaco2_standalone.xacro"))
        .robot_description_semantic(file_path=os.path.join(jaco_moveit,"config","jaco2.srdf"))
        .robot_description_kinematics(file_path=os.path.join(jaco_moveit,"config","kinematics_kdl.yaml"))
        .trajectory_execution(file_path=os.path.join(jaco_moveit, "config", "moveit_controllers.yaml"))
        .planning_scene_monitor(publish_planning_scene=True)
        .to_moveit_configs()
    )

    # Load  ExecuteTaskSolutionCapability so we can execute found solutions in simulation
    move_group_capabilities = {"capabilities": "move_group/ExecuteTaskSolutionCapability"}

    # Start the actual move_group node/action server
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="both",
        parameters=[
            moveit_config.to_dict(),
            move_group_capabilities,
            {"use_sim_time": True},
        ],
    )

    rviz_config_file = (os.path.join(get_package_share_directory("jaco2_moveit_task_constructor"), "config", "mtc.rviz"))
    
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_scene_monitor,
            move_group_capabilities,
            {"use_sim_time": True},
        ],
    )

    return LaunchDescription([
        move_group_node, 
        rviz_node
    ])