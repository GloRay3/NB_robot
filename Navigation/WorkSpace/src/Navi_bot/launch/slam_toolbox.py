import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # 获取功能包路径
    navi_bot_dir = get_package_share_directory('navi_bot')
    sim_robot_dir = get_package_share_directory('sim_robot')

    # 参数文件和 rviz 文件路径(相对路径防止因绝对路径引起错误)
    # 使用os拼接防止路径错误
    slam_params = os.path.join(navi_bot_dir, 'config', 'slam_params.yaml')
    rviz_config = os.path.join(sim_robot_dir, 'config', 'rviz2', 'default.rviz')

    # 使用仿真时间
    use_sim_time = launch.substitutions.LaunchConfiguration(
        'use_sim_time', default='true')

    # 启动 slam_toolbox 节点
    # 建图过程中会发布 map 话题
    slam_node = launch_ros.actions.Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        #结果输出到终端
        output='screen',
        parameters=[slam_params, {'use_sim_time': use_sim_time}]
    )

    # 同时启动 rviz2，方便观察建图效果
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'use_sim_time',
            default_value=use_sim_time
        ),
        slam_node,
        rviz_node
    ])

