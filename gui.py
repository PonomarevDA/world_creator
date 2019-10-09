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


        self.buttons = list()
        for row in range(0, self.SIZE_X + 1, 1):
            self.buttons.append(list())
            if (row % 2) == 0:
                for col in range(0, self.SIZE_Y, 2):
                    self.addEmptySpace(layout, row, col)
                    self.addHorizontalEdge(layout, row, col + 1)
            else:
                for col in range(0, self.SIZE_Y, 2):
                    self.addVerticalEdge(layout, row, col)
                    self.addCell(layout, row, col + 1)
                self.addVerticalEdge(layout, row, col + 2)


        widget = QWidget()
        widget.setLayout(layout)

        window_pose_x = 100
        window_pose_y = 100
        window_size_x = 400
        window_size_y = 400
        self.setGeometry(window_pose_x, window_pose_y, window_size_x, window_size_y)
        self.setCentralWidget(widget)

    def addCell(self, layout, row, col):
        self.buttons[row].append( QPushButton( str(int(1 + self.CELLS_AMOUNT_X - (row + 1)/2)) + "/" + str(int((col + 1)/2)) ))
        self.buttons[row][col].setMinimumSize(QSize(self.CELL_SIZE, self.CELL_SIZE))
        self.buttons[row][col].pressed.connect( lambda r=row, c=col: self.func(r, c))
        self.buttons[row][col].setStyleSheet("QPushButton {background-color: #CFFFFF}") #A3C1DA}")
        layout.addWidget(self.buttons[row][col], row, col, 1, 1)

    def addVerticalEdge(self, layout, row, col):
        self.buttons[row].append( QPushButton("k") )
        self.buttons[row][col].setMinimumSize(QSize(self.EDGE_SIZE, self.CELL_SIZE))
        self.buttons[row][col].setMaximumSize(QSize(self.EDGE_SIZE, self.CELL_SIZE))
        self.buttons[row][col].pressed.connect( lambda r=row, c=col: self.func(r, c))
        self.buttons[row][col].setStyleSheet("QPushButton {background-color: #FFFFFF}") #A3C1DA}")
        layout.addWidget(self.buttons[row][col], row, col, 1, 1)

    def addHorizontalEdge(self, layout, row, col):
        self.buttons[row].append( QPushButton("k") )
        self.buttons[row][col].setMinimumSize(QSize(self.CELL_SIZE, self.EDGE_SIZE))
        self.buttons[row][col].setMaximumSize(QSize(self.CELL_SIZE, self.EDGE_SIZE))
        self.buttons[row][col].pressed.connect( lambda r=row, c=col: self.func(r, c))
        self.buttons[row][col].setStyleSheet("QPushButton {background-color: #FFFFFF}") #A3C1DA}")
        layout.addWidget(self.buttons[row][col], row, col, 1, 1)

    def addEmptySpace(self, layout, row, col):
        self.buttons[row].append( QLabel() )
        self.buttons[row][col].setMinimumSize(QSize(self.EDGE_SIZE, self.EDGE_SIZE))
        self.buttons[row][col].setMaximumSize(QSize(self.EDGE_SIZE, self.EDGE_SIZE))
        #self.buttons[row][col].pressed.connect( lambda r=row, c=col: self.func(r, c))
        #self.buttons[row][col].setStyleSheet("QPushButton {background-color: #FFFFFF}") #A3C1DA}")
        layout.addWidget(self.buttons[row][col], row, col, 1, 1)

    def func(self, row, col):
        self.buttons[row][col].setStyleSheet("QPushButton {background-color: #03C1DA}")
        #self.setStyleSheet("QPushButton {background-color: #03000A}")
        print(str(col + 1) + "/" + str(self.CELLS_AMOUNT_X - row))

app = QApplication(sys.argv)
label = QLabel('World creator v. 0.01')
window = MainWindow()
window.show()

app.exec_()
