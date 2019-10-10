#!/usr/bin/env python2
#import json
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("World creator")
        self.__initParams()
        layout = QGridLayout()
        self.__addTableWithButtonsToLayout(layout)
        self.__addOtherButtons(layout)
        self.__setMode("ChooseStartPos")

        widget = QWidget()
        widget.setLayout(layout)

        window_pose_x = 100
        window_pose_y = 100
        window_size_x = 400
        window_size_y = 400
        self.setGeometry(window_pose_x, window_pose_y, window_size_x, window_size_y)
        self.setCentralWidget(widget)


    def __addTableWithButtonsToLayout(self, layout):
        self.cells = list()
        self.horizontalEdge = list()
        self.verticalEdge = list()
        self.cellsStatus = [[False] * self.CELLS_AMOUNT_X] * (self.CELLS_AMOUNT_Y + 1)
        self.horizontalEdgeStatus = [[False] * self.CELLS_AMOUNT_X] * (self.CELLS_AMOUNT_Y + 1)
        self.verticalEdgeStatus = [[False] * (self.CELLS_AMOUNT_X + 1)] * self.CELLS_AMOUNT_Y
        for row in range(self.SIZE_Y,  -1, -1):
            if (row % 2) == 0:
                heRow = int((self.SIZE_Y - row)/2)  # from 0 to 9
                self.horizontalEdge.append(list())
                for col in range(0, self.SIZE_X, 2):
                    heCol = int(col/2) # from 0 to 8
                    self.__addHorizontalEdge(heRow, heCol)
                    layout.addWidget(self.horizontalEdge[heRow][heCol], row, col + 1, 1, 1)
            else:
                veRow = int((self.SIZE_Y - row)/2) # from 0 to 8
                cellRow = int((self.SIZE_Y - row)/2) # from 0 to 8
                self.verticalEdge.append(list())
                self.cells.append(list())
                for col in range(0, self.SIZE_Y, 2):
                    veCol = int(col/2) # from 0 to 9
                    cellCol = int(col/2) # from 0 to 8
                    self.__addVerticalEdge(veRow, veCol)
                    self.__addCell(cellRow, cellCol)
                    layout.addWidget(self.verticalEdge[veRow][veCol], row, col, 1, 1)
                    layout.addWidget(self.cells[cellRow][cellCol], row, col + 1, 1, 1)
                self.__addVerticalEdge(veRow, veCol + 1)
                layout.addWidget(self.verticalEdge[veRow][veCol + 1], row, col + 2, 1, 1)


    def __addOtherButtons(self, layout):
        layout.addWidget(QLabel("To create world: "), 0, self.SIZE_X + 1)

        self.ChooseStartPosButton = QPushButton("1. Choose start pos")
        self.ChooseStartPosButton.pressed.connect(lambda: self.__ChooseStartPosCallback())
        layout.addWidget(self.ChooseStartPosButton, 1, self.SIZE_X + 1)

        self.ChooseEndPosButton = QPushButton("2. Choose end pos")
        self.ChooseEndPosButton.pressed.connect(lambda: self.__ChooseEndPosCallback())
        layout.addWidget(self.ChooseEndPosButton, 2, self.SIZE_X + 1)

        self.ChooseBordersButton = QPushButton("3. Choose borders")
        self.ChooseBordersButton.pressed.connect(lambda: self.__ChooseBordersCallback())
        layout.addWidget(self.ChooseBordersButton, 3, self.SIZE_X + 1)

        layout.addWidget(QLabel("Then press below button:"), 4, self.SIZE_X + 1)

        self.GenerateJsonButton = QPushButton("Generate json")
        self.GenerateJsonButton.pressed.connect(lambda: self.__GenerateJsonCallback())
        layout.addWidget(self.GenerateJsonButton, 5, self.SIZE_X + 1)

        layout.addWidget(QLabel("Additional features:"), 14, self.SIZE_X + 1)

        self.CreateBordersAroundMapButton = QPushButton("Create borders around map")
        self.CreateBordersAroundMapButton.pressed.connect(lambda: self.__CreateBordersAroundMapCallback())
        layout.addWidget(self.CreateBordersAroundMapButton, 15, self.SIZE_X + 1)

        layout.addWidget(QLabel("Error window:"), 16, self.SIZE_X + 1)


    def __initParams(self):
        self.SIZE_X = 18
        self.SIZE_Y = 18
        self.CELLS_AMOUNT_X = int(self.SIZE_X / 2)
        self.CELLS_AMOUNT_Y = int(self.SIZE_Y / 2)
        self.CELL_SIZE = 30
        self.EDGE_SIZE = 10
        self.MODE = ""


    def __addCell(self, row, col):
        self.cells[row].append(QPushButton(str(col) + "/" + str(row)))
        callbackFunc = lambda b=self.cells, s=self.cellsStatus, r = row, c = col: self.__butCallback(b, s, r, c)
        butMinSizeX = self.CELL_SIZE
        butMinSizeY = self.CELL_SIZE
        self.cells[row][col].pressed.connect(callbackFunc)
        self.cells[row][col].setMinimumSize(QSize(butMinSizeX, butMinSizeY))


    def __addVerticalEdge(self, row, col):
        self.verticalEdge[row].append(QPushButton("v"))
        callbackFunc = lambda b=self.verticalEdge, s=self.verticalEdgeStatus, r=row, c=col: self.__butCallback(b, s, r, c)
        butMinSizeX = self.EDGE_SIZE
        butMinSizeY = self.CELL_SIZE
        butMaxSizeX = self.EDGE_SIZE
        butMaxSizeY = self.CELL_SIZE
        self.verticalEdge[row][col].pressed.connect(callbackFunc)
        self.verticalEdge[row][col].setMinimumSize(QSize(butMinSizeX, butMinSizeY))
        self.verticalEdge[row][col].setMaximumSize(QSize(butMaxSizeX, butMaxSizeY))
        self.verticalEdge[row][col].setEnabled(True)


    def __addHorizontalEdge(self, row, col):
        self.horizontalEdge[row].append(QPushButton("v"))
        callbackFunc = lambda b=self.horizontalEdge, s=self.horizontalEdgeStatus, r=row, c=col: self.__butCallback(b, s, r, c)
        butMinSizeX = self.CELL_SIZE
        butMinSizeY = self.EDGE_SIZE
        butMaxSizeX = self.CELL_SIZE
        butMaxSizeY = self.EDGE_SIZE
        self.horizontalEdge[row][col].pressed.connect(callbackFunc)
        self.horizontalEdge[row][col].setMinimumSize(QSize(butMinSizeX, butMinSizeY))
        self.horizontalEdge[row][col].setMaximumSize(QSize(butMaxSizeX, butMaxSizeY))


    def __butCallback(self, but, status, row=0, col=0):
        print(str(row) + " " + str(col))
        whiteCode = "FFFFFF"
        redCode = "FF0000"
        status[row][col] = not status[row][col]
        if status[row][col] == True:
            self.__setButtonCollor(but[row][col], redCode)
            print("set")
        else:
            self.__setButtonCollor(but[row][col], whiteCode)
            print("reset")


    def __ChooseStartPosCallback(self):
        self.__setMode("ChooseStartPos")
        print("__ChooseStartPosCallback")


    def __ChooseEndPosCallback(self):
        self.__setMode("ChooseEndPose")
        print("__ChooseEndPosCallback")


    def __ChooseBordersCallback(self):
        self.__setMode("ChooseBorders")
        print("__ChooseBordersCallback")


    def __GenerateJsonCallback(self):
        print("__GenerateJsonCallback")


    def __CreateBordersAroundMapCallback(self):
        print("__CreateBordersAroundMapCallback")


    def __setMode(self, mode):
        whiteCode = "FFFFFF"
        redCode = "FF0000"
        if mode == "ChooseStartPos":
            self.MODE = mode
            self.__setButtonCollor(self.ChooseStartPosButton, redCode)
        else:
            self.__setButtonCollor(self.ChooseStartPosButton, whiteCode)
        if mode == "ChooseEndPose":
            self.MODE = mode
            self.__setButtonCollor(self.ChooseEndPosButton, redCode)
        else:
            self.__setButtonCollor(self.ChooseEndPosButton, whiteCode)
        if mode == "ChooseBorders":
            self.MODE = mode
            self.__setButtonCollor(self.ChooseBordersButton, redCode)
        else:
            self.__setButtonCollor(self.ChooseBordersButton, whiteCode)
    

    def __setButtonCollor(self, but, collor="FFFFFF"):
        but.setStyleSheet("QPushButton {background-color: #" + collor + "}")


    def __createButton(self, butName, callbackFunc):
        but = QPushButton(butName)
        but.pressed.connect(callbackFunc)
        return but


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
