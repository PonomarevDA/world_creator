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


def spawn_box(sdf_root, box_position, box_size):
    """ 
    @brief Spawn box with defined size in defined position
    @note You can spawn it in 2 variants:
    1. obstacle: on center of cell in template [odd; odd], for example [3; 1], [3; 3], [3; 5]
    2. border: on center of cell in template [even; odd] or [odd; even], for example [1; 0], [2; 1], [4; 3]
    @param box_position - position in high level abstraction, in other words, start offset was taken into account.
    """
    spawn_box.counter += 1
    box_root = etree.parse("box.world").getroot()
    box_position.x -= START_X
    box_position.y -= START_Y
    set_box_params(box_root, box_position, box_size, spawn_box.counter)
    sdf_root.find("world").insert(0, copy.deepcopy(box_root) )
    return sdf_root
spawn_box.counter = 0


def add_vertical_border(sdf_root, pos_x, pos_y):
    """ 
    @brief Spawn vertical border on edge of cell
    """
    global SIZE_Z
    BORDER_WIDTH = float(0.1)
    MAX_BORDER_LEN = float(1)
    vertical_border_size = Point(BORDER_WIDTH, MAX_BORDER_LEN, SIZE_Z)
    spawn_box(sdf_root, Point(pos_x, pos_y, SIZE_Z), vertical_border_size)


def add_horizontal_border(sdf_root, pos_x, pos_y):
    """ 
    @brief Spawn horisontal border on edge of cell
    """
    global SIZE_Z
    BORDER_WIDTH = float(0.1)
    MAX_BORDER_LEN = float(1)
    horizontal_border_size = Point(MAX_BORDER_LEN, BORDER_WIDTH, SIZE_Z)
    spawn_box(sdf_root, Point(pos_x, pos_y, SIZE_Z), horizontal_border_size)


def add_map_borders(sdf_root):
    """ 
    @brief Spawn borders of edges of world 
    """
    global SIZE_X, SIZE_Y
    BORDER_WIDTH = float(0.1)
    MAX_BORDER_LEN = float(1)

    left_border_mid = 0
    right_border_mid = SIZE_X
    top_border_mid = SIZE_Y
    bottom_border_mid = 0

    x_range = numpy.arange(left_border_mid + MAX_BORDER_LEN/2, right_border_mid, MAX_BORDER_LEN)
    y_range = numpy.arange(bottom_border_mid + MAX_BORDER_LEN/2, top_border_mid, MAX_BORDER_LEN)

    left_border_with_width = left_border_mid - BORDER_WIDTH/2
    right_border_with_width = right_border_mid + BORDER_WIDTH/2
    top_border_with_width = top_border_mid + BORDER_WIDTH/2
    bottom_border_with_width = bottom_border_mid - BORDER_WIDTH/2

    for pos_y in y_range:
        add_vertical_border(sdf_root, left_border_with_width, pos_y)
        add_vertical_border(sdf_root, right_border_with_width, pos_y)
    for pos_x in x_range:
        add_horizontal_border(sdf_root, pos_x, top_border_with_width)
        add_horizontal_border(sdf_root, pos_x, bottom_border_with_width)

def add_top_border(sdf_root, cell_x, cell_y):
    """ 
    @brief Spawn border of cell
    @param cell_x - x number of cell (from 1 to max)
    @param cell_y - y index of cell (from 1 to max)
    """
    CELL_SIZE_X = 2
    CELL_SIZE_Y = 2
    pos_x_1 = SIZE_X - (cell_x * CELL_SIZE_X - 3 * CELL_SIZE_X / 4)
    pos_x_2 = SIZE_X - (cell_x * CELL_SIZE_X - 1 * CELL_SIZE_X / 4)
    pos_y = SIZE_Y - cell_y * CELL_SIZE_Y
    add_horizontal_border(sdf_root, pos_x_1, pos_y)
    add_horizontal_border(sdf_root, pos_x_2, pos_y)

def add_big_obstacle(sdf_root, cell_x, cell_y):
    """ 
    @brief Spawn big obstacle with size 2x2 on middle of cell
    @param cell_x - x number of cell (from 1 to max)
    @param cell_y - y index of cell (from 1 to max)
    """
    global SIZE_X, SIZE_Z
    OBSTACLE_X = 2
    OBSTACLE_Y = 2
    OBSTACLE_Z = 0.5
    OFFSET_X = OBSTACLE_X / 2
    OFFSET_Y = OBSTACLE_Y / 2
    pose_x = SIZE_X - cell_x * OBSTACLE_X + OFFSET_X
    pose_y = SIZE_Y - cell_y * OBSTACLE_Y + OFFSET_Y
    spawn_box(sdf_root, Point(pose_x, pose_y, OBSTACLE_Z), Point(OBSTACLE_X, OBSTACLE_Y, OBSTACLE_Z))

