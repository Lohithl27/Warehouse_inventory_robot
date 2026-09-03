from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
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
        ]
    )
