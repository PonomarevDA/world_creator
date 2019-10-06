#!/usr/bin/env python2
from lxml import etree
import copy
import numpy

# Global parameters
START_X = float()
START_Y = float()
SIZE_X = float()
SIZE_Y = float()
SIZE_Z = float()

class Point:
    x = float()
    y = float()
    z = float()
    def __init__(self, pos_x, pos_y, pos_z):
        self.x = pos_x
        self.y = pos_y
        self.z = pos_z
    def getString(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z) + " 0 0 0"

def set_config(start_x, start_y, size_x, size_y):
    global START_X, START_Y, SIZE_X, SIZE_Y, SIZE_Z
    MIN_MAP_SIZE = 4
    MAX_MAP_SIZE = 40
    DEFAULT_MAP_SIZE = 18
    DEFAULT_POSE = 1
    SIZE_X = size_x if ((size_x >= MIN_MAP_SIZE) and (size_x <= MAX_MAP_SIZE)) else DEFAULT_MAP_SIZE
    SIZE_Y = size_y if ((size_y >= MIN_MAP_SIZE) and (size_y <= MAX_MAP_SIZE)) else DEFAULT_MAP_SIZE
    START_X = start_x if ((start_x >= 0) and (start_x <= SIZE_X)) else DEFAULT_POSE
    START_Y = start_y if ((start_y >= 0) and (start_y <= SIZE_Y)) else DEFAULT_POSE
    SIZE_Z = float(0.5)
    print("Start: " + str(START_X) + "/" + str(START_Y) + ", map size: "+ str(SIZE_X) + "/" + str(SIZE_Y))

def show_tree(root):
    print(etree.tostring(root, pretty_print=True))

def write_tree_to_file(sdf_root):
    f = open('world.world', 'w')
    f.write(etree.tostring(sdf_root, pretty_print=True))

def create_empty_world():
    sdf_root = etree.parse("empty_world.world").getroot()
    return sdf_root

def set_box_params(root, box_position, box_size, counter):
    box_name = "unit_box_" + str(counter)
    box_position_text = box_position.getString()
    box_size_text = box_size.getString()

    root.set("name", box_name)
    root.find("pose").text = box_position_text
    link = root.find("link")
    link.find("collision").find("geometry").find("box").find("size").text = box_size_text
    link.find("visual").find("geometry").find("box").find("size").text = box_size_text


def add_box(sdf_root, box_position, box_size):
    add_box.counter += 1
    box_root = etree.parse("box.world").getroot()
    set_box_params(box_root, box_position, box_size, add_box.counter)
    world = sdf_root.find("world")
    sdf_root.find("world").insert(0, copy.deepcopy(box_root) )
    return sdf_root
add_box.counter = 0


def add_border(sdf_root):
    global START_X, START_Y, SIZE_X, SIZE_Y, SIZE_Z
    BORDER_WIDTH = float(0.1)
    MAX_BORDER_LEN = float(1)

    left_border_mid = -START_X
    right_border_mid = SIZE_X - START_X
    top_border_mid = SIZE_Y - START_Y
    bottom_border_mid = -START_Y

    x_range = numpy.arange(left_border_mid + MAX_BORDER_LEN/2, right_border_mid, MAX_BORDER_LEN)
    y_range = numpy.arange(bottom_border_mid + MAX_BORDER_LEN/2, top_border_mid, MAX_BORDER_LEN)
    vertical_border_size = Point(BORDER_WIDTH, MAX_BORDER_LEN, SIZE_Z)
    horizontal_border_size = Point(MAX_BORDER_LEN, BORDER_WIDTH, SIZE_Z)

    left_border_with_width = left_border_mid - BORDER_WIDTH/2
    right_border_with_width = right_border_mid + BORDER_WIDTH/2
    top_border_with_width = top_border_mid + BORDER_WIDTH/2
    bottom_border_with_width = bottom_border_mid - BORDER_WIDTH/2

    for pos_y in y_range:
        add_box(sdf_root, Point(left_border_with_width, pos_y, SIZE_Z), vertical_border_size)
        add_box(sdf_root, Point(right_border_with_width, pos_y, SIZE_Z), vertical_border_size) 
    for pos_x in x_range:
        add_box(sdf_root, Point(pos_x, top_border_with_width, SIZE_Z), horizontal_border_size)
        add_box(sdf_root, Point(pos_x, bottom_border_with_width, SIZE_Z), horizontal_border_size)


def add_obstacle(sdf_root, x, y):
    global SIZE_X, SIZE_Z
    OBSTACLE_X = 2
    OBSTACLE_Y = 2
    OBSTACLE_Z = 0.5
    box_position = Point((SIZE_X/2 - x) * (2), (SIZE_Y/2 - y) * (2), OBSTACLE_Z)
    add_box(sdf_root, box_position, Point(OBSTACLE_X, OBSTACLE_Y, OBSTACLE_Z))

