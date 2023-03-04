#!/bin/bash
set -e
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
apt-get install -y python3-pip \
                   python3-catkin-tools \
                   ros-$ROS_DISTRO-catkin \
                   ros-$ROS_DISTRO-gazebo-ros
pip3 install -r $SCRIPT_DIR/requirements.txt
