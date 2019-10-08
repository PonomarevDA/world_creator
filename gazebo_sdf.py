#!/usr/bin/env python2
from lxml import etree
import copy
import numpy

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


class SdfCreator:
    def initWithConfig(self, start_x, start_y, size_x, size_y):
        """ 
        @brief Parse world config and create empty world 
        """
        self.__setConfig(start_x, start_y, size_x, size_y)
        self.__create_empty_world()


    def showTree(self):
        """ 
        @brief Print on console xml tree of current world 
        """
        print(etree.tostring(self.sdf_root, pretty_print=True))


    def writeWorldToFile(self, fileName):
        """ 
        @brief Write current world to file
        """
        f = open(fileName, 'w')
        f.write(etree.tostring(self.sdf_root, pretty_print=True))


    def addVerticalBorder(self, edge_x, edge_y):
        """ 
        @brief Spawn vertical border on edge of cell
        @param edge_x - from 0 to size_x/2 
        @param edge_y - from 1 to size_y/2 
        """
        pos_x = self.SIZE_X - edge_x * self.CELL_SIZE_X
        pos_y = self.SIZE_Y - edge_y * self.CELL_SIZE_Y + self.CELL_SIZE_Y/2
        vertical_border_size = Point(self.BORDER_WIDTH, self.MAX_BORDER_LEN, self.SIZE_Z)
        self.__spawnBox(Point(pos_x, pos_y, self.SIZE_Z), vertical_border_size)


    def addHorizontalBorder(self, edge_x, edge_y):
        """ 
        @brief Spawn horisontal border on edge of cell
        @param edge_x - from 1 to size_x/2 
        @param edge_y - from 0 to size_y/2 
        """
        pos_x = self.SIZE_X - edge_x * self.CELL_SIZE_X + self.CELL_SIZE_X/2
        pos_y = self.SIZE_Y - edge_y * self.CELL_SIZE_Y
        horizontal_border_size = Point(self.MAX_BORDER_LEN, self.BORDER_WIDTH, self.SIZE_Z)
        self.__spawnBox(Point(pos_x, pos_y, self.SIZE_Z), horizontal_border_size)


    def addBigObstacle(self, cell_x, cell_y):
        """ 
        @brief Spawn big obstacle with size 2x2 on middle of cell
        @param cell_x - x number of cell (from 1 to max)
        @param cell_y - y index of cell (from 1 to max)
        """
        OBSTACLE_X = 2
        OBSTACLE_Y = 2
        OBSTACLE_Z = 0.5
        OFFSET_X = OBSTACLE_X / 2
        OFFSET_Y = OBSTACLE_Y / 2
        pose_x = self.SIZE_X - cell_x * OBSTACLE_X + OFFSET_X
        pose_y = self.SIZE_Y - cell_y * OBSTACLE_Y + OFFSET_Y
        self.__spawnBox(Point(pose_x, pose_y, OBSTACLE_Z), Point(OBSTACLE_X, OBSTACLE_Y, OBSTACLE_Z))


    def __setConfig(self, start_x, start_y, size_x, size_y):
        """ 
        @brief Set config from inputs
        """
        MIN_MAP_SIZE = 4
        MAX_MAP_SIZE = 40
        DEFAULT_MAP_SIZE = 18
        DEFAULT_POSE = 1
        self.SIZE_X = size_x if ((size_x >= MIN_MAP_SIZE) and (size_x <= MAX_MAP_SIZE)) else DEFAULT_MAP_SIZE
        self.SIZE_Y = size_y if ((size_y >= MIN_MAP_SIZE) and (size_y <= MAX_MAP_SIZE)) else DEFAULT_MAP_SIZE
        self.START_X = start_x if ((start_x >= 0) and (start_x <= self.SIZE_X)) else DEFAULT_POSE
        self.START_Y = start_y if ((start_y >= 0) and (start_y <= self.SIZE_Y)) else DEFAULT_POSE
        self.SIZE_Z = float(0.5)
        print("World settings are: ", self.SIZE_X, self.SIZE_Y, self.SIZE_Z, self.START_X, self.START_Y)


    def __create_empty_world(self):
        """ 
        @brief Create sdf tree for empty world from file
        """
        self.sdf_root = etree.parse("empty_world.world").getroot()


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


    def __spawnBox(self, box_position, box_size):
        """ 
        @brief Spawn box with defined size in defined position
        @note You can spawn it in 2 variants:
        1. obstacle: on center of cell in template [odd; odd], for example [3; 1], [3; 3], [3; 5]
        2. border: on center of cell in template [even; odd] or [odd; even], for example [1; 0], [2; 1], [4; 3]
        @param box_position - position in high level abstraction, in other words, start offset was taken into account.
        """
        self.box_counter += 1
        box_root = etree.parse("box.world").getroot()
        box_position.x += self.START_X - self.SIZE_X
        box_position.y += self.START_Y - self.SIZE_Y
        self.__setBoxParams(box_root, box_position, box_size)
        self.sdf_root.find("world").insert(0, copy.deepcopy(box_root) )


    sdf_root = etree.Element("root")
    box_counter = 0
    START_X = float(0)
    START_Y = float(0)
    SIZE_X = float(0)
    SIZE_Y = float(0)
    SIZE_Z = float(0)

    BORDER_WIDTH = float(0.1)
    MAX_BORDER_LEN = float(2)
    CELL_SIZE_X = 2
    CELL_SIZE_Y = 2

