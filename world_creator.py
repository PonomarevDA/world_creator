#!/usr/bin/env python2

"""
This script create gazebo sdf world with predefined configuration.
"""

from lxml import etree
import copy
import numpy
from gazebo_sdf import *

def add_big_obtacles_like_in_regulations():
    cells_with_big_obstacles = [[8, 9], [8, 8], [8, 7], [8, 5], [8, 4], [6, 8], 
                                [6, 7], [6, 5], [6, 4], [4, 6], [4, 4], [3, 6]]
    for cell_with_obstacle in cells_with_big_obstacles:
        add_big_obstacle(sdf_root, cell_with_obstacle[0], cell_with_obstacle[1])

if __name__=="__main__":
    start_x = 1
    start_y = 1
    size_x = 18
    size_y = 18
    set_config(start_x, start_y, size_x, size_y)
    sdf_root = create_empty_world()
    add_map_borders(sdf_root)
    add_big_obtacles_like_in_regulations()
    #show_tree(sdf_root)
    write_tree_to_file(sdf_root)

