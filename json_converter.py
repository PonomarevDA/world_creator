#!/usr/bin/env python3

"""
This script allow create json file from data and sdf file from json.
"""

import json
from gazebo_sdf import *

JSON_DEFAULT_NAME = "data_file.json"
SDF_DEFAULT_NAME = "world.world"

def create_json_from_gui(start_x, start_y, SIZE_X, SIZE_Y, cellsStatus, veStatus, heStatus):
    write_file = open(JSON_DEFAULT_NAME, "w")
    cells = list()
    vEdge = list()
    hEdge = list()
    for r in range(0, len(cellsStatus)):
        for c in range(0, len(cellsStatus[0])):
            if cellsStatus[r][c] == True:
                cells.append([c, r])
    for r in range(0, len(veStatus)):
        for c in range(0, len(veStatus[0])):
            if veStatus[r][c] == True:
                vEdge.append([c, r])
    for r in range(0, len(heStatus)):
        for c in range(0, len(heStatus[0])):
            if heStatus[r][c] == True:
                hEdge.append([c, r])

    data = dict([("start_x", start_x),
                 ("start_y", start_y),
                 ("size_x", SIZE_X),
                 ("size_y", SIZE_Y),
                 ("cells", cells),
                 ("horizontal_edge", hEdge),
                 ("vertical_edge", vEdge)])
    print(data)
    json.dump(data, write_file, indent=2)


def create_sdf_from_json(jsonFileName=JSON_DEFAULT_NAME, sdfFileName=SDF_DEFAULT_NAME):
    read_file = open(jsonFileName, "r")
    data = json.load(read_file)

    sdfCreator = SdfCreator(data.get("start_x"), data.get("start_y"), data.get("size_x"), data.get("size_y"))
    for cells in data.get("cells"):
        sdfCreator.addBigObstacle(cells[0], cells[1])
    for edges in data.get("horizontal_edge"):
        sdfCreator.addHorizontalBorder(edges[0], edges[1])
    for edges in data.get("vertical_edge"):
        sdfCreator.addVerticalBorder(edges[0], edges[1])
    sdfCreator.writeWorldToFile(sdfFileName)

