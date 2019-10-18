#!/usr/bin/env python3
from lxml import etree
import copy
import numpy

class Point:
    def __init__(self, pos_x, pos_y, pos_z):
        self.x = pos_x
        self.y = pos_y
        self.z = pos_z
    def getString(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z) + " 0 0 0"

#Constants
WALL_WIDTH = float(0.1)
MAX_WALL_LEN = float(2)
CELL_SIZE_X = int(2)
CELL_SIZE_Y = int(2)
SIZE_Z = float(0.5)
HORIZONTAL_WALL_SIZE = Point(MAX_WALL_LEN, WALL_WIDTH, SIZE_Z)
VERTICAL_WALL_SIZE = Point(WALL_WIDTH, MAX_WALL_LEN, SIZE_Z)


class SdfCreator:
    def __init__(self, start, finish, size):
        """ 
        @brief Constructor that create empty world with defined config 
        """
        self.__setConfig(start[0], start[1], size[0], size[1])
        self.__create_empty_world()
        self.CELLS_X_AMOUNT = int(self.SIZE_X / CELL_SIZE_X)
        self.CELLS_Y_AMOUNT = int(self.SIZE_Y / CELL_SIZE_Y)


    def showTree(self):
        """ 
        @brief Print on console xml tree of current world 
        """
        print(etree.tostring(self.SDF_ROOT, pretty_print=True))


    def writeWorldToFile(self, fileName):
        """ 
        @brief Write current world to file
        """
        f = open(fileName, 'wb')
        f.write(etree.tostring(self.SDF_ROOT, pretty_print=True))


    def addWall(self, point1, point2):
        """ 
        @brief Spawn wall (only vertical or horizontal)
        @param point1 - map coordinate array (x, y) without offset (from 0 to SIZE_X)
        @param point2 - map coordinate array (x, y) without offset (from 0 to SIZE_Y)
        """
        print("wall with pos: " + str(point1) + str(point2))
        point1_x =  point1[0]
        point1_y =  point1[1]
        point2_x =  point2[0]
        point2_y =  point2[1]
        # vertical
        if point1_x == point2_x:
            center_x = point1_x
            center_y = (point1_y + point2_y) / 2
            wall_length = abs(point1_y - point2_y)
            wall_size = Point(WALL_WIDTH, wall_length, SIZE_Z)
        # horizontal
        elif point1_y == point2_y:
            center_x = (point1_x + point2_x) / 2
            center_y = point1_y
            wall_length = abs(point1_x - point2_x)
            wall_size = Point(wall_length, WALL_WIDTH, SIZE_Z)
        else:
            return
        self.__spawnBox(Point(center_x, center_y, SIZE_Z), wall_size)


    def addBox(self, cell_x, cell_y):
        """ 
        @brief Spawn big box with size 2x2 on middle of cell
        @param cell_x - x number of cell (from 0 to CELLS_X_AMOUNT - 1)
        @param cell_y - y index of cell (from 0 to CELLS_Y_AMOUNT - 1)
        """
        boxSize = Point(CELL_SIZE_X, CELL_SIZE_Y, SIZE_Z)
        pose_x = cell_x * boxSize.x + boxSize.x / 2
        pose_y = cell_y * boxSize.y + boxSize.y / 2
        self.__spawnBox(Point(pose_x, pose_y, SIZE_Z), boxSize)


    def __spawnBox(self, box_position, box_size):
        """ 
        @brief Spawn box with defined size in defined position
        @note You can spawn it in 2 variants:
        1. box: on center of cell in template [odd; odd], for example [3; 1], [3; 3], [3; 5]
        2. wall: on center of cell in template [even; odd] or [odd; even], for example [1; 0], [2; 1], [4; 3]
        @param box_position - position in high level abstraction, in other words, start offset was taken into account.
        """
        self.box_counter += 1
        box_root = etree.parse("box.world").getroot()
        box_position.x = -box_position.x + self.START_X
        box_position.y = -box_position.y + self.START_Y
        self.__setBoxParams(box_root, box_position, box_size)
        self.SDF_ROOT.find("world").insert(0, copy.deepcopy(box_root) )


    def __setBoxParams(self, box_root, box_position, box_size):
        """ 
        @brief Set box desired parameters
        """
        box_name = "unit_box_" + str(self.box_counter)
        box_position_text = box_position.getString()
        box_size_text = box_size.getString()

        box_root.set("name", box_name)
        box_root.find("pose").text = box_position_text
        link = box_root.find("link")
        link.find("collision").find("geometry").find("box").find("size").text = box_size_text
        link.find("visual").find("geometry").find("box").find("size").text = box_size_text

    def __setConfig(self, start_x, start_y, size_x, size_y):
        """ 
        @brief Set config from inputs
        """
        MIN_MAP_SIZE = 4
        MAX_MAP_SIZE = 40
        DEFAULT_MAP_SIZE = 18
        DEFAULT_POSE = 17
        self.SIZE_X = size_x if ((size_x >= MIN_MAP_SIZE) and (size_x <= MAX_MAP_SIZE)) else DEFAULT_MAP_SIZE
        self.SIZE_Y = size_y if ((size_y >= MIN_MAP_SIZE) and (size_y <= MAX_MAP_SIZE)) else DEFAULT_MAP_SIZE
        self.START_X = (start_x if ((start_x >= 0) and (start_x <= self.SIZE_X)) else DEFAULT_POSE)
        self.START_Y = (start_y if ((start_y >= 0) and (start_y <= self.SIZE_Y)) else DEFAULT_POSE)
        SIZE_Z = float(0.5)
        print("World settings are: ", self.SIZE_X, self.SIZE_Y, SIZE_Z, self.START_X, self.START_Y)


    def __create_empty_world(self):
        """ 
        @brief Create sdf tree for empty world from file
        """
        self.SDF_ROOT = etree.parse("empty_world.world").getroot()

    # Variables:
    box_counter = 0

