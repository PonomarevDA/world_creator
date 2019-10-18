#!/usr/bin/env python3

"""
This script allow create json file from data and sdf file from json.
"""

import json
from gazebo_sdf import *

# File input-output default settings
JSON_DEFAULT_NAME = "data_file.json"
SDF_DEFAULT_NAME = "world.world"

# JSON format settings
class JsonNames:
    START = "start"
    FINISH = "finish"
    SIZE = "size"
    OBJECTS = "objects"
    NAME = "name"
    POSITION = "position"
    POINT_1 = "point1"
    POINT_2 = "point2"
    BOX = "box"
    WALL = "wall"

# Cheet sheet
"""
Data types:
- High level: indexes of cells or nodes (user and frontend work with them)
- JSON level: map position
- Low level: gazebo world position - user shouldn't think about it (private 
  backend methods uses it, we need it because of the start position offset)

Frontend v.2 data:
1.  start       indexes (cell)      list of x and y
2.  end         indexes (cell)      list of x and y
3.  size        meters              list of x and y
4.  boxes
5.  walls       indexes (node)      list of few 2x2 arrays

Json data:
1.  start       map_pose            list of x and y
2.  end         map_pose            list of x and y
3.  size        meters              list of x and y
4.  boxes
5.  walls       map_pose            list of few 2x2 arrays
"""


# Wall position transformation:
def map_pose_to_node_indexes(mapPose):
    return list([ int(mapPose[0] / 2), int(mapPose[1] / 2) ])
def node_indexes_to_map_pose(nodeIndexes):
    return list([ nodeIndexes[0] * 2, nodeIndexes[1] * 2 ])

# Start/End pose transformation:
def map_pose_to_cell_indexes(mapPose):
    return list([ int((mapPose[0] - 1) / 2), int((mapPose[1] - 1) / 2) ])
def cell_indexes_to_map_pose(cellIndexes):
    return list([ cellIndexes[0] * 2 + 1, cellIndexes[1] * 2 + 1 ])


def create_json_from_gui2(start, size, boxes, walls):
    """ 
    Create json file using frontend data
    """
    write_file = open(JSON_DEFAULT_NAME, "w")
    objects = list()
    for wall in walls:
        wall = dict([ (JsonNames.NAME, JsonNames.WALL), 
                      (JsonNames.POINT_1, node_indexes_to_map_pose(wall[0])), 
                      (JsonNames.POINT_2, node_indexes_to_map_pose(wall[1])) ])
        objects.append(wall)
    data = dict([(JsonNames.START, cell_indexes_to_map_pose(start)),
                 (JsonNames.FINISH, [0, 0]),
                 (JsonNames.SIZE, size),
                 (JsonNames.OBJECTS, objects)])
    print(data)
    json.dump(data, write_file, indent=2)

def create_json_from_gui(start_x, start_y, SIZE_X, SIZE_Y, boxesStatus, 
                         vWallsStatus, hWallsStatus):
    """ 
    Create json file using frontend data
    """
    # To do: fix backend in future to reduce number of input variables
    start = [start_x, start_y]
    finish = [0, 0]
    size = [SIZE_X, SIZE_Y]

    write_file = open(JSON_DEFAULT_NAME, "w")
    objects = list()
    for r in range(0, len(boxesStatus)):
        for c in range(0, len(boxesStatus[0])):
            if boxesStatus[r][c] == True:
                obj = dict([(JsonNames.NAME, JsonNames.BOX),
                            (JsonNames.POSITION, [c, r])])
                objects.append(obj)
    for r in range(0, len(vWallsStatus)):
        for c in range(0, len(vWallsStatus[0])):
            if vWallsStatus[r][c] == True:
                point1 = [ c * 2, r * 2 ]
                point2 = [ c * 2, r * 2 + 2 ]
                wall = dict([(JsonNames.NAME, JsonNames.WALL), 
                             (JsonNames.POINT_1, point1), 
                             (JsonNames.POINT_2, point2)])
                objects.append(wall)
    for r in range(0, len(hWallsStatus)):
        for c in range(0, len(hWallsStatus[0])):
            if hWallsStatus[r][c] == True:
                point1 = [ c * 2, r * 2 ]
                point2 = [ c * 2 + 2, r * 2 ]
                wall = dict([(JsonNames.NAME, JsonNames.WALL),
                             (JsonNames.POINT_1, point1),
                             (JsonNames.POINT_2, point2)])
                objects.append(wall)

    data = dict([(JsonNames.START, cell_indexes_to_map_pose(start)),
                 (JsonNames.FINISH, finish ),
                 (JsonNames.SIZE, size),
                 (JsonNames.OBJECTS, objects)])
    print("create_json_from_gui: " + str(data))
    json.dump(data, write_file, indent=2)


def create_sdf_from_json(jsonFileName=JSON_DEFAULT_NAME, sdfFileName=SDF_DEFAULT_NAME):
    """ 
    Create world using json data
    """
    read_file = open(jsonFileName, "r")
    data = json.load(read_file)

    sdfCreator = SdfCreator(data.get(JsonNames.START),
                            data.get(JsonNames.FINISH),
                            data.get(JsonNames.SIZE))
    for obj in data.get(JsonNames.OBJECTS):
        if obj.get(JsonNames.NAME) == JsonNames.BOX:
            position = obj.get(JsonNames.POSITION)
            sdfCreator.addBox(position[0], position[1])
        elif obj.get(JsonNames.NAME) == JsonNames.WALL:
            point1 = obj.get(JsonNames.POINT_1)
            point2 = obj.get(JsonNames.POINT_2)
            sdfCreator.addWall(point1, point2)
    sdfCreator.writeWorldToFile(sdfFileName)


def load_backend_from_json(fileName = JSON_DEFAULT_NAME):
    read_file = open(fileName, "r")
    data = json.load(read_file)

    walls = list()
    boxes = list()
    for obj in data.get(JsonNames.OBJECTS):
        if obj.get(JsonNames.NAME) == JsonNames.BOX:
            position = obj.get(JsonNames.POSITION)
            boxes.append(position)
        elif obj.get(JsonNames.NAME) == JsonNames.WALL:
            p1 = map_pose_to_node_indexes(obj.get(JsonNames.POINT_1))
            p2 = map_pose_to_node_indexes(obj.get(JsonNames.POINT_2))
            walls.append([p1, p2])

    return list([map_pose_to_cell_indexes(data.get(JsonNames.START)),
                 map_pose_to_cell_indexes(data.get(JsonNames.FINISH)),
                 data.get(JsonNames.SIZE),
                 boxes,
                 walls])


