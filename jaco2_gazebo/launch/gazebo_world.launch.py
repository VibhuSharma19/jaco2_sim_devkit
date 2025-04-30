import os
from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node, SetParameter
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    jaco_dir = get_package_share_directory('jaco2_description')
    gazebo_sim_dir = get_package_share_directory('ros_gz_sim')
    gazebo_dir = get_package_share_directory('jaco2_gazebo')

    model_arg = DeclareLaunchArgument(
        name= "model",
        default_value= os.path.join(jaco_dir, 'urdf', 'jaco2_standalone_camera.xacro'),
        description= "Path to robot model xacro file"
    )

    bridge_config_file_path = os.path.join(gazebo_dir, 'config','gz_ros_bridge.yaml')
    
    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration('model')]),
        value_type=str
    )

    robot_state_publisher = Node(
        package= 'robot_state_publisher',
        executable= 'robot_state_publisher',
        parameters= [{"robot_description": robot_description,
                      "use_sim_time": True}],
        output= 'screen'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_sim_dir, 'launch', 'gz_sim.launch.py')),
        launch_arguments= {'gz_args': PathJoinSubstitution([gazebo_dir, 'worlds', 'pick_place_world.sdf'])}.items(),
    )

    spawn_robot = Node(
        package= 'ros_gz_sim',
        executable= 'create',
        output= 'screen',
        arguments= ['-topic','robot_description',
                    '-name', 'jaco2',
                    '-allow_renaming', 'true',
                    'x', '1.0',
                    'y', '0.5',
                    'z', '0.0']
    )

    ros2_gz_bridge = Node(
        package= 'ros_gz_bridge',
        executable= 'parameter_bridge',
        parameters=[{"use_sim_time": True,
                     "config_file": bridge_config_file_path}],
        output= 'screen',
    )

    depth_image_remap = Node(
        package='jaco2_gazebo',
        executable='depth_image_remap.py',
    )

    return LaunchDescription([
        SetParameter(name='use_sim_time', value=True),
        model_arg,
        robot_state_publisher,
        gazebo,
        spawn_robot,
        ros2_gz_bridge,
        depth_image_remap,
    ])