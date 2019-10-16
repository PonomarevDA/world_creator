#!/usr/bin/env python3
import sys, random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 400, 320)
        self.setWindowTitle('World creator v.2')
        self.show()

        self.lastClickNumber = 0
        self.firstMousePosition = None
        self.secondMousePosition = None

    def mousePressEvent(self, e):
        if self.lastClickNumber == 1:
            self.lastClickNumber = 2
            self.secondMousePosition = e.pos()
            self.update()
            print("second " + str(e.pos()))
        else:
            self.lastClickNumber = 1
            self.firstMousePosition = e.pos()
            print("first " + str(e.pos()))

    def paintEvent(self, event=None):

        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        self.drawLine(qp)
        self.drawTable(qp)
        qp.end()


    def drawPoints(self, qp):

        qp.setPen(Qt.red)
        size = self.size()

        for i in range(1000):
            x = random.randint(1, size.width()-1)
            y = random.randint(1, size.height()-1)
            qp.drawPoint(x, y)


    def drawLine(self, qp):
        print("kek" + str(self.firstMousePosition))
        if (self.firstMousePosition != None) and (self.secondMousePosition != None):
            first_x = self.firstMousePosition.x()
            first_y = self.firstMousePosition.y()
            second_x = self.secondMousePosition.x()
            second_y = self.secondMousePosition.y()
            print("kek2" + str())
            pen = QPen(Qt.black, 3, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(first_x, first_y, second_x, second_y)

    def drawTable(self, qp):
        """ 
        Draw table with cells
        """
        thinPen = QPen(Qt.black, 0.5, Qt.SolidLine)
        qp.setPen(thinPen)

        windowWidth = self.frameGeometry().width()
        windowHeight = self.frameGeometry().height()

        mapSize = [18, 18]
        cellsSize = [2, 2]
        cellsAmount = [ int(mapSize[0]/cellsSize[0]), int(mapSize[1]/cellsSize[1]) ]
        tableRight = int(0.70 * windowWidth)
        tableLeft = int(0.05 * windowWidth)
        tableBot = int(0.9 * windowHeight)
        tableTop = int(0.05 * windowHeight)

        # It is important that table sizes must divided on cell size (or amount) without remainder
        tableLeft = tableLeft - ((tableLeft - tableRight) % cellsAmount[0])
        tableTop = tableTop - ((tableTop - tableBot) % cellsAmount[1])

        tableWidth = tableRight - tableLeft
        tableHeight = tableBot - tableTop
        cellsSize = [ int(tableWidth/cellsAmount[0]), int(tableHeight/cellsAmount[1]) ]

        for row in range(tableTop, tableBot + 1, cellsSize[1]):
            qp.drawLine(tableLeft, row, tableRight, row)
        for col in range(tableLeft, tableRight + 1, cellsSize[0]):
            qp.drawLine(col, tableTop, col, tableBot)


