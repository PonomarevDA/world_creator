import math as m
from copy import deepcopy

import objects
import data_structures as ds

BOX_HEIGHT = float(0.5)
BOX_SPAWN_Z = BOX_HEIGHT / 2

WALL_HEIGHT = float(0.5)
WALL_SPAWN_Z = WALL_HEIGHT / 2
WALL_WIDTH = float(0.05)

DOOR_HEIGHT = float(0.5)
DOOR_SPAWN_Z = WALL_HEIGHT - DOOR_HEIGHT / 2

WINDOW_HEIGHT = float(3.5)
WINDOW_MATERIAL_HEIGHT = float(1.0)
WINDOW_SPAWN_Z = WINDOW_HEIGHT / 2
WINDOW_WIDTH = WALL_WIDTH

SQUARE_HEIGHT = float(0.5)
SQUARE_SPAWN_Z = SQUARE_HEIGHT / 2


ORIENTATIONS_2_YAW_ANGLE = {
    objects.CellQuarter.LEFT_BOT: m.pi / 2,
    objects.CellQuarter.RIGHT_BOT: m.pi,
    objects.CellQuarter.LEFT_TOP: m.pi * 2,
    objects.CellQuarter.RIGHT_TOP: m.pi * 3 / 2,
}


class GazeboObject():
    def __init__(self, base, map_params):
        self.map_params = map_params
        self.base = base

    def _swap_axes(self, pos):
        pos.y = self.map_params.n_cells.y - pos.y

    def _turn_to_physical(self, pos):
        pos.x *= self.map_params.cell_sz.x
        pos.y *= self.map_params.cell_sz.y


class GazeboBox(GazeboObject):
    def __init__(self, base, map_params):
        super().__init__(base, map_params)

        if type(base) is not objects.Box:
            raise Exception('Invalid class passed')

    def get_position_str(self):
        # Maybe better to realize and use Box object method like 'get_pos()' with deep copy
        center = self.base.pos + ds.Point2D(0.5, 0.5)
        self._swap_axes(center)
        self._turn_to_physical(center)

        return '{} {} {} 0 0 0'.format(center.x, center.y, BOX_SPAWN_Z)

    def get_size_str(self):
        return '{} {} {}'.format(self.map_params.cell_sz.x, self.map_params.cell_sz.y, BOX_HEIGHT)


class GazeboWall(GazeboObject):
    def __init__(self, base, map_params):
        super().__init__(base, map_params)

        if type(base) is not objects.Wall:
            raise Exception('Invalid class passed')

    def get_position_str(self):
        center = (self.base.p1 + self.base.p2) / 2
        sub = self.base.p2 - self.base.p1
        wall_angle = m.atan2(sub.y, sub.x)

        self._swap_axes(center)
        self._turn_to_physical(center)

        return '{} {} {} 0 0 {}'.format(center.x, center.y,
                                        WALL_SPAWN_Z, -wall_angle)

    def get_size_str(self):
        sub = self.base.p2 - self.base.p1

        wall_length = m.sqrt((sub.x*self.map_params.cell_sz.y)**2 +
                             (sub.y*self.map_params.cell_sz.y)**2)

        return '{} {} {}'.format(wall_length, WALL_WIDTH, WALL_HEIGHT)


class GazeboDoor(GazeboObject):
    def __init__(self, base, map_params):
        super().__init__(base, map_params)

        if type(base) is not objects.Door:
            raise Exception('Invalid class passed')

    def get_position_str(self):
        center = (self.base.p1 + self.base.p2) / 2
        sub = self.base.p2 - self.base.p1
        door_angle = m.atan2(sub.y, sub.x)

        self._swap_axes(center)
        self._turn_to_physical(center)

        return '{} {} {} 0 0 {}'.format(center.x, center.y,
                                        DOOR_SPAWN_Z, -door_angle)

    def get_size_str(self):
        sub = self.base.p2 - self.base.p1

        door_length = m.sqrt((sub.x*self.map_params.cell_sz.y)**2 +
                             (sub.y*self.map_params.cell_sz.y)**2)

        return '{} {} {}'.format(door_length, WALL_WIDTH, DOOR_HEIGHT)


class GazeboWindow(GazeboObject):
    def __init__(self, base, map_params):
        super().__init__(base, map_params)

        if type(base) is not objects.Window:
            raise Exception('Invalid class passed')

    def get_position_str(self):
        center = (self.base.p1 + self.base.p2) / 2
        sub = self.base.p2 - self.base.p1
        window_angle = m.atan2(sub.y, sub.x)

        self._swap_axes(center)
        self._turn_to_physical(center)

        return '{} {} {} 0 0 {}'.format(center.x, center.y,
                                        WINDOW_SPAWN_Z, -window_angle)

    def get_size_str(self):
        sub = self.base.p2 - self.base.p1

        window_length = m.sqrt((sub.x*self.map_params.cell_sz.y)**2 +
                             (sub.y*self.map_params.cell_sz.y)**2)

        return '{} {} {}'.format(window_length, WINDOW_WIDTH, WINDOW_MATERIAL_HEIGHT)

class GazeboSquare(GazeboObject):
    def __init__(self, base, map_params):
        super().__init__(base, map_params)
        self.pillar_width = map_params.cell_sz / 10
        if type(base) is not objects.Square:
            raise Exception('Invalid class passed')

    def get_position_strs(self):
        results = []
        center = deepcopy(self.base.pos)

        positions = [
            ds.Point2D(.0, .0),
            ds.Point2D(.5, .0),
            ds.Point2D(1., .0),
            ds.Point2D(.0, .5),
            ds.Point2D(1., .5),
            ds.Point2D(.0, 1.),
            ds.Point2D(.5, 1.),
            ds.Point2D(1., 1.)
        ]

        for pos in positions:
            pillar_cntr = center + pos

            self._swap_axes(pillar_cntr)
            self._turn_to_physical(pillar_cntr)

            results += ['{} {} {} 0 0 0'.format(pillar_cntr.x, pillar_cntr.y, SQUARE_SPAWN_Z)]

        return results

    def get_size_str(self):
        return '{} {} {}'.format(self.pillar_width.x, self.pillar_width.y, SQUARE_HEIGHT)


class GazeboSign(GazeboObject):
    def __init__(self, base, map_params):
        super().__init__(base, map_params)

        if type(base) is not objects.Sign:
            raise Exception('Invalid class passed')

    def get_position_str(self):
        pos = deepcopy(self.base.pos)

        # Apply small shift
        if self.base.orient == objects.CellQuarter.RIGHT_TOP:
            pos += ds.Point2D(0.9, 0.1)
        elif self.base.orient == objects.CellQuarter.RIGHT_BOT:
            pos += ds.Point2D(0.9, 0.9)
        elif self.base.orient == objects.CellQuarter.LEFT_BOT:
            pos += ds.Point2D(0.1, 0.9)
        elif self.base.orient == objects.CellQuarter.LEFT_TOP:
            pos += ds.Point2D(0.1, 0.1)

        self._swap_axes(pos)
        self._turn_to_physical(pos)

        yaw_angle = ORIENTATIONS_2_YAW_ANGLE[self.base.orient]

        return "{0} {1} 0 0 0 {2}".format(pos.x, pos.y, yaw_angle)

    def get_type(self):
        return self.base.type


class GazeboTrafficLight(GazeboObject):
    LINE_WIDTH = 0.05 # m

    def __init__(self, base, map_params):
        super().__init__(base, map_params)
        if type(base) is not objects.TrafficLight:
            raise Exception('Invalid class passed')

    def _get_position(self):
        pos = deepcopy(self.base.pos)

        # Apply small shift
        if self.base.orient == objects.CellQuarter.RIGHT_TOP:
            pos += ds.Point2D(0.9, 0.1)
        elif self.base.orient == objects.CellQuarter.RIGHT_BOT:
            pos += ds.Point2D(0.9, 0.9)
        elif self.base.orient == objects.CellQuarter.LEFT_BOT:
            pos += ds.Point2D(0.1, 0.9)
        elif self.base.orient == objects.CellQuarter.LEFT_TOP:
            pos += ds.Point2D(0.1, 0.1)

        return pos

    def get_position_str(self):
        pos = self._get_position()

        self._swap_axes(pos)
        self._turn_to_physical(pos)

        yaw_angle = ORIENTATIONS_2_YAW_ANGLE[self.base.orient]

        return "{0} {1} 0 0 0 {2}".format(pos.x, pos.y, yaw_angle)

    def get_line_position_str(self):
        pos = self._get_position()

        # Shift relative to real position
        if self.base.orient == objects.CellQuarter.RIGHT_TOP:
            pos += ds.Point2D(0, -0.6)
        elif self.base.orient == objects.CellQuarter.RIGHT_BOT:
            pos += ds.Point2D(0.6, 0)
        elif self.base.orient == objects.CellQuarter.LEFT_BOT:
            pos += ds.Point2D(0, 0.6)
        elif self.base.orient == objects.CellQuarter.LEFT_TOP:
            pos += ds.Point2D(-0.6, 0)

        self._swap_axes(pos)
        self._turn_to_physical(pos)

        yaw_angle = ORIENTATIONS_2_YAW_ANGLE[self.base.orient]

        # Rise up just to be visible
        return "{0} {1} 0.001 0 0 {2}".format(pos.x, pos.y, yaw_angle)

    def get_line_size_str(self):
        return "{0} {1}".format(self.map_params.cell_sz.x, self.LINE_WIDTH)

class GazeboCube(GazeboObject):
    def __init__(self, base, map_params):
        super().__init__(base, map_params)
        if type(base) is not objects.Cube:
            raise Exception('Invalid class passed')

    def _get_position(self):
        pos = deepcopy(self.base.pos)

        # Apply small shift
        if self.base.orient == objects.CellQuarter.RIGHT_TOP:
            pos += ds.Point2D(0.75, 0.25)
        elif self.base.orient == objects.CellQuarter.RIGHT_BOT:
            pos += ds.Point2D(0.75, 0.25)
        elif self.base.orient == objects.CellQuarter.LEFT_BOT:
            pos += ds.Point2D(0.25, 0.75)
        elif self.base.orient == objects.CellQuarter.LEFT_TOP:
            pos += ds.Point2D(0.25, 0.25)
        return pos

    def get_position_str(self):
        pos = self._get_position()

        self._swap_axes(pos)
        self._turn_to_physical(pos)

        yaw_angle = ORIENTATIONS_2_YAW_ANGLE[self.base.orient]

        return "{0} {1} 0 0 0 {2}".format(pos.x, pos.y, yaw_angle)

class GazeboQrCube(GazeboObject):
    def __init__(self, base, map_params):
        super().__init__(base, map_params)
        if type(base) is not objects.QrCube:
            raise Exception('Invalid class passed')

    def _get_position(self):
        pos = deepcopy(self.base.pos)
        pos += ds.Point2D(self.map_params.cell_sz.x/2, self.map_params.cell_sz.y/2)
        return pos

    def get_position_str(self):
        pos = self._get_position()
        self._swap_axes(pos)
        self._turn_to_physical(pos)
        return "{0} {1} 0 0 0 0".format(pos.x, pos.y)
