# Warehouse Inventory Robot ROS 2 Workspace

This is the full ROS 2 workspace layout for the Major Project - 1 assignment.

## Folder Pattern

```text
warehouse_ws/
  README.md
  src/
    warehouse_inventory_robot/
      package.xml
      CMakeLists.txt
      launch/
      msg/
      urdf/
      worlds/
      rviz/
      docs/
      warehouse_inventory_robot/
```

## Build

Run these commands on Ubuntu 22.04 with ROS 2 Humble:

```bash
cd warehouse_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## Run

```bash
ros2 launch warehouse_inventory_robot simulation.launch.py
```

The package source is inside:

```text
warehouse_ws/src/warehouse_inventory_robot
```
