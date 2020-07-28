#!/usr/bin/env python3
import logging as log
from lxml import etree
import copy
import math as m
from enum import Enum
import converter
from objects import *
import gazebo_objects as go

# Files pathes
SAMPLE_BOX_PATH = "models/box.sdf"
SAMPLE_LINE_PATH = "models/line.sdf"
TRAFFIC_LIGHT_PATH = "model://traffic-light"
EMPTY_WORLD_PATH = "models/empty_world.world"

# Signs materials
class SignsModels(Enum):
    STOP = "model://brick-sign"
    ONLY_FORWARD = "model://forward-sign"
    ONLY_RIGHT = "model://right-sign"
    ONLY_LEFT = "model://left-sign"
    FORWARD_OR_RIGHT = "model://forward-right-sign"
    FORWARD_OR_LEFT = "model://forward-left-sign"


class WorldCreator:
    # Variables:
    box_counter = 0
    sign_counter = 0
    traffic_light_counter = 0

    def __init__(self, map_params: MapParams):
        """
        @brief Constructor that create empty world with defined config
        """
        self.__create_empty_world()

        self.map_params = map_params

    def showTree(self):
        """
        @brief Print on console xml tree of current world
        """
        log.debug(etree.tostring(self.SDF_ROOT, pretty_print=True))

    def writeWorldToFile(self, fileName):
        """
        @brief Write current world to file
        """
        with open(fileName, 'wb') as f:
            f.write(etree.tostring(self.SDF_ROOT, pretty_print=True))

    def addObject(self, obj: Object):
        FUNCTIONS_MAPPING = {
            ObjectType.WALL: self.__addWall,
            ObjectType.SIGN: self.__addSign,
            ObjectType.BOX: self.__addBox,
            ObjectType.SQUARE: self.__addSquare,
            ObjectType.TRAFFIC_LIGHT: self.__addTrafficLight
        }

        if obj.TYPE not in FUNCTIONS_MAPPING:
            log.error('Object type {} is not supported in WORLD generation'.format(obj.TYPE.name))
            return

        FUNCTIONS_MAPPING[obj.TYPE](obj)

    def __addWall(self, wall):
        gz_wall = go.GazeboWall(wall, self.map_params)

        pos_str = gz_wall.get_position_str()
        size_str = gz_wall.get_size_str()

        self.__spawnBox(pos_str, size_str)

    def __addBox(self, box):
        gz_box = go.GazeboBox(box, self.map_params)

        pos_str = gz_box.get_position_str()
        size_str = gz_box.get_size_str()

        self.__spawnBox(pos_str, size_str)

    def __addSquare(self, square):
        gz_square = go.GazeboSquare(square, self.map_params)

        size_str = gz_square.get_size_str()
        pos_strs = gz_square.get_position_strs()

        for pos_str in pos_strs:
            self.__spawnBox(pos_str, size_str)

    def __spawnBox(self, pos_str, size_str):
        self.box_counter += 1
        box_root = etree.parse(SAMPLE_BOX_PATH).getroot()

        box_root.set("name", "box_{}".format(self.box_counter))
        box_root.find("pose").text = pos_str
        link = box_root.find("link")
        link.find("collision").find("geometry").find("box").find("size").text = size_str
        link.find("visual").find("geometry").find("box").find("size").text = size_str

        self.SDF_ROOT.find("world").insert(0, box_root)

    def __addSign(self, sign):
        gz_sign = go.GazeboSign(sign, self.map_params)

        pos_str = gz_sign.get_position_str()
        _type = gz_sign.get_type()

        SIGN_MODEL_MAP = {
            SignsTypes.STOP.value:              SignsModels.STOP,
            SignsTypes.ONLY_FORWARD.value:      SignsModels.ONLY_FORWARD,
            SignsTypes.ONLY_LEFT.value:         SignsModels.ONLY_LEFT,
            SignsTypes.ONLY_RIGHT.value:        SignsModels.ONLY_RIGHT,
            SignsTypes.FORWARD_OR_LEFT.value:   SignsModels.FORWARD_OR_LEFT,
            SignsTypes.FORWARD_OR_RIGHT.value:  SignsModels.FORWARD_OR_RIGHT,
        }

        if _type not in SIGN_MODEL_MAP:
            log.error("Error: sign type \'{}\' is not supported".format(_type))
            return

        self.__spawnSign(pos_str, SIGN_MODEL_MAP[_type])

    def __spawnSign(self, pos_str, model_path):
        ### LEFT/RIGHT_BOT/TOP - in terms of rendered map
        log.debug("sign with pos: {} / {}".format(pos_str, model_path))

        sign_root = etree.Element("include")
        uri_elem = etree.Element("uri")
        uri_elem.text = model_path.value
        name_elem = etree.Element("name")
        name_elem.text = "sign_{}".format(self.sign_counter)
        pose_elem = etree.Element("pose")
        pose_elem.text = pos_str
        sign_root.append(uri_elem)
        sign_root.append(name_elem)
        sign_root.append(pose_elem)

        self.SDF_ROOT.find("world").insert(0, sign_root)
        self.sign_counter += 1

    def __addTrafficLight(self, trafficLight):
        go_traf_light = go.GazeboTrafficLight(trafficLight, self.map_params)
        pos_str = go_traf_light.get_position_str()
        self.__spawnTrafficLight(pos_str)

        line_pos_str = go_traf_light.get_line_position_str()
        line_size_str = go_traf_light.get_line_size_str()
        self.__spawnTrafficLightLine(line_pos_str, line_size_str)

        self.traffic_light_counter += 1

    def __spawnTrafficLight(self, pos_str):
        log.debug("traffic light with pos: {}".format(pos_str))

        model_path = TRAFFIC_LIGHT_PATH
        counter = self.traffic_light_counter
        model_name = "traffic_light"

        model_root = etree.Element("include")
        uri_elem = etree.Element("uri")
        uri_elem.text = model_path
        name_elem = etree.Element("name")
        name_elem.text = "{}_{}".format(model_name, counter)
        pose_elem = etree.Element("pose")
        pose_elem.text = pos_str
        model_root.append(uri_elem)
        model_root.append(name_elem)
        model_root.append(pose_elem)

        self.SDF_ROOT.find("world").insert(0, model_root)

    def __spawnTrafficLightLine(self, pos_str, size_str):
        log.debug("traffic light line with pos: {}".format(pos_str))

        line_root = etree.parse(SAMPLE_LINE_PATH).getroot()

        line_root.set("name", "tl_line_{}".format(self.traffic_light_counter))
        line_root.find("pose").text = pos_str
        link = line_root.find("link")
        link.find("collision").find("geometry").find("plane").find("size").text = size_str
        link.find("visual").find("geometry").find("plane").find("size").text = size_str

        self.SDF_ROOT.find("world").insert(0, line_root)

    def __create_empty_world(self):
        """
        @brief Create sdf tree for empty world from file
        """
        self.SDF_ROOT = etree.parse(EMPTY_WORLD_PATH).getroot()

