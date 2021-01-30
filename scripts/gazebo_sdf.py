#!/usr/bin/env python3
from enum import Enum
import logging as log
from lxml import etree
from objects import SignsTypes, ObjectType, MapParams, Object
import gazebo_objects as go

# Files pathes
SAMPLE_BOX_PATH = "models/box.sdf"
SAMPLE_WINDOW_PATH = "models/window.sdf"
SAMPLE_LINE_PATH = "models/line.sdf"
SAMPLE_QR_CUBE_PATH = "models/qr_cube.sdf"

TRAFFIC_LIGHT_PATH = "model://traffic-light"
CUBE_PATH = "model://cube"

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
    window_counter = 0
    sign_counter = 0
    traffic_light_counter = 0
    cube_counter = 0
    qr_cube_counter = 0

    def __init__(self, map_params: MapParams):
        self.map_params = map_params
        self.__create_empty_world()

    def show_tree(self):
        log.debug(etree.tostring(self.SDF_ROOT, pretty_print=True))

    def write_world_to_file(self, fileName):
        with open(fileName, 'wb') as f:
            f.write(etree.tostring(self.SDF_ROOT, pretty_print=True))

    def add_object(self, obj: Object):
        FUNCTIONS_MAPPING = {
            ObjectType.WALL: self.__add_wall,
            ObjectType.DOOR: self.__add_door,
            ObjectType.WINDOW: self.__add_window,
            ObjectType.SIGN: self.__add_sign,
            ObjectType.BOX: self.__add_box,
            ObjectType.SQUARE: self.__add_square,
            ObjectType.TRAFFIC_LIGHT: self.__add_traffic_light,
            ObjectType.CUBE: self.__add_cube,
            ObjectType.QR_CUBE: self.__add_qr_cube,
        }

        if obj.TYPE not in FUNCTIONS_MAPPING:
            log.error('Object type {} is not supported in WORLD generation'.format(obj.TYPE.name))
            return

        FUNCTIONS_MAPPING[obj.TYPE](obj)

    def __add_wall(self, wall):
        gz_object = go.GazeboWall(wall, self.map_params)

        pos_str = gz_object.get_position_str()
        size_str = gz_object.get_size_str()

        self.__spawn_box(pos_str, size_str)

    def __add_door(self, door):
        gz_object = go.GazeboDoor(door, self.map_params)

        pos_str = gz_object.get_position_str()
        size_str = gz_object.get_size_str()

        self.__spawn_box(pos_str, size_str)

    def __add_box(self, box):
        gz_object = go.GazeboBox(box, self.map_params)

        pos_str = gz_object.get_position_str()
        size_str = gz_object.get_size_str()

        self.__spawn_box(pos_str, size_str)

    def __add_square(self, square):
        gz_object = go.GazeboSquare(square, self.map_params)

        size_str = gz_object.get_size_str()
        pos_strs = gz_object.get_position_str()

        for pos_str in pos_strs:
            self.__spawn_box(pos_str, size_str)

    def __spawn_box(self, pos_str, size_str):
        self.box_counter += 1
        counter = self.box_counter
        model_root = etree.parse(SAMPLE_BOX_PATH).getroot()
        model_name = "box"

        model_root.set("name", "{}_{}".format(model_name, counter))
        model_root.find("pose").text = pos_str
        link = model_root.find("link")
        link.find("collision").find("geometry").find("box").find("size").text = size_str
        link.find("visual").find("geometry").find("box").find("size").text = size_str

        allowed_textures = ['Orange', 'White', 'Grey', 'Wood', 'WoodPallet', 'WoodFloor']
        if self.map_params.wall_texture in allowed_textures:
            texture = self.map_params.wall_texture
        else:
            texture = 'Orange'
        link.find("visual").find("material").find("script").find("name").text = 'Gazebo/' + texture
        self.SDF_ROOT.find("world").insert(0, model_root)

    def __add_window(self, model):
        gz_object = go.GazeboWindow(model, self.map_params)

        pos_str = gz_object.get_position_str()
        size_str = gz_object.get_size_str()

        self.__spawn_window(pos_str, size_str)

    def __spawn_window(self, pos_str, size_str):
        self.window_counter += 1
        counter = self.window_counter
        model_root = etree.parse(SAMPLE_WINDOW_PATH).getroot()
        model_name = "window"

        model_root.set("name", "{}_{}".format(model_name, counter))
        model_root.find("pose").text = pos_str

        link = model_root[1]    # link.top
        link.find("collision").find("geometry").find("box").find("size").text = size_str
        link.find("visual").find("geometry").find("box").find("size").text = size_str

        link = model_root[2]    # link.bot
        link.find("collision").find("geometry").find("box").find("size").text = size_str
        link.find("visual").find("geometry").find("box").find("size").text = size_str

        self.SDF_ROOT.find("world").insert(0, model_root)

    def __add_qr_cube(self, model):
        gz_object = go.GazeboQrCube(model, self.map_params)

        pos_str = gz_object.get_position_str()
        size_str = None

        self.__spawn_qr_cube(pos_str, size_str)

    def __spawn_qr_cube(self, pos_str, size_str):
        counter = self.qr_cube_counter
        self.qr_cube_counter += 1
        model_root = etree.parse(SAMPLE_QR_CUBE_PATH).getroot()
        model_name = "qr_cube"

        model_root.set("name", "{}_{}".format(model_name, counter))
        model_root.find("pose").text = pos_str

        link = model_root[1]
        link.find("visual").find("material").find("script").find("name").text = 'QrCode{}'.format(counter)

        self.SDF_ROOT.find("world").insert(0, model_root)

    def __add_sign(self, sign):
        gz_object = go.GazeboSign(sign, self.map_params)

        pos_str = gz_object.get_position_str()
        _type = gz_object.get_type()

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

        self.__spawn_sign(pos_str, SIGN_MODEL_MAP[_type])

    def __spawn_sign(self, pos_str, _model_path):
        ### LEFT/RIGHT_BOT/TOP - in terms of rendered map
        model_path = _model_path.value
        counter = self.sign_counter
        model_name = "sign"
        log.debug("sign with pos: {} / {}".format(pos_str, model_path))

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

        self.sign_counter += 1

    def __add_traffic_light(self, trafficLight):
        go_traf_light = go.GazeboTrafficLight(trafficLight, self.map_params)
        pos_str = go_traf_light.get_position_str()
        self.__spawn_traffic_light(pos_str)

        line_pos_str = go_traf_light.get_line_position_str()
        line_size_str = go_traf_light.get_line_size_str()
        self.__spawn_traffic_light_line(line_pos_str, line_size_str)

    def __spawn_traffic_light(self, pos_str):
        model_path = TRAFFIC_LIGHT_PATH
        counter = self.traffic_light_counter
        model_name = "traffic_light"
        log.debug("traffic light with pos: {}".format(pos_str))

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

        self.traffic_light_counter += 1

    def __spawn_traffic_light_line(self, pos_str, size_str):
        log.debug("traffic light line with pos: {}".format(pos_str))

        model_root = etree.parse(SAMPLE_LINE_PATH).getroot()
        model_root.set("name", "tl_line_{}".format(self.traffic_light_counter))
        model_root.find("pose").text = pos_str
        link = model_root.find("link")
        link.find("collision").find("geometry").find("plane").find("size").text = size_str
        link.find("visual").find("geometry").find("plane").find("size").text = size_str

        self.SDF_ROOT.find("world").insert(0, model_root)

    def __add_cube(self, model):
        gazebo_object = go.GazeboCube(model, self.map_params)
        pos_str = gazebo_object.get_position_str()
        self.__spawn_cube(pos_str)

    def __spawn_cube(self, pos_str):
        model_path = CUBE_PATH
        counter = self.cube_counter
        model_name = "cube"
        log.debug("cube with pos: {}".format(pos_str))

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

        self.cube_counter += 1

    def __create_empty_world(self):
        self.SDF_ROOT = etree.parse(EMPTY_WORLD_PATH).getroot()

        if self.map_params.scene == 'sky':
            speed_elem = etree.Element("speed")
            speed_elem.text = '12'

            clouds_elem = etree.Element("clouds")
            clouds_elem.append(speed_elem)

            model_root = etree.Element("sky")
            model_root.append(clouds_elem)

            self.SDF_ROOT.find("world").find('scene').insert(0, model_root)
        else:
            pass
