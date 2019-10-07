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


    def addMapBorders(self):
        """ 
        @brief Spawn borders of world edges
        """
        BORDER_WIDTH = float(0.1)
        MAX_BORDER_LEN = float(1)

        left_border_mid = 0
        right_border_mid = self.SIZE_X
        top_border_mid = self.SIZE_Y
        bottom_border_mid = 0

        x_range = numpy.arange(left_border_mid + MAX_BORDER_LEN/2, right_border_mid, MAX_BORDER_LEN)
        y_range = numpy.arange(bottom_border_mid + MAX_BORDER_LEN/2, top_border_mid, MAX_BORDER_LEN)

        left_border_with_width = left_border_mid - BORDER_WIDTH/2
        right_border_with_width = right_border_mid + BORDER_WIDTH/2
        top_border_with_width = top_border_mid + BORDER_WIDTH/2
        bottom_border_with_width = bottom_border_mid - BORDER_WIDTH/2

        for pos_y in y_range:
            self.__addVerticalBorder(left_border_with_width, pos_y)
            self.__addVerticalBorder(right_border_with_width, pos_y)
        for pos_x in x_range:
            self.__addHorizontalBorder(pos_x, top_border_with_width)
            self.__addHorizontalBorder(pos_x, bottom_border_with_width)


    def addTopBorder(self, cell_x, cell_y):
        """ 
        @brief Spawn border of cell
        @param cell_x - x number of cell (from 1 to max)
        @param cell_y - y index of cell (from 1 to max)
        """
        CELL_SIZE_X = 2
        CELL_SIZE_Y = 2
        pos_x_1 = self.SIZE_X - (cell_x * CELL_SIZE_X - 3 * CELL_SIZE_X / 4)
        pos_x_2 = self.SIZE_X - (cell_x * CELL_SIZE_X - 1 * CELL_SIZE_X / 4)
        pos_y = self.SIZE_Y - cell_y * CELL_SIZE_Y
        self.__addHorizontalBorder(pos_x_1, pos_y)
        self.__addHorizontalBorder(pos_x_2, pos_y)


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


    def __addVerticalBorder(self, pos_x, pos_y):
        """ 
        @brief Spawn vertical border on edge of cell
        """
        BORDER_WIDTH = float(0.1)
        MAX_BORDER_LEN = float(1)
        vertical_border_size = Point(BORDER_WIDTH, MAX_BORDER_LEN, self.SIZE_Z)
        self.__spawnBox(Point(pos_x, pos_y, self.SIZE_Z), vertical_border_size)


    def __addHorizontalBorder(self, pos_x, pos_y):
        """ 
        @brief Spawn horisontal border on edge of cell
        """
        BORDER_WIDTH = float(0.1)
        MAX_BORDER_LEN = float(1)
        horizontal_border_size = Point(MAX_BORDER_LEN, BORDER_WIDTH, self.SIZE_Z)
        self.__spawnBox(Point(pos_x, pos_y, self.SIZE_Z), horizontal_border_size)


    sdf_root = etree.Element("root")
    box_counter = 0
    START_X = float(0)
    START_Y = float(0)
    SIZE_X = float(0)
    SIZE_Y = float(0)
    SIZE_Z = float(0)

