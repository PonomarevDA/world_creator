# Gazebo sdf world creator

This is ROS package that allows quickly and easily create Gazebo worlds using GUI.

![Alt text](Img/fpi.jpg?raw=true "fpi")
![Alt text](Img/autonet.png?raw=true "autonet")

## Preparation

You must have installed Gazebo.

Then you should install required packages:

```bash
pip3 install -r requirements.txt
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
- Argument --name specify the output files prefix. Generete button will always generate 2 files: example.json and example.world

**Loading of creating world**

```bash
./start_creator.sh --load worlds/example.json --name worlds/example
```
- Argument --load specify the input json file
- Argument --name specify the output prefix of generated files

**Running created gazebo world**

```bash
./start_gz.sh worlds/example.world
```

If you want to run a world in your application, don't forget to set up `GAZEBO_MODEL_PATH`.

## For developer:

`world_creator.py` is the main script. It runs GUI and parses arguments.

`gui.py` is the frontend of this program. It creates main window, lables, buttons, sets callbacks and allow to create json and world files.

`converter.py` allows to convert frontend data to json format, load json data to frontend and to backend.

`gazebo_sdf.py` is the backend of this program. It allows to create .world file from json file.

`data_structures.py` contains the basic type like Size2D and Point2D.

`objects.py` contains objects like Wall, Box, Sign, Traffic light.

`gazebo_objects.py` contains improved objects from objects.py which is using in gazebo_sdf.py.
