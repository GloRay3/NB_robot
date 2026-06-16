import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    # 获取路径
    navi_bot_dir = get_package_share_directory('navi_bot')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    # 地图和参数文件
    map_yaml_path = launch.substitutions.LaunchConfiguration(
        'map',
        default=os.path.join(navi_bot_dir, 'maps', 'maze.yaml')
    )
    nav2_param_path = launch.substitutions.LaunchConfiguration(
        'params_file',
        default=os.path.join(navi_bot_dir, 'config', 'nav2_params.yaml')
    )
    use_sim_time = launch.substitutions.LaunchConfiguration(
        'use_sim_time',
        default='true'
    )

    # 相对路径拼接，使用 navigation2 默认 rviz 文件
    rviz_config = os.path.join(
        nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')

    # 启动 
    nav2_launch = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [nav2_bringup_dir, '/launch', '/bringup_launch.py']
        ),
        launch_arguments={
            'map': map_yaml_path,
            'use_sim_time': use_sim_time,
            'params_file': nav2_param_path,
            'autostart': 'true'
        }.items()
    )

    # # 启动 rviz2
    # rviz_node = launch_ros.actions.Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     name='rviz2',
    #     arguments=['-d', rviz_config],
    #     parameters=[{'use_sim_time': use_sim_time}],
    #     output='screen'
    # )


  # 返回所有需要启动的内容
    return launch.LaunchDescription([
        # 声明地图参数
        launch.actions.DeclareLaunchArgument(
            'map',
            default_value=map_yaml_path
        ),
        # 声明文件参数
        launch.actions.DeclareLaunchArgument(
            'params_file',
            default_value=nav2_param_path
        ),
        # 声明仿真时间
        launch.actions.DeclareLaunchArgument(
            'use_sim_time',
            default_value=use_sim_time
        ),
        nav2_launch,
        # rviz_node
    ])

