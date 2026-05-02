# 整合gazebo.launch.py和bot_pub.launch.py为一个launch文件

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    
    pkg_share = get_package_share_directory('sim_robot')

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'gazebo.launch.py')
        )
    )

    bot_pub_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'bot_pub.py')
        )
    )

    return LaunchDescription([
        gazebo_launch,
        bot_pub_launch
    ])