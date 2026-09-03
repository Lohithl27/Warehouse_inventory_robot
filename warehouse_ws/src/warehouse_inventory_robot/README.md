# Warehouse Inventory Robot

ROS 2 Humble project for simulating an autonomous warehouse inventory robot in Gazebo and RViz.

## Project Features

- Custom Gazebo warehouse world with racks, walls, obstacle, and four inventory zones.
- Differential-drive warehouse robot with lidar, odometry, and `cmd_vel` control.
- Autonomous waypoint patrol through zones A1, B2, C3, and D4.
- Simple obstacle avoidance using laser scan data.
- Custom ROS 2 message for inventory actions.
- Inventory manager node that updates simulated stock counts.
- RViz markers for inventory zones and robot visualization.

## Folder Structure

```text
warehouse_inventory_robot/
  launch/
    simulation.launch.py
    nodes_only.launch.py
  msg/
    InventoryAction.msg
  rviz/
    warehouse_inventory.rviz
  urdf/
    warehouse_bot.urdf.xacro
  warehouse_inventory_robot/
    inventory_manager.py
    warehouse_patrol.py
    zone_marker_publisher.py
  worlds/
    warehouse.world
  docs/
    PROJECT_REPORT.md
```

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Classic with `gazebo_ros`
- RViz2

Install common dependencies:

```bash
sudo apt update
sudo apt install -y ros-humble-desktop ros-humble-gazebo-ros-pkgs ros-humble-xacro
```

## Build

Copy this package into the `src` folder of a ROS 2 workspace:

```bash
mkdir -p ~/warehouse_ws/src
cp -r warehouse_inventory_robot ~/warehouse_ws/src/
cd ~/warehouse_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## Run Full Simulation

```bash
ros2 launch warehouse_inventory_robot simulation.launch.py
```

This starts:

- Gazebo with the warehouse world.
- The warehouse robot model.
- Robot state publisher.
- Patrol controller.
- Inventory manager.
- RViz zone marker publisher.
- RViz visualization.

## Run Nodes Only

Use this when another simulator or real robot is already publishing `/odom`, `/scan`, and subscribing to `/cmd_vel`.

```bash
ros2 launch warehouse_inventory_robot nodes_only.launch.py
```

## Important Topics

- `/cmd_vel`: velocity commands sent to the robot.
- `/odom`: robot position from Gazebo diff drive plugin.
- `/scan`: lidar scan used for obstacle avoidance.
- `/inventory_action`: custom inventory action message.
- `/inventory_zones`: RViz marker array for zones.

## Expected Demo

1. Robot starts near the center of the warehouse.
2. It drives toward zone A1 and publishes `CHECK_STOCK`.
3. It continues to zone B2 and publishes `PICK_ITEM`.
4. It continues to zone C3 and publishes `DROP_ITEM`.
5. It continues to zone D4 and publishes `CHECK_STOCK`.
6. Inventory manager logs the simulated stock result for each zone.

## Troubleshooting

- If Gazebo opens but the robot does not appear, check that `gazebo_ros` and `xacro` are installed.
- If RViz shows fixed frame errors, make sure `simulation.launch.py` is running because it publishes the `map -> odom` transform.
- If the robot spins near an obstacle, move the obstacle in `worlds/warehouse.world` or increase the patrol controller clearance threshold.
