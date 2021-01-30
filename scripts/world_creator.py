#!/usr/bin/env python3

"""
This sript creates gui that allow to create json and sdf files.
"""

import argparse
import sys

from PyQt5.QtWidgets import QApplication
from objects import MapParams
from gui import MainWindow
from data_structures import Size2D

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Map creation tool')
    parser.add_argument('--load',
                        type=str,
                        help='Path to JSON to load',
                        default=None)
    parser.add_argument('--name',
                        type=str,
                        help='Prefix for generated JSON/WORLD files. For \'--name worlds/new\' files \'worlds/new.json\' and \'worlds/new.world\' will be generated',
                        default='new_world')
    parser.add_argument('--size',
                        help='Size of map [measured in cells] (w x h)',
                        default='9x9')
    parser.add_argument('--cell',
                        help='Size of cell in map',
                        default='1x1')
    parser.add_argument('--height',
                        help='Height of wall',
                        default='0.5')
    parser.add_argument('--scene',
                        help='Type of scene. Supported: default, sky',
                        default='default')
    parser.add_argument('--wall_texture',
                        help='Texture of wall. Supported: Orange, White, Grey, Wood, WoodPallet, WoodFloor',
                        default='default')
    parser.add_argument('--ground_texture',
                        help='Texture of wall. Supported: orange, grey',
                        default='default')

    args = vars(parser.parse_args())

    ncell_w, ncell_h = args['size'].split('x')
    cell_w, cell_h = args['cell'].split('x')
    load_filepath = args['load']
    basename_prefix = args['name']
    height = args['height']
    scene = args['scene']
    wall_texture = args['wall_texture']
    ground_texture = args['ground_texture']

    cells_size = Size2D(float(cell_w), float(cell_h))
    cells_amount = Size2D(int(ncell_w), int(ncell_h))

    app = QApplication(sys.argv)
    map_params = MapParams(cells_amount, cells_size, height, scene, wall_texture, ground_texture)
    window = MainWindow(load_filepath, basename_prefix, map_params)
    app.exec_()
