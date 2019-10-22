#!/usr/bin/env python3
from lxml import etree
import copy, numpy

class Point:
    def __init__(self, pos_x, pos_y, pos_z):
        self.x = pos_x
        self.y = pos_y
        self.z = pos_z
    def getString(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z) + " 0 0 0"

#Constants
WALL_WIDTH = float(0.1)
CELL_SIZE = [int(2), int(2)]
HEGHT = float(0.5)


class SdfCreator:
    def __init__(self, start, finish, size):
        """ 
        @brief Constructor that create empty world with defined config 
        """
        self.__setConfig(start, finish, size)
        self.__create_empty_world()


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
        @param point1 - list of map coordinate (x, y) (from 0 to SIZE_X)
        @param point2 - list of map coordinate (x, y) (from 0 to SIZE_Y)
        @note few notes:
        1. wall must be horizontal or vertical (too lazy to work with 
        rotation angles)
        2. param do not take into account offset
        """
        print("wall with pos:", point1, point2)
        center_x = numpy.mean([point1[0], point2[0]]) 
        center_y = numpy.mean([point1[1], point2[1]])
        center_point = Point(center_x, center_y, HEGHT)

        # vertical
        if point1[0] == point2[0]:
            wall_length = abs(point1[1] - point2[1])
            wall_size = Point(WALL_WIDTH, wall_length, HEGHT)
        # horizontal
        elif point1[1] == point2[1]:
            wall_length = abs(point1[0] - point2[0])
            wall_size = Point(wall_length, WALL_WIDTH, HEGHT)
        else:
            return
        self.__spawnBox(center_point, wall_size)


    def addBox(self, cellIndexes):
        """ 
        @brief Spawn big box with size 2x2 on middle of cell
        @param cellIndexes - index of cell (from 0 to CELLS_AMOUNT - 1)
        """
        boxSize = Point(CELL_SIZE[0], CELL_SIZE[1], HEGHT)
        pose_x = cellIndexes[0] * boxSize.x + boxSize.x / 2
        pose_y = cellIndexes[1] * boxSize.y + boxSize.y / 2
        self.__spawnBox(Point(pose_x, pose_y, HEGHT), boxSize)


    def __spawnBox(self, box_position, box_size):
        """ 
        @brief Spawn box with defined size in defined position
        @note You can spawn it in 2 variants:
        1. box: on center of cell in template [odd; odd], 
            for example [3; 1], [3; 3], [3; 5]
        2. wall: on center of cell in template [even; odd] or [odd; even], 
            for example [1; 0], [2; 1], [4; 3]
        @param box_position - position in high level abstraction, in other 
            words, start offset is not taken into account.
        """
        self.box_counter += 1
        box_root = etree.parse("box.world").getroot()
        box_position.x = self.START_X - box_position.x
        box_position.y = - self.START_Y + box_position.y
        self.__setBoxParams(box_root, box_position, box_size)
        self.SDF_ROOT.find("world").insert(0, copy.deepcopy(box_root) )


    def __setBoxParams(self, box_root, box_position, box_size):
        """ 
        @brief Set box desired parameters
        @note To avoid collision problem when objects spawn on borders of each
            other, the collision length will reduce on WALL width size
        """
        box_name = "unit_box_" + str(self.box_counter)

        box_position_text = box_position.getString()

        box_visual_size_text = box_size.getString()

        collision_size = box_size
        if collision_size.x > WALL_WIDTH:
            collision_size.x = collision_size.x - WALL_WIDTH
        if collision_size.y > WALL_WIDTH:
            collision_size.y -= WALL_WIDTH
        box_collision_size_text = collision_size.getString()

        box_root.set("name", box_name)
        box_root.find("pose").text = box_position_text
        link = box_root.find("link")
        link.find("collision").find("geometry").find("box").find("size").text = box_collision_size_text
        link.find("visual").find("geometry").find("box").find("size").text = box_visual_size_text

    def __setConfig(self, start, finish, size):
        """ 
        @brief Set config from inputs
        """
        MIN_MAP_SIZE = 4
        MAX_MAP_SIZE = 40
        DEFAULT_MAP_SIZE = 18
        DEFAULT_POSE = 17

        if ((size[0] >= MIN_MAP_SIZE) and (size[0] <= MAX_MAP_SIZE)):
            self.SIZE_X = size[0]
        else:
            self.SIZE_X = DEFAULT_MAP_SIZE
        if ((size[1] >= MIN_MAP_SIZE) and (size[1] <= MAX_MAP_SIZE)):
            self.SIZE_Y = size[1]
        else:
            self.SIZE_Y = DEFAULT_MAP_SIZE

        if ((start[0] >= 0) and (start[0] <= self.SIZE_X)):
            self.START_X = start[0]
        else:
            self.START_X = DEFAULT_POSE
        if ((start[1] >= 0) and (start[1] <= self.SIZE_X)):
            self.START_Y = start[1]
        else:
            self.START_Y = DEFAULT_POSE

        print("World settings are:", 
              "size = [", self.SIZE_X, self.SIZE_Y, HEGHT, "],",
              "start: [", self.START_X, self.START_Y,  "]")


    def __create_empty_world(self):
        """ 
        @brief Create sdf tree for empty world from file
        """
        self.SDF_ROOT = etree.parse("empty_world.world").getroot()

    # Variables:
    box_counter = 0

