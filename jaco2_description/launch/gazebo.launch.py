import os
from pathlib import Path
from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition, UnlessCondition

from launch_ros.actions import Node, SetParameter
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    jaco_dir = get_package_share_directory('jaco2_description')
    gazebo_sim_dir = get_package_share_directory('ros_gz_sim')
    gazebo_dir = get_package_share_directory('jaco2_gazebo')

    model_arg = DeclareLaunchArgument(
        name= "model",
        default_value= os.path.join(jaco_dir, 'urdf', 'jaco2_standalone.xacro'),
        description= "Path to robot model xacro file"
    )

    camera_model_arg = DeclareLaunchArgument(
        name="camera_model",
        default_value= os.path.join(jaco_dir, 'urdf', 'jaco2_standalone_camera.xacro'),
        description= "Path to robot model with camera sensor"
    )

    declare_use_camera_cmd = DeclareLaunchArgument(
        name='use_camera',
        default_value='false',
        choices=['true', 'false'],
        description='Flag to enable camera sensor')

    gazebo_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[
            str(Path(jaco_dir).parent.resolve())
            ]
        )
    
    gazebo_world = DeclareLaunchArgument(
        default_value=PathJoinSubstitution([gazebo_dir, 'worlds', 'empty.sdf']),
        name = "empty_world"
    )

    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration('model')]),
        value_type=str
    )

    robot_description_camera = ParameterValue(
        Command(["xacro ", LaunchConfiguration('camera_model')]),
        value_type=str
    )

    robot_state_publisher_with_camera = Node(
        condition=IfCondition(LaunchConfiguration('use_camera')),
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{"robot_description": robot_description_camera, "use_sim_time": True}],
        output='screen'
    )

    robot_state_publisher_without_camera = Node(
        condition=UnlessCondition(LaunchConfiguration('use_camera')),
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
        output='screen'
    )


    #gazebo = IncludeLaunchDescription(
    #    PythonLaunchDescriptionSource(os.path.join(gazebo_sim_dir, 'launch', 'gz_sim.launch.py')),
    #    launch_arguments= {'gz_args': ' -r --physics-engine gz-physics-bullet-featherstone-plugin'}.items(),
    #)

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_sim_dir, 'launch', 'gz_sim.launch.py')),
        launch_arguments= {'gz_args': PathJoinSubstitution([gazebo_dir, 'worlds', 'empty.sdf']),
                           'unpaused': 'true'}.items(),
    )

    spawn_robot = Node(
        package= 'ros_gz_sim',
        executable= 'create',
        output= 'screen',
        arguments= ['-topic','robot_description',
                    '-name', 'jaco2',
                    'x', '1.0',
                    'y', '0.5',
                    'z', '0.0']
    )

    ros2_gz_bridge = Node(
        package= 'ros_gz_bridge',
        executable= 'parameter_bridge',
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",],
        parameters=[{"use_sim_time": True},]
    )

    return LaunchDescription([
        SetParameter(name='use_sim_time', value=True),
        model_arg,
        camera_model_arg,
        declare_use_camera_cmd,
        gazebo_resource_path,
        robot_state_publisher_with_camera,
        robot_state_publisher_without_camera,
        gazebo,
        spawn_robot,
        ros2_gz_bridge
    ])