#!/usr/bin/env python3
import os
from enum import Enum
import logging as log
import math as m
from data_structures import Point2D, Size2D

APP_VERSION = 1.0

class SignsTypes(Enum):
    STOP = "stop sign"
    ONLY_FORWARD = "only forward sign"
    ONLY_RIGHT = "only right sign"
    ONLY_LEFT = "only left sign"
    FORWARD_OR_RIGHT = "forward or right sign"
    FORWARD_OR_LEFT = "forward or left sign"

class ImagesPaths():
    PATH_TO_IMAGE = 'models'
    STOP = os.path.join(PATH_TO_IMAGE, 'brick-sign/brick.png')
    ONLY_FORWARD = os.path.join(PATH_TO_IMAGE, 'forward-sign/forward.png')
    ONLY_LEFT = os.path.join(PATH_TO_IMAGE, 'left-sign/left.png')
    ONLY_RIGHT = os.path.join(PATH_TO_IMAGE, 'right-sign/right.png')
    FORWARD_OR_LEFT = os.path.join(PATH_TO_IMAGE, 'forward-left-sign/frwd_left.png')
    FORWARD_OR_RIGHT = os.path.join(PATH_TO_IMAGE, 'forward-right-sign/frwd_right.png')

TRAFFIC_LIGHT_IMG_PATH = 'models/traffic-light.png'

def sign_path_to_sign_type(img_path):
    if img_path is ImagesPaths.STOP:
        return SignsTypes.STOP.value
    elif img_path is ImagesPaths.ONLY_FORWARD:
        return SignsTypes.ONLY_FORWARD.value
    elif img_path is ImagesPaths.ONLY_LEFT:
        return SignsTypes.ONLY_LEFT.value
    elif img_path is ImagesPaths.ONLY_RIGHT:
        return SignsTypes.ONLY_RIGHT.value
    elif img_path is ImagesPaths.FORWARD_OR_LEFT:
        return SignsTypes.FORWARD_OR_LEFT.value
    elif img_path is ImagesPaths.FORWARD_OR_RIGHT:
        return SignsTypes.FORWARD_OR_RIGHT.value
    else:
        return " "

def sign_type_to_sign_path(sign_type):
    if sign_type == SignsTypes.STOP.value:
        return ImagesPaths.STOP
    elif sign_type == SignsTypes.ONLY_FORWARD.value:
        return ImagesPaths.ONLY_FORWARD
    elif sign_type == SignsTypes.ONLY_LEFT.value:
        return ImagesPaths.ONLY_LEFT
    elif sign_type == SignsTypes.ONLY_RIGHT.value:
        return ImagesPaths.ONLY_RIGHT
    elif sign_type == SignsTypes.FORWARD_OR_LEFT.value:
        return ImagesPaths.FORWARD_OR_LEFT
    elif sign_type == SignsTypes.FORWARD_OR_RIGHT.value:
        return ImagesPaths.FORWARD_OR_RIGHT
    else:
        return " "

class ObjectType(Enum):
    START = 10,
    WALL = 11,
    BOX = 12,
    SQUARE = 13,
    SIGN = 14,
    TRAFFIC_LIGHT = 15

class CellQuarter(Enum):
    RIGHT_TOP = 0
    RIGHT_BOT = 1
    LEFT_TOP = 2
    LEFT_BOT = 3


class MapParams:
    def __init__(self, n_cells: Size2D, cell_sz: Size2D):
        self.n_cells = n_cells
        self.cell_sz = cell_sz
        self.phys_size = Size2D(self.n_cells.x * self.cell_sz.x, 
                                self.n_cells.y * self.cell_sz.y)
        print("World cells: count={0},size={1}".format(self.n_cells, self.cell_sz))

    def serialize(self):
        data = {
            'cell_cnt': self.n_cells.as_list(),
            'cell_sz': self.cell_sz.as_list()
        }
        
        return data
    
    def __str__(self):
        return 'Map params: count({}) / size({})'.format(self.n_cells, self.cell_sz)
    
    @staticmethod
    def deserialize(data: dict):
        return MapParams(Point2D.from_list(data['cell_cnt']), Point2D.from_list(data['cell_sz']))

        
class Object:
    def render(self, qp):
        pass
    def serialized(self):
        pass
    @staticmethod
    def deserialize(data: dict):
        if data['name'] not in SERIALIZATION_SUPPORT:
            log.error('Object type \'{}\' not found'.format(data['name']))
            return None
        
        return SERIALIZATION_SUPPORT[data['name']].deserialize(data)


class Wall():
    TYPE = ObjectType.WALL

    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
    
    def __str__(self):
        return "[({}) p1 = {}, p2 = {}]".format(type(self), self.p1, self.p2)
    
    def distance_2_point(self, pnt):
        import numpy
        from numpy import arccos, array, dot, pi, cross
        from numpy.linalg import det, norm

        A = numpy.array(self.p1.as_list())
        B = numpy.array(self.p2.as_list())
        P = numpy.array(pnt.as_list())

        if arccos(dot((P - A) / norm(P - A), (B - A) / norm(B - A))) > m.pi / 2:
            return norm(P - A)
        if arccos(dot((P - B) / norm(P - B), (A - B) / norm(A - B))) > m.pi / 2:
            return norm(P - B)
        return norm(cross(A-B, A-P))/norm(B-A)

    def render(self, qp):
        qp.drawWallLine(self.p1, self.p2, color=(0, 0, 0))
        
    def serialized(self):
        for name, _class in SERIALIZATION_SUPPORT.items():
            if type(self) == _class:
                break
        
        data = {
            'name': name,
            'pnts': self.p1.as_list() + self.p2.as_list()
        }
        
        return data

    @staticmethod
    def deserialize(data: dict):
        return Wall(Point2D.from_list(data['pnts'][0:2]), 
                    Point2D.from_list(data['pnts'][2:4]))
    
    
class Sign(Object):
    TYPE = ObjectType.SIGN
    
    def __init__(self, pos, orient, signType):
        self.pos = pos
        self.type = signType
        self.orient = orient

    def __str__(self):
        return "[({}) pose = {}, orient = {}, type = {}]".format(type(self), self.pos, self.orient, self.type)
    
    def render(self, qp):
        qp.drawQuarterImg(self.pos, self.orient, sign_type_to_sign_path(self.type))
    
    def serialized(self):
        for name, _class in SERIALIZATION_SUPPORT.items():
            if type(self) == _class:
                break
        
        data = {
            'name': name,
            'pos': self.pos.as_list(),
            'orient': self.orient.value,
            'type': self.type
        }
        
        return data        
    
    @staticmethod
    def deserialize(data: dict):
        return Sign(Point2D.from_list(data['pos']), 
                    CellQuarter(data['orient']),
                    data['type'])
    
    
class TrafficLight(Object):
    TYPE = ObjectType.TRAFFIC_LIGHT
    
    def __init__(self, pos, orient):
        self.pos = pos
        self.orient = orient

    def __str__(self):
        return "[({}) pose = {}, orient = {}]".format(type(self), self.pos, self.orient)
    
    def render(self, qp):
        qp.drawQuarterImg(self.pos, self.orient, TRAFFIC_LIGHT_IMG_PATH)
    
    def serialized(self):
        for name, _class in SERIALIZATION_SUPPORT.items():
            if type(self) == _class:
                break
        
        data = {
            'name': name,
            'pos': self.pos.as_list(),
            'orient': self.orient.value,
        }
        
        return data        
    
    @staticmethod
    def deserialize(data: dict):
        return TrafficLight(Point2D.from_list(data['pos']), 
                            CellQuarter(data['orient']))
    
    
class Box(Object):
    TYPE = ObjectType.BOX

    def __init__(self, pos: Point2D):
        self.pos = pos
   
    def render(self, qp):
        qp.fillCell(self.pos, color=(150, 150, 150))
        
    def serialized(self):
        for name, _class in SERIALIZATION_SUPPORT.items():
            if type(self) == _class:
                break
        
        data = {
            'name': name,
            'pos': self.pos.as_list()
        }
        
        return data

    @staticmethod
    def deserialize(data: dict):
        return Box(Point2D.from_list(data['pos']))
     
    
class Square(Object):
    TYPE = ObjectType.SQUARE

    def __init__(self, pos: Point2D):
        self.pos = pos
   
    def render(self, qp):
        qp.fillCell(self.pos, color=(30, 250, 30))
        
    def serialized(self):
        for name, _class in SERIALIZATION_SUPPORT.items():
            if type(self) == _class:
                break
        
        data = {
            'name': name,
            'pos': self.pos.as_list()
        }
        
        return data

    @staticmethod
    def deserialize(data: dict):
        return Square(Point2D.from_list(data['pos']))
     
        
SERIALIZATION_SUPPORT = {
    'wall': Wall,
    'sign': Sign,
    'square': Square, 
    'box': Box, 
    'traffic_light': TrafficLight,
}
    
