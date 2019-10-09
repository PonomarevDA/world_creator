#!/usr/bin/env python3

"""
The scripts with some tests
"""
import json

def testJsonCreation():
    start_x = 17
    start_y = 17
    size_x = 18
    size_y = 18
    cells = [[8, 9], [8, 8], [8, 7], [8, 5], [8, 4], [6, 8], 
             [6, 7], [6, 5], [6, 4], [4, 6], [4, 4], [3, 6]]
    horizontal_edge = [[2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2],
                       [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0],
                       [0, 9], [1, 9], [2, 9], [3, 9], [4, 9], [5, 9], [6, 9], [7, 9], [8, 9]]
    vertical_edge = [[2, 2], [2, 3], [2, 4], [2, 5],
                     #[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1,6], [1,7], [1, 8], [1,9],
                     #[10, 1], [10, 2], [10, 3], [10, 4], [10, 5], [10,6], [10,7], [10, 8], [10,9]]
                     #[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8],
                     [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8],
                     [9, 0], [9, 1], [9, 2], [9, 3], [9, 4], [9, 5], [9, 6], [9, 7], [9, 8]]

    data =dict([("start_x", start_x),
                ("start_y", start_y),
                ("size_x", size_x),
                ("size_y", size_y),
                ("cells", cells),
                ("horizontal_edge", horizontal_edge),
                ("vertical_edge", vertical_edge) ])

    write_file = open("data_file.json", "w")
    json.dump(data, write_file, indent=2)

