cmake_minimum_required(VERSION 3.8)
project(warehouse_inventory_robot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(std_msgs REQUIRED)
find_package(warehouse_inventory_robot_msgs REQUIRED)

ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  warehouse_inventory_robot/inventory_manager.py
  warehouse_inventory_robot/warehouse_patrol.py
  warehouse_inventory_robot/zone_marker_publisher.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  launch
  worlds
  urdf
  rviz
  docs
  DESTINATION share/${PROJECT_NAME}
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
