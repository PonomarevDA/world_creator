#!/usr/bin/env python3

"""
This script allow create json file from data and sdf file from json.
"""

import json
from gazebo_sdf import *

# Input-output settings
JSON_DEFAULT_NAME = "data_file.json"
SDF_DEFAULT_NAME = "world.world"

# JSON format settings
START_POSITION_NAME = "start"
FINISH_POSITION_NAME = "finish"
SIZE_NAME = "size"
OBJECTS_NAME = "objects"
OBJECTS_NAME_FIELD_NAME = "name"
OBJECTS_POSITION_FIELD_NAME = "position"
BOX_NAME = "box"
VERTICAL_WALL_NAME = "vertical_wall"
HORIZONTAL_WALL_NAME = "horizontal_wall"

def create_json_from_gui(start_x, start_y, SIZE_X, SIZE_Y, boxesStatus, vWallsStatus, hWallsStatus):
    """ 
    Create json file using frontend data
    """
    write_file = open(JSON_DEFAULT_NAME, "w")
    objects = list()
    for r in range(0, len(boxesStatus)):
        for c in range(0, len(boxesStatus[0])):
            if boxesStatus[r][c] == True:
                obj = dict([(OBJECTS_NAME_FIELD_NAME, BOX_NAME), (OBJECTS_POSITION_FIELD_NAME, [c, r])])
                objects.append(obj)
    for r in range(0, len(vWallsStatus)):
        for c in range(0, len(vWallsStatus[0])):
            if vWallsStatus[r][c] == True:
                obj = dict([(OBJECTS_NAME_FIELD_NAME, VERTICAL_WALL_NAME), (OBJECTS_POSITION_FIELD_NAME, [c, r])])
                objects.append(obj)
    for r in range(0, len(hWallsStatus)):
        for c in range(0, len(hWallsStatus[0])):
            if hWallsStatus[r][c] == True:
                obj = dict([(OBJECTS_NAME_FIELD_NAME, HORIZONTAL_WALL_NAME), (OBJECTS_POSITION_FIELD_NAME, [c, r])])
                objects.append(obj)

    data = dict([(START_POSITION_NAME, [start_x, start_y] ),
                 (FINISH_POSITION_NAME, [0, 0] ),
                 (SIZE_NAME, [SIZE_X, SIZE_Y]),
                 (OBJECTS_NAME, objects)])
    print(data)
    json.dump(data, write_file, indent=2)


def create_sdf_from_json(jsonFileName=JSON_DEFAULT_NAME, sdfFileName=SDF_DEFAULT_NAME):
    """ 
    Create world using json data
    """
    read_file = open(jsonFileName, "r")
    data = json.load(read_file)

    sdfCreator = SdfCreator(data.get(START_POSITION_NAME)[0],
                            data.get(START_POSITION_NAME)[1],
                            data.get(SIZE_NAME)[0],
                            data.get(SIZE_NAME)[1])
    for obj in data.get(OBJECTS_NAME):
        position = obj.get(OBJECTS_POSITION_FIELD_NAME)
        if obj.get(OBJECTS_NAME_FIELD_NAME) == BOX_NAME:
            sdfCreator.addBox(position[0], position[1])
        if obj.get(OBJECTS_NAME_FIELD_NAME) == HORIZONTAL_WALL_NAME:
            sdfCreator.addHorizontalWall(position[0], position[1])
        if obj.get(OBJECTS_NAME_FIELD_NAME) == VERTICAL_WALL_NAME:
            sdfCreator.addVerticalWall(position[0], position[1])
    sdfCreator.writeWorldToFile(sdfFileName)

