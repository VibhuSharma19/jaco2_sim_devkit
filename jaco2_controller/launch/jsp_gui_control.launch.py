import os
from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import AppendEnvironmentVariable, DeclareLaunchArgument, ExecuteProcess
from launch.actions import RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare

from launch_ros.actions import Node


def generate_launch_description():
    jaco_controller_dir = get_package_share_directory('jaco2_controller')
    jaco_description_dir = get_package_share_directory('jaco2_description')

    gazebo_launch = ExecuteProcess(
        cmd= ['ros2','launch','jaco2_description','gazebo.launch.py'],
        output = "screen"
    )

    controller_launch_cmd = ExecuteProcess(
        cmd=['ros2','launch','jaco2_controller','controller.launch.py'],
        output = "screen",
    )

    jsp_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        remappings=[
            ("/joint_states", "/joint_commands"),
        ]
    )

    jsp_controller_node = Node(
        package='jaco2_controller',
        executable='jsp_controller',
        output="screen"
    )

    controller_event = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=gazebo_launch,
            on_exit=[controller_launch_cmd],
        )
    )

    return LaunchDescription([
        jsp_gui,
        jsp_controller_node,
    ])
