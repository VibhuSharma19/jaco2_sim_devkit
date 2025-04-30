import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler, TimerAction, ExecuteProcess
from launch.substitutions import Command, LaunchConfiguration
from launch.event_handlers import OnProcessExit
from launch.conditions import IfCondition, UnlessCondition

from launch_ros.actions import Node, SetParameter
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    jaco2_dir = get_package_share_directory('jaco2_description')
    jaco2_control_dir = get_package_share_directory('jaco2_controller')

    model_arg = DeclareLaunchArgument(
        name= "model",
        default_value= os.path.join(jaco2_dir, 'urdf', 'jaco2_generic', 'jaco2_standalone_generic.xacro'),
        description= "Path to robot model xacro file"
    )

    camera_model_arg = DeclareLaunchArgument(
        name= "camera_model",
        default_value= os.path.join(jaco2_dir, 'urdf', 'jaco2_generic', 'jaco2_standalone_camera_generic.xacro'),
        description= "Path to robot model with camera sensor xacro file"
    )

    declare_use_camera_cmd = DeclareLaunchArgument(
        name='use_camera',
        default_value='false',
        choices=['true', 'false'],
        description='Flag to enable camera sensor')

    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration('model')]),
        value_type=str
    )

    robot_description_camera = ParameterValue(
        Command(["xacro ", LaunchConfiguration('camera_model')]),
        value_type=str
    )

    robot_state_publisher = Node(
        condition=UnlessCondition(LaunchConfiguration('use_camera')),
        package= 'robot_state_publisher',
        executable= 'robot_state_publisher',
        parameters= [{"robot_description": robot_description}],
        output= 'screen'
    )

    robot_state_publisher_camera = Node(
        condition=IfCondition(LaunchConfiguration('use_camera')),
        package= 'robot_state_publisher',
        executable= 'robot_state_publisher',
        parameters= [{"robot_description": robot_description_camera}],
        output= 'screen'
    )

    robot_controller_config = os.path.join(jaco2_control_dir, 'config', 'jaco2_controllers.yaml')

    robot_controller = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_controller_config,
                    {"robot_description": robot_description},],
        output='both',
        arguments=[
            "--controller-ros-args",
            "--remap /controller_manager/robot_description:=/robot_description",
        ],
    )

    load_controllers = [

        Node(
            package="controller_manager",
            executable="spawner",
            arguments=[
                "joint_state_broadcaster",
                "--controller-manager",
                "/controller_manager",
            ],
            parameters=[{"use_sim_time": True},],
        ),

        Node(
            package="controller_manager",
            executable="spawner",
            arguments=[
                "arm_controller",
                "--controller-manager",
                "/controller_manager",
            ],
        ),

        Node(
            package="controller_manager",
            executable="spawner",
            arguments=[
                "gripper_controller",
                "--controller-manager",
                "/controller_manager",
            ],
        )
    ]

    return LaunchDescription([
        model_arg,
        robot_state_publisher,
        robot_controller,
        camera_model_arg,
        declare_use_camera_cmd,
        robot_state_publisher_camera,
    ] + load_controllers)
