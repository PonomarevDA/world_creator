#!/usr/bin/env python2

"""
This script create gazebo sdf world with predefined configuration.
"""

from lxml import etree
import copy
import numpy
from gazebo_sdf import *

def add_obtacles_like_in_regulations():
    add_obstacle(sdf_root, 8, 9)
    add_obstacle(sdf_root, 8, 8)
    add_obstacle(sdf_root, 8, 7)
    add_obstacle(sdf_root, 8, 5)
    add_obstacle(sdf_root, 8, 4)

    add_obstacle(sdf_root, 6, 8)
    add_obstacle(sdf_root, 6, 7)
    add_obstacle(sdf_root, 6, 5)
    add_obstacle(sdf_root, 6, 4)

    add_obstacle(sdf_root, 4, 6)
    add_obstacle(sdf_root, 4, 4)
    add_obstacle(sdf_root, 3, 6)

if __name__=="__main__":
    read_config()
    sdf_root = create_empty_world()
    add_border(sdf_root)
    add_obtacles_like_in_regulations()
    #show_tree(sdf_root)
    write_tree_to_file(sdf_root)

