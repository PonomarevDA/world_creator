#!/usr/bin/env python3
import sys, random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt
from enum import Enum

# Constants:
class Mode(Enum):
    CHOOSE_MAP_SIZE = 1
    CHOOSE_CELL_SIZE = 2
    CHOOSE_START_POSITION = 3
    CHOOSE_END_POSITION = 4
    CREATE_BOXES = 5
    CREATE_WALLS = 6
    DELETE_WALLS = 7
    CREATE_SIGNS = 8
    CREATE_LIGHTS = 9


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.initUI()
        self.initMap(36, 18)

    def initUI(self):

        self.setGeometry(300, 300, 400, 320)
        self.setWindowTitle('World creator v.2')
        self.show()

        self.lastClickNumber = 0
        self.pressedFirstNode = None
        self.pressedSecondNode = None

    def initMap(self, map_size_x, map_size_y):
        self.MAP_SIZE = [map_size_x, map_size_y]
        self.CELLS_SIZE = [2, 2]
        self.CELLS_AMOUNT = [ int(self.MAP_SIZE[0]/self.CELLS_SIZE[0]), 
                              int(self.MAP_SIZE[1]/self.CELLS_SIZE[1]) ]
        self.walls = list()
        #self.cellsStatus = [[False] * self.CELLS_AMOUNT[0] for i in range(self.CELLS_AMOUNT[1])]
        #self.hWallStatus = [[False] * (self.CELLS_AMOUNT[0]) for i in range(self.CELLS_AMOUNT[1] + 1)]
        #self.vWallStatus = [[False] * (self.CELLS_AMOUNT[0] + 1) for i in range(self.CELLS_AMOUNT[1])]

        self.mode = Mode.CREATE_WALLS

    def mousePressEvent(self, e):
        if self.mode is Mode.CREATE_WALLS:
            pos = e.pos()
            pos = self.calculateNodeIndexes(pos.x(), pos.y())
            if pos != None:
                if self.lastClickNumber == 1:
                    self.lastClickNumber = 2
                    self.pressedSecondNode = pos
                    self.addWall(e, [self.pressedFirstNode, self.pressedSecondNode])
                    self.update()
                else:
                    self.lastClickNumber = 1
                    self.pressedFirstNode = pos


    def addWall(self, e, nodesIndexes):
        """
        @brief Add new wall
        @note there are simple rule to create it:
        1. wall must be only horizontal or vertical
        2. wall must not conflict with walls that already exists
        """
        try:
            if (self.isThisWallVertical(nodesIndexes) or self.isThisWallHorizontal(nodesIndexes)):
                if self.isThereConflictBetweenWalls(nodesIndexes) is not True:
                    print("Wall was added: " + str(nodesIndexes))
                    self.walls.append(nodesIndexes)
                else:
                    print("Error: there is conflict between existing walls and this: " + str(nodesIndexes))
            else:
                print("Error: wall is not vertical or horizontal: " + str(nodesIndexes))
        except:
            print("Error: it's not wall anyway: " + str(nodesIndexes))


    def isThisWallVertical(self, nodesIndexes):
        return nodesIndexes[0][0] is nodesIndexes[1][0]
    def isThisWallHorizontal(self, nodesIndexes):
        return nodesIndexes[0][1] is nodesIndexes[1][1]
    def isThereConflictBetweenWalls(self, nodesIndexes):
        return False

    def paintEvent(self, event=None):

        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        for wall in self.walls:
            self.drawWall(qp, wall[0], wall[1])
        self.drawTable(qp)
        qp.end()


    def drawWall(self, qp, firstNodeIndexes, secondNodeIndexes):
        """
        @brief Draw wall on table
        """
        print("Update wall: " + str([firstNodeIndexes, secondNodeIndexes]))
        firstNodePose = self.calculateRealPosition(firstNodeIndexes)
        secondNodePose = self.calculateRealPosition(secondNodeIndexes)
        self.drawLine(qp, firstNodePose, secondNodePose)


# ******************** Low level methods: raw draw and calculations ********************
    def calculateNodeIndexes(self, point_x, point_y):
        """
        @brief Calculate node coordinate using real mouse position on window
        """
        table = [point_x - self.tableLeft, point_y - self.tableTop]
        node = [int()] * 2

        for axe in range(0, 2):
            node[axe] = int(table[axe] / self.cellsSize[axe])
            if (table[axe] % self.cellsSize[axe]) > (self.cellsSize[axe] / 2):
                node[axe] += 1
            if node[axe] > (self.CELLS_AMOUNT[axe] + 1) or (node[axe] < 0):
                return None
        return node


    def calculateRealPosition(self, nodeIndexes):
        """
        @brief Calculate real node coordinate using node indexes
        """
        return [ self.tableLeft + nodeIndexes[0] * self.cellsSize[0],
                 self.tableTop + nodeIndexes[1] * self.cellsSize[1] ]

    def drawPoints(self, qp):
        """ 
        @brief Draw window background with random points cloud
        """
        qp.setPen(Qt.red)
        size = self.size()
        for i in range(1000):
            x = random.randint(1, size.width()-1)
            y = random.randint(1, size.height()-1)
            qp.drawPoint(x, y)


    def drawLine(self, qp, firstPoseOnWindow, secondPoseOnWindow):
        """ 
        @brief Draw line
        @note it uses real window coordinates 
        """
        pen = QPen(Qt.black, 3, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(*firstPoseOnWindow, *secondPoseOnWindow)


    def drawTable(self, qp):
        """ 
        @brief Draw table with cells
        """
        thinPen = QPen(Qt.black, 0.5, Qt.SolidLine)
        qp.setPen(thinPen)

        windowWidth = self.frameGeometry().width()
        windowHeight = self.frameGeometry().height()

        self.tableRight = int(0.70 * windowWidth)
        self.tableLeft = int(0.05 * windowWidth)
        self.tableBot = int(0.9 * windowHeight)
        self.tableTop = int(0.05 * windowHeight)

        # It is important that table sizes must divided on cell size (or amount) without remainder
        self.tableLeft = self.tableLeft - ((self.tableLeft - self.tableRight) % self.CELLS_AMOUNT[0])
        self.tableTop = self.tableTop - ((self.tableTop - self.tableBot) % self.CELLS_AMOUNT[1])

        self.tableWidth = self.tableRight - self.tableLeft
        self.tableHeight = self.tableBot - self.tableTop
        self.cellsSize = [ int(self.tableWidth/self.CELLS_AMOUNT[0]), int(self.tableHeight/self.CELLS_AMOUNT[1]) ]

        for row in range(self.tableTop, self.tableBot + 1, self.cellsSize[1]):
            qp.drawLine(self.tableLeft, row, self.tableRight, row)
        for col in range(self.tableLeft, self.tableRight + 1, self.cellsSize[0]):
            qp.drawLine(col, self.tableTop, col, self.tableBot)


