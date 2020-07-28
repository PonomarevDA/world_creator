# Gazebo sdf world creator
This package allow to create Gazebo sdf world from gui.

### How to create a world
Firstly, you should install required packages:

```bash
pip3 install -r requirements.txt
```

Then you should run the main script and configure the map as you like:

```bash
./start_creator.sh
```

If you want to see new world:

```bash
./start_gz.sh new_world.world
```

### Scripts description
`world_creator.py` is the main script. It runs GUI and parses arguments.

`gui.py` is the frontend of this program. It creates main window, lables, buttons, sets callbacks and allow to create json and world files.

`converter.py` allows to convert frontend data to json format, load json data to frontend and to backend.

`gazebo_sdf.py` is the backend of this program. It allows to create .world file from json file.

`data_structures.py` contains the basic type like Size2D and Point2D.

`objects.py` contains objects like Wall, Box, Sign, Traffic light.

`gazebo_objects.py` contains improved objects from objects.py which is using in gazebo_sdf.py.
