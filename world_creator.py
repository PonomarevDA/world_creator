#!/usr/bin/env python2

"""
This script create gazebo sdf world with predefined configuration.
"""

from gazebo_sdf import *

def addBigObtaclesLikeInRegulations(sdfCreator):
    cells_with_big_obstacles = [[8, 9], [8, 8], [8, 7], [8, 5], [8, 4], [6, 8], 
                                [6, 7], [6, 5], [6, 4], [4, 6], [4, 4], [3, 6]]
    for cells in cells_with_big_obstacles:
        sdfCreator.addBigObstacle(cells[0], cells[1])

    edge_with_horizontal_borders = [[3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [9, 2]]
    for edges in edge_with_horizontal_borders:
        sdfCreator.addHorizontalBorder(edges[0], edges[1])

    edge_with_vertical_borders = [[2, 3], [2, 4], [2, 5], [2, 6]]
    for edges in edge_with_vertical_borders:
        sdfCreator.addVerticalBorder(edges[0], edges[1])

def addMapBorders(sdfCreator, size_x, size_y):
    cellsAmount_x = size_x/2
    cellsAmount_y = size_y/2

    for pos_y in range(1, cellsAmount_y + 1):
        sdfCreator.addVerticalBorder(cellsAmount_x, pos_y)
        sdfCreator.addVerticalBorder(0, pos_y)
    for pos_x in range(1, cellsAmount_x + 1):
        sdfCreator.addHorizontalBorder(pos_x, 0)
        sdfCreator.addHorizontalBorder(pos_x, cellsAmount_y)

if __name__=="__main__":
    start_x = 17
    start_y = 17
    size_x = 18
    size_y = 18

    sdfCreator = SdfCreator(start_x, start_y, size_x, size_y)
    addMapBorders(sdfCreator, size_x, size_y)
    addBigObtaclesLikeInRegulations(sdfCreator)
    #sdfCreator.showTree()
    sdfCreator.writeWorldToFile("world.world")

