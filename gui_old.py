#!/usr/bin/env python3
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from json_converter import *

# Some constants
WHITE_CODE = "FFFFFF"
BLUE_CODE = "0000FF"
GREEN_CODE = "00FF00"
RED_CODE = "FF0000"

WINDOW_POSE_X = 100
WINDOW_POSE_Y = 100
WINDOW_SIZE_X = 400
WINDOW_SIZE_Y = 400

CELL_SIZE = 30
WALL_SIZE = 10
MODE_CHOOSE_START_POS = "ChooseStartPos"
MODE_CHOOSE_END_POS = "ChooseEndPos"
MODE_CHOOSE_BORDERS = "ChooseBorders"

JSON_FILE_NAME = "data_file.json"


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("World creator")
        self.__initParams()
        layout = QGridLayout()
        self.__addTableWithButtonsToLayout(layout)
        self.__addSettingsButtons(layout)
        self.__setMode(MODE_CHOOSE_START_POS)

        widget = QWidget()
        widget.setLayout(layout)

        self.setGeometry(WINDOW_POSE_X, WINDOW_POSE_Y, WINDOW_SIZE_X, WINDOW_SIZE_Y)
        self.setCentralWidget(widget)


    def __addTableWithButtonsToLayout(self, layout):
        self.cells = list()
        self.horizontalWall = list()
        self.verticalWall = list()
        self.cellsStatus = [[False] * self.CELLS_AMOUNT_X for i in range(self.CELLS_AMOUNT_Y)]
        self.horizontalWallStatus = [[False] * (self.CELLS_AMOUNT_X) for i in range(self.CELLS_AMOUNT_Y + 1)]
        self.verticalWallStatus = [[False] * (self.CELLS_AMOUNT_X + 1) for i in range(self.CELLS_AMOUNT_Y)]

        for row in range(self.SIZE_Y, -1, -1):
            if (row % 2) == 0:
                heRow = int((self.SIZE_Y - row)/2)  # from 0 to 9
                self.horizontalWall.append(list())
                for col in range(0, self.SIZE_X, 2):
                    heCol = int(col/2) # from 0 to 8
                    self.__addHorizontalWall(heRow, heCol)
                    layout.addWidget(self.horizontalWall[heRow][heCol], row, col + 1, 1, 1)
            else:
                veRow = int((self.SIZE_Y - row)/2) # from 0 to 8
                cellRow = int((self.SIZE_Y - row)/2) # from 0 to 8
                self.verticalWall.append(list())
                self.cells.append(list())
                for col in range(0, self.SIZE_Y, 2):
                    veCol = int(col/2) # from 0 to 9
                    cellCol = int(col/2) # from 0 to 8
                    self.__addVerticalWall(veRow, veCol)
                    self.__addCell(cellRow, cellCol)
                    layout.addWidget(self.verticalWall[veRow][veCol], row, col, 1, 1)
                    layout.addWidget(self.cells[cellRow][cellCol], row, col + 1, 1, 1)
                self.__addVerticalWall(veRow, veCol + 1)
                layout.addWidget(self.verticalWall[veRow][veCol + 1], row, col + 2, 1, 1)


    def __addSettingsButtons(self, layout):
        layout.addWidget(QLabel("To create world: "), 0, self.SIZE_X + 1)

        self.ChooseStartPosButton = QPushButton("1. Choose start pos")
        self.ChooseStartPosButton.pressed.connect(self.__ChooseStartPosCallback)
        layout.addWidget(self.ChooseStartPosButton, 1, self.SIZE_X + 1)

        self.ChooseEndPosButton = QPushButton("2. Choose end pos")
        self.ChooseEndPosButton.pressed.connect(self.__ChooseEndPosCallback)
        layout.addWidget(self.ChooseEndPosButton, 2, self.SIZE_X + 1)

        self.ChooseBordersButton = QPushButton("3. Choose borders")
        self.ChooseBordersButton.pressed.connect(self.__ChooseBordersCallback)
        layout.addWidget(self.ChooseBordersButton, 3, self.SIZE_X + 1)

        self.ChooseSignsButton = QPushButton("4. Choose signs")
        self.ChooseSignsButton.pressed.connect(self.__ChooseSignsCallback)
        self.ChooseSignsButton.setEnabled(False)
        layout.addWidget(self.ChooseSignsButton, 4, self.SIZE_X + 1)

        self.ChooseLightsButton = QPushButton("5. Choose lighs")
        self.ChooseLightsButton.pressed.connect(self.__ChooseLightsCallback)
        self.ChooseLightsButton.setEnabled(False)
        layout.addWidget(self.ChooseLightsButton, 5, self.SIZE_X + 1)

        layout.addWidget(QLabel("Or use this features:"), 6, self.SIZE_X + 1)

        self.LoadJsonButton = QPushButton("Load json")
        self.LoadJsonButton.pressed.connect(self.__LoadJsonCallback)
        layout.addWidget(self.LoadJsonButton, 7, self.SIZE_X + 1)
        self.LoadJsonButton.setEnabled(False)

        layout.addWidget(QLabel("Then press below button:"), 8, self.SIZE_X + 1)

        self.GenerateJsonButton = QPushButton("Generate json")
        self.GenerateJsonButton.pressed.connect(self.__GenerateJsonCallback)
        layout.addWidget(self.GenerateJsonButton, 9, self.SIZE_X + 1)

        self.GenerateSdfButton = QPushButton("Create sdf world from json")
        self.GenerateSdfButton.pressed.connect(self.__GenerateSdfCallback)
        layout.addWidget(self.GenerateSdfButton, 10, self.SIZE_X + 1)

        layout.addWidget(QLabel("Additional features:"), 14, self.SIZE_X + 1)

        self.CreateBordersAroundMapButton = QPushButton("Create borders around map")
        self.CreateBordersAroundMapButton.pressed.connect(self.__CreateBordersAroundMapCallback)
        self.CreateBordersAroundMapButton.setEnabled(False)
        layout.addWidget(self.CreateBordersAroundMapButton, 15, self.SIZE_X + 1)

        layout.addWidget(QLabel("Error window:"), 16, self.SIZE_X + 1)


    def __initParams(self):
        self.SIZE_X = 18
        self.SIZE_Y = 18
        self.CELLS_AMOUNT_X = int(self.SIZE_X / 2)
        self.CELLS_AMOUNT_Y = int(self.SIZE_Y / 2)
        self.MODE = ""
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None


    def __addCell(self, row, col):
        self.cells[row].append(QPushButton(str(col) + "/" + str(row)))
        callbackFunc = lambda b=self.cells, s=self.cellsStatus, r = row, c = col: self.__butCallback(b, s, r, c)
        butMinSizeX = CELL_SIZE
        butMinSizeY = CELL_SIZE
        self.cells[row][col].pressed.connect(callbackFunc)
        self.cells[row][col].setMinimumSize(QSize(butMinSizeX, butMinSizeY))


    def __addVerticalWall(self, row, col):
        self.verticalWall[row].append(QPushButton("v"))
        callbackFunc = lambda b=self.verticalWall, s=self.verticalWallStatus, r=row, c=col: self.__butCallback(b, s, r, c)
        butMinSizeX = WALL_SIZE
        butMinSizeY = CELL_SIZE
        butMaxSizeX = WALL_SIZE
        butMaxSizeY = CELL_SIZE
        self.verticalWall[row][col].pressed.connect(callbackFunc)
        self.verticalWall[row][col].setMinimumSize(QSize(butMinSizeX, butMinSizeY))
        self.verticalWall[row][col].setMaximumSize(QSize(butMaxSizeX, butMaxSizeY))
        self.verticalWall[row][col].setEnabled(True)


    def __addHorizontalWall(self, row, col):
        self.horizontalWall[row].append(QPushButton("h"))
        callbackFunc = lambda b=self.horizontalWall, s=self.horizontalWallStatus, r=row, c=col: self.__butCallback(b, s, r, c)
        butMinSizeX = CELL_SIZE
        butMinSizeY = WALL_SIZE
        butMaxSizeX = CELL_SIZE
        butMaxSizeY = WALL_SIZE
        self.horizontalWall[row][col].pressed.connect(callbackFunc)
        self.horizontalWall[row][col].setMinimumSize(QSize(butMinSizeX, butMinSizeY))
        self.horizontalWall[row][col].setMaximumSize(QSize(butMaxSizeX, butMaxSizeY))


    def __butCallback(self, but, status, row, col):
        if self.MODE == MODE_CHOOSE_BORDERS:
            print(str(row) + " " + str(col) + " " + self.MODE)
            status[row][col] = not status[row][col]
            if status[row][col] == True:
                self.__setButtonCollor(but[row][col], BLUE_CODE)
            else:
                self.__setButtonCollor(but[row][col], WHITE_CODE)
            if (row == self.start_x) and (col == self.start_y):
                start_x = None
                start_y = None
            if (row == self.end_x) and (col == self.end_y):
                end_x = None
                end_y = None
        elif self.MODE == MODE_CHOOSE_START_POS:
            status[row][col] = False
            if (self.start_x != None) and (self.start_y != None):
                self.__setButtonCollor(but[self.start_x][self.start_y], WHITE_CODE)
                status[row][col] = False
            self.__setButtonCollor(but[row][col], RED_CODE)
            self.start_x = row
            self.start_y = col
        elif self.MODE == MODE_CHOOSE_END_POS:
            status[row][col] = False
            if (self.end_x != None) and (self.end_y != None):
                self.__setButtonCollor(but[self.end_x][self.end_y], WHITE_CODE)
                status[row][col] = False
            self.__setButtonCollor(but[row][col], GREEN_CODE)
            self.end_x = row
            self.end_y = col
    

    def __ChooseStartPosCallback(self):
        self.__setMode(MODE_CHOOSE_START_POS)
        print("__ChooseStartPosCallback")


    def __ChooseEndPosCallback(self):
        self.__setMode(MODE_CHOOSE_END_POS)
        print("__ChooseEndPosCallback")


    def __ChooseBordersCallback(self):
        self.__setMode(MODE_CHOOSE_BORDERS)
        print("__ChooseBordersCallback")


    def __ChooseSignsCallback(self):
        print("__ChooseSignsCallback")


    def __ChooseLightsCallback(self):
        print("__ChooseLightsCallback")


    def __LoadJsonCallback(self):
        print("__LoadJsonCallback")


    def __GenerateJsonCallback(self):
        create_json_from_gui(self.start_x, self.start_y, self.SIZE_X, self.SIZE_Y, self.cellsStatus, self.verticalWallStatus, self.horizontalWallStatus)
        print("__GenerateJsonCallback")


    def __GenerateSdfCallback(self):
        create_sdf_from_json()
        print("__GenerateJsonCallback")


    def __CreateBordersAroundMapCallback(self):
        print("__CreateBordersAroundMapCallback")


    def __setMode(self, mode):
        if mode == MODE_CHOOSE_START_POS:
            self.MODE = mode
            self.__setButtonCollor(self.ChooseStartPosButton, RED_CODE)
            self.__disableBordersButtons()
        else:
            self.__setButtonCollor(self.ChooseStartPosButton, WHITE_CODE)

        if mode == MODE_CHOOSE_END_POS:
            self.MODE = mode
            self.__setButtonCollor(self.ChooseEndPosButton, RED_CODE)
            self.__disableBordersButtons()
        else:
            self.__setButtonCollor(self.ChooseEndPosButton, WHITE_CODE)

        if mode == MODE_CHOOSE_BORDERS:
            self.MODE = mode
            self.__setButtonCollor(self.ChooseBordersButton, RED_CODE)
            self.__enableBordersButtons()
        else:
            self.__setButtonCollor(self.ChooseBordersButton, WHITE_CODE)
    

    def __setButtonCollor(self, but, collor=WHITE_CODE):
        but.setStyleSheet("QPushButton {background-color: #" + collor + "}")


    def __createButton(self, butName, callbackFunc):
        but = QPushButton(butName)
        but.pressed.connect(callbackFunc)
        return but


    def __disableBordersButtons(self):
        for r in range(0, len(self.horizontalWall)):
            for c in range(0, len(self.horizontalWall[0])):
                self.horizontalWall[r][c].setEnabled(False)
        for r in range(0, len(self.verticalWall)):
            for c in range(0, len(self.verticalWall[0])):
                self.verticalWall[r][c].setEnabled(False)


    def __enableBordersButtons(self):
        for r in range(0, len(self.horizontalWall)):
            for c in range(0, len(self.horizontalWall[0])):
                self.horizontalWall[r][c].setEnabled(True)
        for r in range(0, len(self.verticalWall)):
            for c in range(0, len(self.verticalWall[0])):
                self.verticalWall[r][c].setEnabled(True)

