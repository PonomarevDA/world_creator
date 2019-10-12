#!/usr/bin/env python3

"""
This script create gazebo sdf world with predefined configuration.
"""

from gazebo_sdf import *
import json
from tests import *

def createWorldFromJson(jsonFileName="data_file.json", sdfFileName="world.world"):
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

if __name__=="__main__":
    #testJsonCreation()
    createWorldFromJson()

