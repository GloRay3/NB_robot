# 记载gazebo,导入世界模型，导入机器人的urdf文件

import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource



def generate_launch_description():
    # 获取sim_robot包的路径
    sim_robot_dir = get_package_share_directory('sim_robot')

   # 定义gazebo的世界文件路径
    world_file = os.path.join(sim_robot_dir, 'world', 'maze.world')
    # 启动gazebo仿真环境，并加载指定的世界文件
    launch_gazebo = launch.actions. IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory('gazebo_ros'), '/launch/gazebo.launch.py']),
        launch_arguments = [('world', world_file) , ('verbose', 'true') ]
    )

    # 请求gazebo加载机器人
    spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                   '-entity', 'turtlebot3_waffle_pi'],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )
    # 发布关节tf变换。由于launch里节点不能接受到gazebo仿真环境的真实信息，该部分关节tf放在了urdf文件中吗，以便能真实接受到gazebo仿真环境的真实信息
    joint_state_publisher_node = launch_ros.actions.Node(
    package='joint_state_publisher',
    executable='joint_state_publisher',
    name='joint_state_publisher'
)
    return launch.LaunchDescription([
        launch_gazebo,
        spawn_entity,
        # joint_state_publisher_node
    ])
