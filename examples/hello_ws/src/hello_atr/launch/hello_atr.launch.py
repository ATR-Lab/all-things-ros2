"""Start the talker and the listener together.

Usage:
    ros2 launch hello_atr hello_atr.launch.py
    ros2 launch hello_atr hello_atr.launch.py greeting:='Hi from the lab'
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    params_file = os.path.join(
        get_package_share_directory('hello_atr'), 'config', 'talker.yaml')

    greeting = LaunchConfiguration('greeting')

    return LaunchDescription([
        DeclareLaunchArgument(
            'greeting',
            default_value='Hello from the ATR Lab',
            description='Text the talker publishes'),
        Node(
            package='hello_atr',
            executable='talker',
            name='talker',
            # Parameters later in the list win: the YAML file first, then the launch argument.
            parameters=[params_file, {'greeting': greeting}],
            output='screen'),
        Node(
            package='hello_atr',
            executable='listener',
            name='listener',
            output='screen'),
    ])
