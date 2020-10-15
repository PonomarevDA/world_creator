cmake_minimum_required(VERSION 2.8.3)
project(world_creator)

set(TF_PLUGIN tf_plugin)

# Find other CMake/Catkin packages needed for build
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  gazebo_ros
)
find_package(gazebo REQUIRED)

# Specify package build info export
catkin_package(
  DEPENDS 
    roscpp 
    gazebo_ros 
)
link_directories(${GAZEBO_LIBRARY_DIRS})
include_directories(
	include
    plugins
    ${Boost_INCLUDE_DIR}
    ${GAZEBO_INCLUDE_DIRS}
	${catkin_INCLUDE_DIRS}
)

# Libraries/Executables to build
add_library(${TF_PLUGIN}
  plugins/traffic_light.cpp
)
target_link_libraries(${TF_PLUGIN}
  ${catkin_LIBRARIES}
  ${CAR_INTERFACE_PLUGIN}
)

# Install
install(
  TARGETS 
  ${TF_PLUGIN}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
)
install(
  DIRECTORY
    launch
    rviz
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

