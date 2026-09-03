#!/usr/bin/env python3
import math
from dataclasses import dataclass

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

from warehouse_inventory_robot_msgs.msg import InventoryAction


@dataclass
class Zone:
    zone_id: str
    x: float
    y: float
    action: str


class WarehousePatrol(Node):
    """Waypoint controller with simple laser-based obstacle avoidance."""

    def __init__(self):
        super().__init__("warehouse_patrol")
        self.zones = [
            Zone("A1", 2.0, 1.4, "CHECK_STOCK"),
            Zone("B2", 2.0, -1.4, "PICK_ITEM"),
            Zone("C3", -2.0, -1.4, "DROP_ITEM"),
            Zone("D4", -2.0, 1.4, "CHECK_STOCK"),
        ]
        self.zone_index = 0
        self.pose = None
        self.front_clearance = float("inf")
        self.zone_hold_until = None
        self.visited_current_zone = False

        self.cmd_pub = self.create_publisher(Twist, "cmd_vel", 10)
        self.action_pub = self.create_publisher(InventoryAction, "inventory_action", 10)
        self.create_subscription(Odometry, "odom", self.odom_callback, 10)
        self.create_subscription(LaserScan, "scan", self.scan_callback, 10)
        self.create_timer(0.1, self.control_loop)
        self.get_logger().info("Warehouse patrol node started.")

    def odom_callback(self, msg):
        q = msg.pose.pose.orientation
        yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))
        self.pose = (msg.pose.pose.position.x, msg.pose.pose.position.y, yaw)

    def scan_callback(self, msg):
        ranges = [r for r in msg.ranges if msg.range_min < r < msg.range_max]
        if not ranges:
            self.front_clearance = float("inf")
            return

        center = len(msg.ranges) // 2
        window = msg.ranges[max(0, center - 15): min(len(msg.ranges), center + 16)]
        valid = [r for r in window if msg.range_min < r < msg.range_max]
        self.front_clearance = min(valid) if valid else float("inf")

    def control_loop(self):
        if self.pose is None:
            return

        if self.zone_hold_until is not None:
            self.cmd_pub.publish(Twist())
            if self.get_clock().now().nanoseconds >= self.zone_hold_until:
                self.zone_index = (self.zone_index + 1) % len(self.zones)
                self.zone_hold_until = None
                self.visited_current_zone = False
            return

        zone = self.zones[self.zone_index]
        x, y, yaw = self.pose
        dx = zone.x - x
        dy = zone.y - y
        distance = math.hypot(dx, dy)
        target_yaw = math.atan2(dy, dx)
        heading_error = self.normalize_angle(target_yaw - yaw)

        cmd = Twist()
        if self.front_clearance < 0.55:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.7
            self.cmd_pub.publish(cmd)
            return

        if distance < 0.25:
            self.publish_inventory_action(zone, distance)
            self.zone_hold_until = self.get_clock().now().nanoseconds + int(2.0e9)
            return

        cmd.angular.z = max(min(1.4 * heading_error, 1.0), -1.0)
        if abs(heading_error) < 0.65:
            cmd.linear.x = min(0.35, 0.45 * distance)
        self.cmd_pub.publish(cmd)

    def publish_inventory_action(self, zone, distance):
        if self.visited_current_zone:
            return
        msg = InventoryAction()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "map"
        msg.zone_id = zone.zone_id
        msg.action = zone.action
        msg.completed = True
        msg.distance_to_zone = float(distance)
        self.action_pub.publish(msg)
        self.visited_current_zone = True
        self.get_logger().info(f"Inventory action completed: {zone.action} at zone {zone.zone_id}")

    @staticmethod
    def normalize_angle(angle):
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle


def main(args=None):
    rclpy.init(args=args)
    node = WarehousePatrol()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
