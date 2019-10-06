#!/usr/bin/env python2
from lxml import etree
import copy
import numpy

# Global parameters
OFFSET_X = float()
OFFSET_Y = float()
SIZE_X = float()
SIZE_Y = float()
SIZE_Z = float()
BORDER_WIDTH = float()
MAX_BORDER_LEN = float()

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

def read_config():
    global OFFSET_X, OFFSET_Y, SIZE_X, SIZE_Y, SIZE_Z, BORDER_WIDTH, MAX_BORDER_LEN
    OFFSET_X = float(8)
    OFFSET_Y = float(8)
    SIZE_X = float(18)
    SIZE_Y = float(18)
    SIZE_Z = float(0.5)
    BORDER_WIDTH = float(0.1)
    MAX_BORDER_LEN = float(3)

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
    global OFFSET_X, OFFSET_Y, SIZE_X, SIZE_Y, SIZE_Z, BORDER_WIDTH, MAX_BORDER_LEN

    x_range = numpy.arange(OFFSET_X - SIZE_X/2 + MAX_BORDER_LEN/2, OFFSET_X + SIZE_X/2, MAX_BORDER_LEN)
    y_range = numpy.arange(OFFSET_Y - SIZE_Y/2 + MAX_BORDER_LEN/2, OFFSET_Y + SIZE_Y/2, MAX_BORDER_LEN)
    vertical_border_size = Point(BORDER_WIDTH, MAX_BORDER_LEN, SIZE_Z)
    horizontal_border_size = Point(MAX_BORDER_LEN, BORDER_WIDTH, SIZE_Z)
    right_pos_x = OFFSET_X + SIZE_X/2 + BORDER_WIDTH/2
    left_pos_x = OFFSET_X - SIZE_X/2 - BORDER_WIDTH/2
    top_pos_y = OFFSET_Y + SIZE_Y/2 + BORDER_WIDTH/2
    bottom_pos_y = OFFSET_Y - SIZE_Y/2 - BORDER_WIDTH/2

    for pos_y in y_range:
        add_box(sdf_root, Point(right_pos_x, pos_y, SIZE_Z), vertical_border_size)
        add_box(sdf_root, Point(left_pos_x, pos_y, SIZE_Z), vertical_border_size) 
    for pos_x in x_range:
        add_box(sdf_root, Point(pos_x, top_pos_y, SIZE_Z), horizontal_border_size)
        add_box(sdf_root, Point(pos_x, bottom_pos_y, SIZE_Z), horizontal_border_size)


def add_obstacle(sdf_root, x, y):
    global SIZE_X, SIZE_Z
    box_position = Point((SIZE_X/2 - x) * (2), (SIZE_Y/2 - y) * (2), 0.5)
    add_box(sdf_root, box_position, Point(2, 2, 0.5))

