#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from warehouse_inventory_robot_msgs.msg import InventoryAction


class InventoryManager(Node):
    """Receives robot inventory actions and maintains a simulated stock table."""

    def __init__(self):
        super().__init__("inventory_manager")
        self.stock = {"A1": 15, "B2": 8, "C3": 2, "D4": 12}
        self.create_subscription(InventoryAction, "inventory_action", self.action_callback, 10)
        self.get_logger().info("Inventory manager ready.")

    def action_callback(self, msg):
        if not msg.completed:
            self.get_logger().warning(f"Incomplete action received for zone {msg.zone_id}")
            return

        if msg.action == "PICK_ITEM":
            self.stock[msg.zone_id] = max(0, self.stock.get(msg.zone_id, 0) - 1)
        elif msg.action == "DROP_ITEM":
            self.stock[msg.zone_id] = self.stock.get(msg.zone_id, 0) + 1

        stock_count = self.stock.get(msg.zone_id, 0)
        self.get_logger().info(
            f"Zone {msg.zone_id}: {msg.action} complete, stock={stock_count}, "
            f"arrival_error={msg.distance_to_zone:.2f} m"
        )


def main(args=None):
    rclpy.init(args=args)
    node = InventoryManager()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
