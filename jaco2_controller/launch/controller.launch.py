import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.substitutions import Command, LaunchConfiguration
from launch.event_handlers import OnProcessExit

from launch_ros.actions import Node, SetParameter
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    jaco2_dir = get_package_share_directory('jaco2_description')
    jaco2_control_dir = get_package_share_directory('jaco2_controller')

    model_arg = DeclareLaunchArgument(
        name= "model",
        default_value= os.path.join(jaco2_dir, 'urdf', 'jaco2_standalone.xacro'),
        description= "Path to robot model xacro file"
    )

    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration('model')]),
        value_type=str
    )

    robot_controller_config = os.path.join(jaco2_control_dir, 'config', 'jaco2_controllers.yaml')

    robot_controller = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_controller_config,
                    {"use_sim_time": True},],
        output='both',
        arguments=[
            "--controller-ros-args",
            "--remap /controller_manager/robot_description:=/robot_description",
        ],
    )

    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
            "--controller-ros-args",
            "--remap /controller_manager/robot_description:=/robot_description",
        ],
        parameters=[{"use_sim_time": True},],
    )

    arm_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "arm_controller",
            "--controller-manager",
            "/controller_manager",
            "--controller-ros-args",
            "--remap /controller_manager/robot_description:=/robot_description",
        ],
    )

    gripper_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "gripper_controller",
            "--controller-manager",
            "/controller_manager",
            "--controller-ros-args",
            "--remap /controller_manager/robot_description:=/robot_description",
        ],
    )

    jsb_before_arm = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=gripper_controller,
            on_exit=joint_state_broadcaster,
        )
    )

    gripper_after_arm = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=arm_controller,
            on_exit=gripper_controller,
        )
    )
    return LaunchDescription([
        SetParameter(name='use_sim_time', value=True),
        model_arg,
        #robot_controller,
        joint_state_broadcaster,
        arm_controller,
        gripper_controller,
        #jsb_before_arm,
        #gripper_after_arm,
    ])
