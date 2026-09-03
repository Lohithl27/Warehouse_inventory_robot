from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare("warehouse_inventory_robot")
    world = PathJoinSubstitution([pkg_share, "worlds", "warehouse.world"])
    robot_description_file = PathJoinSubstitution([pkg_share, "urdf", "warehouse_bot.urdf.xacro"])
    rviz_config = PathJoinSubstitution([pkg_share, "rviz", "warehouse_inventory.rviz"])

    robot_description = {
        "robot_description": Command([FindExecutable(name="xacro"), " ", robot_description_file])
    }

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare("gazebo_ros"), "launch", "gazebo.launch.py"])
        ),
        launch_arguments={"world": world}.items(),
    )

    return LaunchDescription(
        [
            gazebo,
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[robot_description],
            ),
            Node(
                package="gazebo_ros",
                executable="spawn_entity.py",
                arguments=["-topic", "robot_description", "-entity", "warehouse_bot", "-x", "0", "-y", "0", "-z", "0.08"],
                output="screen",
            ),
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                arguments=["0", "0", "0", "0", "0", "0", "map", "odom"],
                output="screen",
            ),
            Node(
                package="warehouse_inventory_robot",
                executable="warehouse_patrol.py",
                name="warehouse_patrol",
                output="screen",
            ),
            Node(
                package="warehouse_inventory_robot",
                executable="inventory_manager.py",
                name="inventory_manager",
                output="screen",
            ),
            Node(
                package="warehouse_inventory_robot",
                executable="zone_marker_publisher.py",
                name="zone_marker_publisher",
                output="screen",
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                arguments=["-d", rviz_config],
                output="screen",
            ),
        ]
    )
