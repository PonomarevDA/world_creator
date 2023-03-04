#!/bin/bash
set -e 
apt-get install -y python3-pip \
                   python3-catkin-tools \
                   ros-$ROS_DISTRO-catkin \
                   ros-$ROS_DISTRO-gazebo-ros
pip3 install -r requirements.txt
