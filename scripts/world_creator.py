#!/usr/bin/env python3

"""
This sript creates gui that allow to create json and sdf files.
"""

import argparse

from gui import *
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

    args = vars(parser.parse_args())

    ncell_w, ncell_h = args['size'].split('x')
    cell_w, cell_h = args['cell'].split('x')
    filepath2Load = args['load']
    basenamePrefix = args['name'] 

    cellsSize = Size2D(float(cell_w), float(cell_h))
    cellsAmount = Size2D(int(ncell_w), int(ncell_h))

    app = QApplication(sys.argv)
    window = MainWindow(filepath2Load, basenamePrefix, MapParams(cellsAmount, cellsSize))
    app.exec_()

