import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    jaco = get_package_share_directory("jaco2_description")
    jaco_moveit = get_package_share_directory("jaco2_moveit_config")

    moveit_config = (
        MoveItConfigsBuilder(robot_name="jaco2", package_name="jaco2_moveit_config")
        .planning_pipelines(pipelines=["ompl", "pilz_industrial_motion_planner", "stomp"])
        .robot_description(file_path=os.path.join(jaco, "urdf", "jaco2_standalone.xacro"))
        .robot_description_semantic(file_path=os.path.join(jaco_moveit,"config","jaco2.srdf"))
        .robot_description_kinematics(file_path=os.path.join(jaco_moveit,"config","kinematics_kdl.yaml"))
        .trajectory_execution(file_path=os.path.join(jaco_moveit, "config", "moveit_controllers.yaml"))
        .joint_limits(file_path=os.path.join(jaco_moveit, 'config', 'joint_limits.yaml'))
        .planning_scene_monitor(publish_planning_scene=True, publish_geometry_updates=True)
        .to_moveit_configs()
    )

    planning_scene_publisher = Node(
        package="jaco2_moveit_task_constructor",
        executable="scene_publisher",
        output="screen",
    )

    node_exec = Node(
        package="jaco2_moveit_task_constructor",
        executable=LaunchConfiguration("exe"),
        output="both",
        parameters=[
            moveit_config.to_dict(),
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            moveit_config.planning_pipelines,
            moveit_config.planning_scene_monitor,
        ],
    )

    node_delayed = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action = planning_scene_publisher,
            on_exit = node_exec,
        )
    )



    arg = DeclareLaunchArgument(name="exe")

    return LaunchDescription([arg, planning_scene_publisher, node_delayed])