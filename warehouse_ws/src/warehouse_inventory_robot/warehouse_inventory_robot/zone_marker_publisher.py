#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray


class ZoneMarkerPublisher(Node):
    """Publishes RViz markers for warehouse inventory zones."""

    def __init__(self):
        super().__init__("zone_marker_publisher")
        self.publisher = self.create_publisher(MarkerArray, "inventory_zones", 10)
        self.zones = [
            ("A1", 2.0, 1.4, 0.1, 0.7, 0.2),
            ("B2", 2.0, -1.4, 0.1, 0.3, 0.9),
            ("C3", -2.0, -1.4, 0.9, 0.6, 0.1),
            ("D4", -2.0, 1.4, 0.8, 0.2, 0.6),
        ]
        self.create_timer(1.0, self.publish_markers)

    def publish_markers(self):
        markers = MarkerArray()
        for index, (zone_id, x, y, r, g, b) in enumerate(self.zones):
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "inventory_zones"
            marker.id = index
            marker.type = Marker.CUBE
            marker.action = Marker.ADD
            marker.pose.position.x = x
            marker.pose.position.y = y
            marker.pose.position.z = 0.05
            marker.scale.x = 0.55
            marker.scale.y = 0.55
            marker.scale.z = 0.1
            marker.color.r = r
            marker.color.g = g
            marker.color.b = b
            marker.color.a = 0.85
            markers.markers.append(marker)

            label = Marker()
            label.header = marker.header
            label.ns = "inventory_zone_labels"
            label.id = index + 100
            label.type = Marker.TEXT_VIEW_FACING
            label.action = Marker.ADD
            label.pose.position.x = x
            label.pose.position.y = y
            label.pose.position.z = 0.55
            label.scale.z = 0.28
            label.color.r = 1.0
            label.color.g = 1.0
            label.color.b = 1.0
            label.color.a = 1.0
            label.text = zone_id
            markers.markers.append(label)

        self.publisher.publish(markers)


def main(args=None):
    rclpy.init(args=args)
    node = ZoneMarkerPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
