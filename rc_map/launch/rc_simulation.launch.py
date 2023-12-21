#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory, get_package_share_path

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.conditions import LaunchConfigurationEquals

#create RoboCon Type ARES for world
class RC_WORLD:
    RC = 'RC'

def rc_get_world_config(world_type):
    rc_world_configs = {
        RC_WORLD.RC:{
            'x': '11.8',
            'y': '0.5',
            'z': '-0.165403',
            'yaw': '3.14',
            'world_path': 'rc_world/rc_world.world'
        }
    }
    return rc_world_configs.get(world_type,None)

def generate_launch_description():  #这个函数是launch.py所必须的函数
     # Get the launch directory
    bringup_dir = get_package_share_directory('rc_map')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # Specify xacro path
    urdf_dir = get_package_share_path('rc_map') / 'urdf' / 'waking_robot.xacro'
    # urdf_dir = get_package_share_path('rc_map') / 'urdf' / 'test.xacro'


    # Create the launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')
    world = LaunchConfiguration('world')

    #DeclareLaunchArgume用于设置命令行参数
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Use simulation (Gazebo) clock if true'
    )
    
    declare_world_cmd = DeclareLaunchArgument(
        'world',
        default_value=RC_WORLD.RC,
        description='weison_pan choose for you'
    )

    declare_rviz_config_file_cmd = DeclareLaunchArgument(
        'rviz_config_file',
        default_value=os.path.join(bringup_dir, 'rviz', 'rviz2.rviz'),
        description='Full path to the RVIZ config file to use'
    )
        
    # 启动gazeboGUI(启动另外一个launch文件)
    gazebo_client_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')),
    )

    #开启节点,用于发布关节状态
    start_joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': ParameterValue(
                Command(['xacro ', str(urdf_dir)]), value_type=str
            ),
        }],
        output='screen'
    )
    #开启节点,用于发布机器人状态
    start_robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': ParameterValue(
                Command(['xacro ', str(urdf_dir)]), value_type=str
            ),
        }],
        output='screen'
    )

    #根据rviz中的rviz的配置信息,启动rviz
    start_rviz_cmd = Node(
        package='rviz2',
        namespace='',
        executable='rviz2',
        arguments=['-d' + os.path.join(bringup_dir, 'rviz', 'rviz2.rviz')]
    )

    def rc_create_gazebo_launch_group(world_type):
        world_config = rc_get_world_config(world_type)
        if world_config is None:
            return None

        return GroupAction(
            condition=LaunchConfigurationEquals('world', world_type),#检查配置项是否统一成功
            actions=[
                Node(
                    package='gazebo_ros',
                    executable='spawn_entity.py',
                    arguments=[
                        '-entity', 'robot',
                        '-topic', 'robot_description',
                        '-x', world_config['x'],
                        '-y', world_config['y'],
                        '-z', world_config['z'],
                        '-Y', world_config['yaw']
                    ],
                ),
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')),
                    launch_arguments={'world': os.path.join(bringup_dir, 'world', world_config['world_path'])}.items(),
                )
            ]
        )


    #创建了一个,是一个用于描述和组织一系列启动动作（Actions）的对象
    bringup_RC_cmd_group = rc_create_gazebo_launch_group(RC_WORLD.RC)

    ld = LaunchDescription()

    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_world_cmd)
    ld.add_action(declare_rviz_config_file_cmd)
    ld.add_action(gazebo_client_launch)
    ld.add_action(start_joint_state_publisher_cmd)
    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(bringup_RC_cmd_group)


    # ld.add_action(start_rviz_cmd)#启动rviz

    return ld