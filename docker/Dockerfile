
ARG ROS_DISTRO=melodic

FROM ros:$ROS_DISTRO
LABEL description="World creator"
SHELL ["/bin/bash", "-c"]
WORKDIR /catkin_ws/src/world_creator

# 1. Install basic requirements
RUN apt-get update && apt-get upgrade -y && apt-get install -y python3-pip

# 2. Install requirements
COPY install.sh install.sh
COPY requirements.txt requirements.txt
RUN ./install.sh

# 3. Copy files
COPY CMakeLists.txt CMakeLists.txt
COPY package.xml package.xml
COPY plugins/ plugins/

# 4. Build
RUN source /opt/ros/$ROS_DISTRO/setup.bash      &&  \
    cd ../../                                   &&  \
    catkin build

COPY models models
COPY scripts scripts
COPY worlds worlds
COPY zawrka zawrka
COPY start_creator.sh start_creator.sh
COPY start_gz.sh start_gz.sh