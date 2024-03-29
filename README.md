# Gazebo SDF World Creator ![catkin_build](https://github.com/PonomarevDA/world_creator/actions/workflows/catkin_build.yml/badge.svg?branch=main)


This is a ROS package that allows quick and easy creation of Gazebo worlds using a GUI.

![Alt text](Img/fpi.jpg?raw=true "fpi")
![Alt text](Img/autonet.png?raw=true "autonet")

## Preparation

You must have Gazebo installed.

You should then install the required packages:

```bash
./install.sh
```

## Usage

**Getting help**

```bash
./start_creator.sh --help
```

**Creation of a new world**

```bash
./start_creator.sh --cell 0.5x0.5 --size 30x30 --name worlds/example
```
--name specifies the prefix of the output files. The generated button will always generate 2 files: example.json and example.world

**Loading of creating world**

```bash
./start_creator.sh --load worlds/example.json --name worlds/example
```
--load specifies the input json file
--name specifies the output prefix of generated files

**Running created gazebo world**

```bash
./start_gz.sh worlds/example.world
```

If you want to run a world in your application, don't forget to set up `GAZEBO_MODEL_PATH`.

## For developer:

`world_creator.py` is the main script. It runs GUI and parses arguments.

`gui.py` is the frontend of this program. It creates main window, labels, buttons, sets callbacks and allow to create json and world files.

`converter.py` allows to convert frontend data to json format, load json data to frontend and to backend.

`gazebo_sdf.py` is the backend of this program. It allows to create .world file from json file.

`data_structures.py` contains the basic type like Size2D and Point2D.

`objects.py` contains objects like Wall, Box, Sign, Traffic light.

`gazebo_objects.py` contains improved objects from objects.py which is using in gazebo_sdf.py.
