#!/usr/bin/env python3
import sys, random
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QGridLayout, \
    QLabel, QDialog, QStatusBar, QMainWindow, QButtonGroup
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QIcon, QImage
from PyQt5.QtCore import Qt, QSize
from enum import Enum
import logging as log
import itertools as it

import converter
from objects import *

log.basicConfig(filename='world_creator.log', level=log.DEBUG)
log.getLogger().addHandler(log.StreamHandler(sys.stdout))

# ************************** Constants and enums *****************************
class Mode(Enum):
    NO_MODE = int(-1)
    BOXES = int(0)
    WALLS = int(1)
    SIGNS = int(2)
    TRAFFIC_LIGHTS = int(3)
    SQUARES = int(4)

class ColorCode(Enum):
    WHITE = str("FFFFFF")
    BLUE = str("0000FF")
    GREEN = str("00FF00")
    RED = str("FF0000")
    
# ***************************** Main window *********************************

class MyPainter(QPainter):
    def __init__(self, base, cell_sz):
        super().__init__(base)
        
        self.cell_sz = cell_sz

    def fillCell(self, cell_pos, color=(255, 0, 0)):
        self.setBrush(QBrush(QColor(*color)))
        self.setPen(Qt.NoPen)
        self.drawRect(cell_pos.x * self.cell_sz.x, cell_pos.y * self.cell_sz.y, 
                      self.cell_sz.x, self.cell_sz.y)
    
    def drawWallLine(self, node_pos1, node_pos2, color=(0, 0, 0)):
        self.setPen(QPen(QColor(*color), 3))
        self.drawLine(node_pos1.x * self.cell_sz.x, node_pos1.y * self.cell_sz.y,
                      node_pos2.x * self.cell_sz.x, node_pos2.y * self.cell_sz.y)
        
    def drawQuarterImg(self, cell, quarter, img_path):
        self.half_cell_sz = self.cell_sz / 2
        
        render_x = cell.x
        render_y = cell.y
        
        if quarter == CellQuarter.RIGHT_TOP or quarter == CellQuarter.RIGHT_BOT:
            render_x += 0.5
        
        if quarter == CellQuarter.RIGHT_BOT or quarter == CellQuarter.LEFT_BOT:
            render_y += 0.5
        
        img = QImage(img_path).scaled(QSize(self.half_cell_sz.x-1, self.half_cell_sz.y-1))
        self.drawImage(render_x * self.cell_sz.x + 1, render_y * self.cell_sz.y + 1, img)
        

class Canvas(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        
    def paintEvent(self, event=None):
        self.cellSz = Size2D(int(self.geometry().width() // self.model.map_params.n_cells.x), 
                             int(self.geometry().height() // self.model.map_params.n_cells.y))
        self.canvasSz = Size2D(self.cellSz.x * self.model.map_params.n_cells.x, 
                               self.cellSz.y * self.model.map_params.n_cells.y)
        
        qp = MyPainter(self, self.cellSz)

        self.drawMap(qp)
    
        for obj_type, objs in self.model.objects.items():
            if type(objs) is list:
                [obj.render(qp) for obj in objs] 
            else:
                objs.render(qp)
                
    def get_map_positions(self, canvas_click, cell_sz):
        return Point2D(canvas_click.x / cell_sz.x, canvas_click.y / cell_sz.y)

    @staticmethod   
    def getCellClicked(map_pos):
        return Point2D(int(map_pos.x), int(map_pos.y))

    @staticmethod
    def getCrossClicked(map_pos):
        # Cross == Node (crossing of lines)
        return Point2D(int(map_pos.x + .5), int(map_pos.y + .5))
    
    @staticmethod
    def getCellQuarter(map_pos):
        cell_pos = Canvas.getCellClicked(map_pos)

        orient = None
        if map_pos.x - cell_pos.x > 0.5:
            if map_pos.y - cell_pos.y > 0.5:
                orient = CellQuarter.RIGHT_BOT
            else:
                orient = CellQuarter.RIGHT_TOP
        else:
            if map_pos.y - cell_pos.y > 0.5:
                orient = CellQuarter.LEFT_BOT
            else:
                orient = CellQuarter.LEFT_TOP
        
        return orient
        
    def get_canvas_pos(self, x, y):
        if x >= self.canvasSz.x:
            x = self.canvasSz.x - 1
        
        if y >= self.canvasSz.y:
            y = self.canvasSz.y - 1
        
        return Point2D(x, y)
        
    def mousePressEvent(self, e):
        canvas_pos = self.get_canvas_pos(e.pos().x(), e.pos().y()) 
        map_pos = self.get_map_positions(canvas_pos, self.cellSz)
        
        if self.model.mode in self.model.modes:
            if e.button() == Qt.LeftButton:
                self.model.modes[self.model.mode].processLeftMousePressing(map_pos)
            elif e.button() == Qt.RightButton:
                self.model.modes[self.model.mode].processRightMousePressing(map_pos)
        else:
            print("Warning: you should choose mode")
            
        self.update()
           
    def drawMap(self, qp):
        thinPen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(thinPen)
        qp.drawRect(0, 0, self.canvasSz.x-1, self.canvasSz.y-1)
        for row in range(1, self.model.map_params.n_cells.y):
            qp.drawLine(0, row*self.cellSz.y, self.canvasSz.x-1, row*self.cellSz.y)
        for col in range(1, self.model.map_params.n_cells.x):
            qp.drawLine(col*self.cellSz.x, 0, col*self.cellSz.x, self.canvasSz.y-1)
    
    
class Model:
    # Class for keeping main processing data
    def __init__(self, map_params, load_filepath):
        self.modes = {}
        
        self.objects = {
            ObjectType.TRAFFIC_LIGHT: [],
            ObjectType.WALL: [],
            ObjectType.SIGN: [],
            ObjectType.SQUARE: [],
            ObjectType.BOX: []
        }
        
        if load_filepath:
            print('Loading data from {}'.format(load_filepath))
            self.map_params = converter.deserialize_from_json(load_filepath, self.objects)
        else:
            self.map_params = map_params
        
        self.mode = Mode.NO_MODE
    
    def add_mode(self, mode, controller):
        self.modes[mode] = controller
    
    def set_mode(self, _set_mode):
        print(_set_mode)
        
        if self.mode in self.modes:
            self.modes[self.mode].on_disable()
        
        self.mode = _set_mode

    
class ModeButton(QPushButton):
    def __init__(self, text: str, mode: Mode, model: Model, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(QSize(200, 25))
        self.setCheckable(True)
        
        self.mode = mode
        self.model = model

        self.clicked[bool].connect(self.clickHandler)

    def clickHandler(self, pressed):
        if pressed:
            self.model.set_mode(self.mode)
        else:
            self.model.set_mode(Mode.NO_MODE)
    
    
class MainWindow(QWidget):
    def __init__(self, load_filepath, save_file_prefix, map_params):
        super().__init__()
        WINDOW_TITLE = 'World creator v.2'
        self.setWindowTitle(WINDOW_TITLE)
        self.show()
        
        self.model = Model(map_params, load_filepath)

        self.json_save_fpath = save_file_prefix + '.json'
        self.world_save_fpath = save_file_prefix + '.world'

        layout = QGridLayout()
        layout.setSpacing(5)
        self.setLayout(layout)
        
        generateButton = QPushButton('Generate JSON/WORLD', self)
        generateButton.setFixedSize(QSize(200, 25))
        generateButton.pressed.connect(self.generateOutputFiles)
        
        self.ctrl_grp = QButtonGroup()
        self.ctrl_grp.setExclusive(True)

        # TODO - maybe must be not "model" but "controller" connected to buttons
        mode_buttons = [
            (ModeButton('1. Create walls', Mode.WALLS, self.model, self), GuiWallsMode(self.model)),
            (ModeButton('2. Create boxes', Mode.BOXES, self.model, self), GuiBoxesMode(self.model)),
            (ModeButton('3. Create signs', Mode.SIGNS, self.model, self), GuiSignsMode(self.model)),
            (ModeButton('4. Create traffic-lights', Mode.TRAFFIC_LIGHTS, self.model, self), GuiTrafficLightsMode(self.model)),
            (ModeButton('5. Create squares', Mode.SQUARES, self.model, self), GuiSquaresMode(self.model)),
        ]        
        
        # Layout fill
        layout.addWidget(QLabel('To create the world:', self), 0, 1)
        for idx, btn in enumerate(mode_buttons):
            layout.addWidget(btn[0], idx + 1, 1)       
            self.ctrl_grp.addButton(btn[0])
            self.model.add_mode(btn[0].mode, btn[1])

        layout.addWidget(QLabel('Then press buttons below:', self), len(mode_buttons)+1, 1)
        layout.addWidget(generateButton, len(mode_buttons)+2, 1)
        
        self.statusBar = QStatusBar()
        self.statusBar.showMessage('Ready')
        self.statusBar.setMaximumHeight(20)
        layout.addWidget(self.statusBar, len(mode_buttons)+3, 0, 1, 2)
        
        self.canvas = Canvas(self.model, self)
        layout.addWidget(self.canvas, 0, 0, len(mode_buttons)+3, 1)

    def paintEvent(self, event=None):
        qp = QPainter(self)
        self.drawPoints(qp)

    def drawPoints(self, qp):
        """ 
        @brief Draw window background with random points cloud
        """
        qp.setPen(Qt.red)
        windowSize = self.size()
        for i in range(1000):
            x = random.randint(1, windowSize.width() - 1)
            y = random.randint(1, windowSize.height() - 1)
            qp.drawPoint(x, y)


    def generateOutputFiles(self):
        converter.serialize_2_json(self.json_save_fpath, self.model.objects, self.model.map_params)
        converter.create_sdf(self.world_save_fpath, self.model.objects, self.model.map_params)
        
        log.info("Files generated!")


# ***************************** BaseGuiMode ********************************
class BaseGuiMode():
    """ @brief Interface for button features """
    def __init__(self, model):
        self.model = model

    # map_pos - means position in cells (float), for ex. center of (1, 1) == map_pos(1.5, 1.5)
    def processRightMousePressing(self, map_pos):
        pass
    
    def processLeftMousePressing(self, map_pos):
        pass

    def on_disable(self):
        pass


class GuiBoxesMode(BaseGuiMode):
    def processLeftMousePressing(self, map_pos):
        map_cell = Canvas.getCellClicked(map_pos)

        self.model.objects[ObjectType.BOX] += [Box(map_cell)]

    def processRightMousePressing(self, map_pos):
        map_cell = Canvas.getCellClicked(map_pos)

        for box in self.model.objects[ObjectType.BOX]:
            if box.pos == map_cell:
                print("Delete object: {}".format(box))
                self.model.objects[ObjectType.BOX].remove(box)


class GuiSquaresMode(BaseGuiMode):
    def processLeftMousePressing(self, map_pos):
        map_cell = Canvas.getCellClicked(map_pos)

        self.model.objects[ObjectType.SQUARE] += [Square(map_cell)]

    def processRightMousePressing(self, map_pos):
        map_cell = Canvas.getCellClicked(map_pos)

        for square in self.model.objects[ObjectType.SQUARE]:
            if square.pos == map_cell:
                print("Delete object: {}".format(square))
                self.model.objects[ObjectType.SQUARE].remove(square)


class GuiWallsMode(BaseGuiMode):
    def __init__(self, model):
        super().__init__(model)
        self._prev_clicked_cross = None

    def processRightMousePressing(self, map_pos):
        self._prev_clicked_cross = None

        WALL_REMOVE_LIMIT = 0.1

        filtered_walls = it.filterfalse(lambda x: x.distance_2_point(map_pos) < WALL_REMOVE_LIMIT, 
                                        [wall for wall in self.model.objects[ObjectType.WALL]])

        self.model.objects[ObjectType.WALL] = list(filtered_walls)

    def processLeftMousePressing(self, map_pos):
        map_cross = Canvas.getCrossClicked(map_pos)
        
        if self._prev_clicked_cross is not None and \
           self._prev_clicked_cross != map_cross:
            self.model.objects[ObjectType.WALL] += [Wall(map_cross, self._prev_clicked_cross)]
            # self._prev_clicked_cross = None
        # else:
        self._prev_clicked_cross = map_cross
        
    def on_disable(self):
        self._prev_clicked_cross = None
      
      
class GuiTrafficLightsMode(BaseGuiMode):
    def processLeftMousePressing(self, map_pos):
        map_cell = Canvas.getCellClicked(map_pos)
        orient = Canvas.getCellQuarter(map_pos)
        
        new_tl = TrafficLight(map_cell, orient)
        self.model.objects[ObjectType.TRAFFIC_LIGHT] += [new_tl]
        print("Add object: {}".format(new_tl))
        
    def processRightMousePressing(self, map_pos):
        map_cell = Canvas.getCellClicked(map_pos)
        orient = Canvas.getCellQuarter(map_pos)

        for tl in self.model.objects[ObjectType.TRAFFIC_LIGHT]:
            if tl.pos == map_cell and tl.orient == orient:
                log.debug("Delete object {}".format(tl))
                self.model.objects[ObjectType.TRAFFIC_LIGHT].remove(tl)
  

class GuiSignsMode(BaseGuiMode):
    def processLeftMousePressing(self, map_pos):
        map_cell = Canvas.getCellClicked(map_pos)
        orient = Canvas.getCellQuarter(map_pos)

        info = list([ ["Stop", ImagesPaths.STOP],
                      ["Forward", ImagesPaths.ONLY_FORWARD],
                      ["Left", ImagesPaths.ONLY_LEFT],
                      ["Right", ImagesPaths.ONLY_RIGHT],
                      ["Forward or left", ImagesPaths.FORWARD_OR_LEFT],
                      ["Forward or right", ImagesPaths.FORWARD_OR_RIGHT],])

        self.signChoiceDialog = SignChoiceDialog(info)
        self.signChoiceDialog.exec_()
        
        select_idx = self.signChoiceDialog.get_result()
        if select_idx >= 0:
            self.addSign(map_cell, orient, info[select_idx][1])

    def processRightMousePressing(self, map_pos):
        map_cell = Canvas.getCellClicked(map_pos)
        orient = Canvas.getCellQuarter(map_pos)

        self.deleteSign(map_cell, orient)

    def addSign(self, pos, orient, signImg):
        self.deleteSign(pos, orient)

        sign_type = sign_path_to_sign_type(signImg)
        
        print("Add object: sign ({2}) with pose {0}/{1}.".format(pos, orient.name, sign_type))
        self.model.objects[ObjectType.SIGN] += [Sign(pos, orient, sign_type)]
    
    def deleteSign(self, pos, orient):
        for sign in self.model.objects[ObjectType.SIGN]:
            if sign.pos == pos and sign.orient == orient:
                print("Delete object: sign ({2}) with pose {0}/{1}".format(pos, orient.name, sign.type))
                self.model.objects[ObjectType.SIGN].remove(sign)


class SignSelectButton(QPushButton):
    def __init__(self, text, idx, parent=None):
        super().__init__(text, parent)
        self.idx = idx
        

class SignChoiceDialog(QDialog):
    def __init__(self, sign_list):
        super().__init__()

        self.result_idx = -1
        self.label = QLabel("Choose the sign:")     
        
        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0)
        
        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        
        for idx, sign_info in enumerate(sign_list):
            btn = SignSelectButton(sign_info[0], idx, self)
            btn.setIcon(QIcon(sign_info[1]))
            btn.setIconSize(QSize(24, 24))
            layout.addWidget(btn, idx+1, 0)
            
            self.btn_grp.addButton(btn)
            self.btn_grp.setId(btn, idx)

        self.btn_grp.buttonClicked.connect(self.on_click)

        self.setLayout(layout)
        self.show()

    def on_click(self, btn):
        self.result_idx = btn.idx
        self.close()

    def get_result(self):
        # -1 - no selection 
        return self.result_idx
