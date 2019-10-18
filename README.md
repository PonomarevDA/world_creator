# Gazebo sdf world creator
These scripts allow to create Gazebo sdf world from gui.

### How to create a world
Firstly, you should install required packages:

`. install.sh`

Then you should run the main script and configure the map as you like:

`python3 world_creator.py`

After that you should consistently click on buttons `create json` and `create sdf from json`.

### Description
`world_creator.py` is the main script. It runs GUI.

`gui_new.py` and `gui_old.py` are the frontend of this program. They create main window, lables, buttons and sets callbacks.

`json_converter.py` allows to convert frontend data to json format, load json data to frontend and to backend.

`gazebo_sdf.py` is the backend of this program. It allows to create .world file from json file. 

`box.world` and `empty_world.world` are templates of object and empty world. `gazebo_sdf.py` required for these.

`tests.py` is the test script that allows to create json.

`data_file.json` is the example of json file. 
