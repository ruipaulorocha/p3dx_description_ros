import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, OpaqueFunction, SetLaunchConfiguration)
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command


def generate_launch_description():
    
    urdf_file_name = 'pioneer3dx_fixed_joints.urdf'
    urdf_path = os.path.join(
        get_package_share_directory('p3dx_description_ros'), 'urdf', urdf_file_name
        )
    robot_desc = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    arg_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )
    arg_tf_prefix = DeclareLaunchArgument(
            'tf_prefix',
            default_value='',
            description='TF2 prefix'
    )

    def get_prefix(context):
        prefix = context.launch_configurations['tf_prefix']
        if (prefix != ''):
            frame_prefix = prefix + '/'
        else:
            frame_prefix = ''
        return [SetLaunchConfiguration('frame_prefix', frame_prefix)]

    get_prefix_fn = OpaqueFunction(function = get_prefix)


    state_publisher = Node(
        namespace=[LaunchConfiguration('tf_prefix')],
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='p3dx_description',
        output='screen',
        parameters=[
            {
                'robot_description': robot_desc,
                'use_sim_time': use_sim_time,
                'frame_prefix': [LaunchConfiguration('frame_prefix')]
            }
        ]
    )

    return LaunchDescription([
        arg_sim_time,
        arg_tf_prefix,
        get_prefix_fn,
        state_publisher
    ])
