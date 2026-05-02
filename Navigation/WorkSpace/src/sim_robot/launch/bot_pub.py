# 用于发布turtlebot3_waffle_pi的urdf文件及发布静态tf变换以及启动rviz2可视化界面
# 导入必要的库
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    # 将环境变量默认设置为'turtlebot3_waffle_pi'。默认启动turtleaffle_pi模型的urdf文件
    TURTLEBOT3_MODEL = os.environ.get('TURTLEBOT3_MODEL', 'waffle_pi')
    # 设置命名空间参数，默认为''
    namespace = LaunchConfiguration('namespace')

    # 设置是否使用仿真时间参数，默认为'false'.如果启动gazebo仿真环境，将该参数设置为'true'(通过启动命令行或者修改此源码)
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    urdf_file_name = 'turtlebot3_' + TURTLEBOT3_MODEL + '.urdf'

    print('urdf_file_name : {}'.format(urdf_file_name))

    urdf = os.path.join(
        get_package_share_directory('sim_robot'),
        'urdf',
        urdf_file_name)
    robot_desc = Command([
        'xacro ',
        urdf,
        ' namespace:=',
        PythonExpression(['"', namespace, '" + "/" if "', namespace, '" != "" else ""']),
    ])


    rsp_params = {'robot_description': robot_desc}

    # 导入rviz默认配置文件路径
    # rviz_config_dir = os.path.join(
    #     get_package_share_directory('sim_robot'),
    #     'config',
    #     'rviz2',
    #     'default.rviz')
    rviz_config_dir = os.path.join(
       get_package_share_directory('nav2_bringup'),
        'rviz',
        'nav2_default_view.rviz')
    return LaunchDescription([
        # 设置命名空间参数,默认为'bot'
        DeclareLaunchArgument(
            'namespace',
            default_value='',
            description='Namespace for the robot'),
        # 设置是否使用仿真时间参数,次高优先级(命令行权限最高)
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        # 启动robot_state_publisher节点，发布机器人urdf信息
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[
                    rsp_params,
                    {'use_sim_time': use_sim_time}]),
        
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            parameters=[{'use_sim_time': True}],
            arguments=['-d', rviz_config_dir],
            output='screen'),
        
    ])



    
  