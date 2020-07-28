# Gazebo sdf world creator

This package allows quickly and easily create Gazebo words using GUI.

### Preparation

You must have installed Gazebo.

Then you shoold install required packages:

```bash
pip3 install -r requirements.txt
```

### How to use GUI

Example:

```bash
./start_creator.sh --load worlds/world2.json
```

For more information use help:

```bash
./start_creator.sh --help
```

### How run world in gazebo

```bash
./start_gz.sh worlds/world2.world
```

where new_world.world is a location of your world file.

If you want to run a world in your application, don't forget to set up GAZEBO_MODEL_PATH.

### For developer:

`world_creator.py` is the main script. It runs GUI and parses arguments.

`gui.py` is the frontend of this program. It creates main window, lables, buttons, sets callbacks and allow to create json and world files.

`converter.py` allows to convert frontend data to json format, load json data to frontend and to backend.

`gazebo_sdf.py` is the backend of this program. It allows to create .world file from json file.

`data_structures.py` contains the basic type like Size2D and Point2D.

`objects.py` contains objects like Wall, Box, Sign, Traffic light.

`gazebo_objects.py` contains improved objects from objects.py which is using in gazebo_sdf.py.
