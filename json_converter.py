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
- JSON (user) level: it uses only map position in meters
- Frontend level: indexes of cells and nodes (they are more conveniente to use
  because QPaint window is divided into cells and real cell sizes in meters
  are not interesting in this abstraction level)
- Low level: gazebo world position - (robot should spawn in (0,0) gazebo
  position, but user think in his abstraction level that start position can be
  any, so backend methods use start position offset)

Frontend v.2 data:
1.  start       indexes (cell)      list of x and y
2.  end         indexes (cell)      list of x and y
3.  size        meters              list of x and y
4.  boxes       indexes (cell)      list of x and y
5.  walls       indexes (node)      list of few 2x2 arrays

Json data:
1.  start       meters              list of x and y
2.  end         meters              list of x and y
3.  size        meters              list of x and y
4.  boxes       meters              list of x and y
5.  walls       meters              list of few 2x2 arrays
"""


# Wall position transformation:
def __map_pose_to_node_indexes(mapPose):
    return list([ int(mapPose[0] / 2), int(mapPose[1] / 2) ])
def __node_indexes_to_map_pose(nodeIndexes):
    return list([ nodeIndexes[0] * 2, nodeIndexes[1] * 2 ])

# Start/End pose transformation:
def __map_pose_to_cell_indexes(mapPose):
    return list([ int((mapPose[0] - 1) / 2), int((mapPose[1] - 1) / 2) ])
def __cell_indexes_to_map_pose(cellIndexes):
    return list([ cellIndexes[0] * 2 + 1, cellIndexes[1] * 2 + 1 ])


def create_json_from_gui(start, size, boxes, walls):
    """ 
    Create json file using frontend data
    """
    write_file = open(JSON_DEFAULT_NAME, "w")
    objects = list()
    for wall in walls:
        wall = dict([ (JsonNames.NAME, JsonNames.WALL), 
                   (JsonNames.POINT_1, __node_indexes_to_map_pose(wall[0])),
                   (JsonNames.POINT_2, __node_indexes_to_map_pose(wall[1])) ])
        objects.append(wall)
    data = dict([(JsonNames.START, __cell_indexes_to_map_pose(start)),
                 (JsonNames.FINISH, [0, 0]),
                 (JsonNames.SIZE, size),
                 (JsonNames.OBJECTS, objects)])
    print(data)
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
            sdfCreator.addBox(position)
        elif obj.get(JsonNames.NAME) == JsonNames.WALL:
            point1 = obj.get(JsonNames.POINT_1)
            point2 = obj.get(JsonNames.POINT_2)
            sdfCreator.addWall(point1, point2)
    sdfCreator.writeWorldToFile(sdfFileName)


def load_frontend_from_json(fileName = JSON_DEFAULT_NAME):
    read_file = open(fileName, "r")
    data = json.load(read_file)

    walls = list()
    boxes = list()
    for obj in data.get(JsonNames.OBJECTS):
        if obj.get(JsonNames.NAME) == JsonNames.BOX:
            position = obj.get(JsonNames.POSITION)
            boxes.append(position)
        elif obj.get(JsonNames.NAME) == JsonNames.WALL:
            p1 = __map_pose_to_node_indexes(obj.get(JsonNames.POINT_1))
            p2 = __map_pose_to_node_indexes(obj.get(JsonNames.POINT_2))
            walls.append([p1, p2])

    return list([__map_pose_to_cell_indexes(data.get(JsonNames.START)),
                 __map_pose_to_cell_indexes(data.get(JsonNames.FINISH)),
                 data.get(JsonNames.SIZE),
                 boxes,
                 walls])


