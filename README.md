# Gazebo sdf world creator

This package allows quickly and easily create Gazebo worlds especially mazes using GUI.

The limitation of this package is that it is considered that each walls and objects in the world can be placed in the discretize space.
You can see the example of gui below.
![Alt text](Img/example.jpg?raw=true "Title")

So, the space of gui is divided into 2 parts: grid representing the world and buttons that allow you to choose which objects you are working with. Once you press any button, your left mouse clock at the grid will create an object. You always can delete created object using right click.
Note: While you can create such objects like `Box`, `Sign`, etc using only 1 click, `Walls`, `Windows` and `Doors` require at least 2 clicks. To simplify their creating, only continuous mode is avaliable. It means that to start creating you need press left button and to stop you need to press right button.

## Preparation

You must have installed Gazebo.

Then you should install required packages:

```bash
pip3 install -r requirements.txt
```

## How to use GUI

To get help just type:

```bash
./start_creator.sh --help
```

If you want to create new world, probably you want to specify the number of grids and their size. So, you should type:

```bash
./start_creator.sh --cell 0.5x0.5 --size 30x30 --name worlds/example
```
- Such arguments like --cell and --size don't need any description
- Argument --name specify the output files prefix. Generete button will always generate 2 files: example.json and example.world


If you want to load existing maze from json you should type:

```bash
./start_creator.sh --load worlds/example.json --name worlds/example
```
- Argument --load specify the input json file
- Argument --name specify the output prefix of generated files



## How to run a created gazebo world

Example:

```bash
./start_gz.sh worlds/world2.world
```

where `new_world.world` is a location of your world file.

If you want to run a world in your application, don't forget to set up `GAZEBO_MODEL_PATH`.

## For developer:

`world_creator.py` is the main script. It runs GUI and parses arguments.

`gui.py` is the frontend of this program. It creates main window, lables, buttons, sets callbacks and allow to create json and world files.

`converter.py` allows to convert frontend data to json format, load json data to frontend and to backend.

`gazebo_sdf.py` is the backend of this program. It allows to create .world file from json file.

`data_structures.py` contains the basic type like Size2D and Point2D.

`objects.py` contains objects like Wall, Box, Sign, Traffic light.

`gazebo_objects.py` contains improved objects from objects.py which is using in gazebo_sdf.py.
