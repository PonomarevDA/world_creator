#!/usr/bin/env python2

"""
This script create gazebo sdf world with predefined configuration.
"""

from lxml import etree
import copy
import numpy
from gazebo_sdf import *

def addBigObtaclesLikeInRegulations(sdfCreator):
    cells_with_big_obstacles = [[8, 9], [8, 8], [8, 7], [8, 5], [8, 4], [6, 8], 
                                [6, 7], [6, 5], [6, 4], [4, 6], [4, 4], [3, 6]]
    for cell_with_obstacle in cells_with_big_obstacles:
        sdfCreator.addBigObstacle(cell_with_obstacle[0], cell_with_obstacle[1])

if __name__=="__main__":
    start_x = 1
    start_y = 1
    size_x = 18
    size_y = 18

    sdfCreator = SdfCreator() 
    sdfCreator.initWithConfig(start_x, start_y, size_x, size_y)
    sdfCreator.addMapBorders()
    addBigObtaclesLikeInRegulations(sdfCreator)
    sdfCreator.addTopBorder(2, 1)
    #sdfCreator.showTree()
    sdfCreator.writeWorldToFile("world.world")

