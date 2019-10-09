#!/usr/bin/env python2
#import json
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#import QtCore, QtGui, QtWidgets

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("World creator")

        layout = QGridLayout()

        self.SIZE_X = 18
        self.SIZE_Y = 18
        self.CELLS_AMOUNT_X = int(self.SIZE_X / 2)
        self.CELLS_AMOUNT_Y = int(self.SIZE_Y / 2)
        self.CELL_SIZE = 30
        self.EDGE_SIZE = 10

        self.cells = list()
        self.horizontalEdge = list()
        self.verticalEdge = list()
        for row in range(self.SIZE_Y,  -1, -1):
            if (row % 2) == 0:
                heRow = int((self.SIZE_Y - row)/2)  # from 0 to 9
                print(heRow)
                self.horizontalEdge.append(list())
                print(heRow)
                for col in range(0, self.SIZE_X, 2):
                    heCol = int(col/2) # from 0 to 8
                    self.addHorizontalEdge(heRow, heCol)
                    layout.addWidget(self.horizontalEdge[heRow][heCol], row, col + 1, 1, 1)
            else:
                veRow = int((self.SIZE_Y - row)/2) # from 0 to 8
                cellRow = int((self.SIZE_Y - row)/2) # from 0 to 8
                self.verticalEdge.append(list())
                self.cells.append(list())
                for col in range(0, self.SIZE_Y, 2):
                    veCol = int(col/2) # from 0 to 9
                    cellCol = int(col/2) # from 0 to 8
                    self.addVerticalEdge(veRow, veCol)
                    self.addCell(cellRow, cellCol)
                    layout.addWidget(self.verticalEdge[veRow][veCol], row, col, 1, 1)
                    layout.addWidget(self.cells[cellRow][cellCol], row, col + 1, 1, 1)
                self.addVerticalEdge(veRow, veCol + 1)
                layout.addWidget(self.verticalEdge[veRow][veCol + 1], row, col + 2, 1, 1)


        widget = QWidget()
        widget.setLayout(layout)

        window_pose_x = 100
        window_pose_y = 100
        window_size_x = 400
        window_size_y = 400
        self.setGeometry(window_pose_x, window_pose_y, window_size_x, window_size_y)
        self.setCentralWidget(widget)

    def addCell(self, row, col):
        self.cells[row].append( QPushButton(str(col) + "/" + str(row)) )
        self.cells[row][col].setMinimumSize(QSize(self.CELL_SIZE, self.CELL_SIZE))
        self.cells[row][col].pressed.connect( lambda r=row, c=col: self.cellCallback(r, c))
        self.cells[row][col].setStyleSheet("QPushButton {background-color: #CFFFFF}")

    def addVerticalEdge(self, row, col):
        self.verticalEdge[row].append( QPushButton("v") )
        self.verticalEdge[row][col].setMinimumSize(QSize(self.EDGE_SIZE, self.CELL_SIZE))
        self.verticalEdge[row][col].setMaximumSize(QSize(self.EDGE_SIZE, self.CELL_SIZE))
        self.verticalEdge[row][col].pressed.connect( lambda r=row, c=col: self.verticalEdgeCallback(r, c))
        self.verticalEdge[row][col].setStyleSheet("QPushButton {background-color: #FFFFFF}")

    def addHorizontalEdge(self, row, col):
        self.horizontalEdge[row].append( QPushButton("h") )
        self.horizontalEdge[row][col].setMinimumSize(QSize(self.CELL_SIZE, self.EDGE_SIZE))
        self.horizontalEdge[row][col].setMaximumSize(QSize(self.CELL_SIZE, self.EDGE_SIZE))
        self.horizontalEdge[row][col].pressed.connect( lambda r=row, c=col: self.horizontalEdgeCallback(r, c))
        self.horizontalEdge[row][col].setStyleSheet("QPushButton {background-color: #FFFFFF}")

    def cellCallback(self, row, col):
        self.cells[row][col].setStyleSheet("QPushButton {background-color: #F00000}")
        print(str(col) + "/" + str(row))

    def verticalEdgeCallback(self, row, col):
        self.verticalEdge[row][col].setStyleSheet("QPushButton {background-color: #00F000}")
        print(str(col) + "/" + str(row))

    def horizontalEdgeCallback(self, row, col):
        self.horizontalEdge[row][col].setStyleSheet("QPushButton {background-color: #0000F0}")
        print(str(col) + "/" + str(row))

app = QApplication(sys.argv)
label = QLabel('World creator v. 0.01')
window = MainWindow()
window.show()

app.exec_()
