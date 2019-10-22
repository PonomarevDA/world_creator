#!/usr/bin/env python3
import sys, random
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QGridLayout, QLabel, QDialog, QFileDialog
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt, QSize
from enum import Enum
from json_converter import *

# Constants:
class Mode(Enum):
    NO_MODE = int(-1)
    CHOOSE_MAP_SIZE = int(0)
    CHOOSE_CELL_SIZE = int(1)
    CHOOSE_START_POSITION = int(2)
    CHOOSE_END_POSITION = int(3)
    CREATE_BOXES = int(4)
    CREATE_WALLS = int(5)
    DELETE_WALLS = int(6)
    CREATE_SIGNS = int(7)
    CREATE_LIGHTS = int(8)

class CollorCode(Enum):
    WHITE = str("FFFFFF")
    BLUE = str("0000FF")
    GREEN = str("00FF00")
    RED = str("FF0000")

class MainWindow(QWidget):
# *************** High level methods which allow create window ***************
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.initUI()
        self.initMap(18, 18)
        self.initControlButtons()

    def initUI(self):
        self.setGeometry(300, 300, 710, 320)
        self.setWindowTitle('World creator v.2')
        self.show()

    def initMap(self, map_size_x, map_size_y):
        self.lastClickNumber = 0
        self.pressedFirstNode = None
        self.pressedSecondNode = None

        self.MAP_SIZE = [map_size_x, map_size_y]
        self.CELLS_SIZE = [2, 2]
        self.CELLS_AMOUNT = [ int(self.MAP_SIZE[0]/self.CELLS_SIZE[0]), 
                              int(self.MAP_SIZE[1]/self.CELLS_SIZE[1]) ]
        self.walls = list()
        self.mode = Mode.NO_MODE

        self.start = None
        self.end = None

    def initControlButtons(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        label = QLabel(' ', self)
        self.layout.addWidget(label, 0, 0)
        self.layout.setSpacing(1)

        self.buttons = list()

        self.buttons.append(self.createButton('1. Choose map size'))
        self.buttons[0].pressed.connect(self.chooseMapSizeCallback)
        self.buttons[0].setEnabled(False)
        self.layout.addWidget(self.buttons[0], 1, 1)

        self.buttons.append(self.createButton('2. Choose cells size'))
        self.buttons[1].pressed.connect(self.chooseCellsSizeCallback)
        self.buttons[1].setEnabled(False)
        self.layout.addWidget(self.buttons[1], 2, 1)

        self.buttons.append(self.createButton('3. Choose start pose'))
        self.buttons[2].pressed.connect(self.chooseStartPoseCallback)
        self.layout.addWidget(self.buttons[2], 3, 1)

        self.buttons.append(self.createButton('4. Choose end pose'))
        self.buttons[3].pressed.connect(self.chooseEndPoseCallback)
        self.buttons[3].setEnabled(False)
        self.layout.addWidget(self.buttons[3], 4, 1)

        self.buttons.append(self.createButton('5. Create boxes'))
        self.buttons[4].pressed.connect(self.createBoxesCallback)
        self.buttons[4].setEnabled(False)
        self.layout.addWidget(self.buttons[4], 5, 1)

        self.buttons.append(self.createButton('6. Create walls'))
        self.buttons[5].pressed.connect(self.createWallsCallback)
        self.layout.addWidget(self.buttons[5], 6, 1)

        self.buttons.append(self.createButton('7. Delete walls'))
        self.buttons[6].pressed.connect(self.deleteWallsCallback)
        self.layout.addWidget(self.buttons[6], 7, 1)

        self.buttons.append(self.createButton('8. Create signs'))
        self.buttons[7].pressed.connect(self.createSignsCallback)
        self.buttons[7].setEnabled(False)
        self.layout.addWidget(self.buttons[7], 8, 1)

        self.buttons.append(self.createButton('9. Create lights'))
        self.buttons[8].pressed.connect(self.createLightsCallback)
        self.buttons[8].setEnabled(False)
        self.layout.addWidget(self.buttons[8], 9, 1)

        self.buttons.append(self.createButton('Load json'))
        self.buttons[9].pressed.connect(self.loadJsonCallback)
        self.layout.addWidget(self.buttons[9], 11, 1)

        self.buttons.append(self.createButton('Generate json'))
        self.buttons[10].pressed.connect(self.generateJsonCallback)
        self.layout.addWidget(self.buttons[10], 13, 1)

        self.buttons.append(self.createButton('Create sdf world from json'))
        self.buttons[11].pressed.connect(self.createSdfCallback)
        self.layout.addWidget(self.buttons[11], 14, 1)

        self.layout.addWidget(QLabel('To create the world:', self), 0, 1)
        self.layout.addWidget(QLabel('Or use these features:', self), 10, 1)
        self.layout.addWidget(QLabel('Then press buttons below:',self), 12, 1)

    def createButton(self, name):
        but = QPushButton(name, self)
        but.setFixedSize(QSize(200, 25))
        return but
    def setButtonCollor(self, but, collor = CollorCode.WHITE):
        but.setStyleSheet("QPushButton {background-color: #" + \
                          collor.value + "}")

# ************** Control methods which allow to choose mode ******************
    def chooseMapSizeCallback(self):
        print(self.buttons[0].text())
    def chooseCellsSizeCallback(self):
        print(self.buttons[1].text())
    def chooseStartPoseCallback(self):
        print(self.buttons[Mode.CHOOSE_START_POSITION.value].text())
        self.setMode(Mode.CHOOSE_START_POSITION)
    def chooseEndPoseCallback(self):
        print(self.buttons[3].text())
    def createBoxesCallback(self):
        print(self.buttons[4].text())
    def createWallsCallback(self):
        print(self.buttons[Mode.CREATE_WALLS.value].text())
        self.setMode(Mode.CREATE_WALLS)
    def deleteWallsCallback(self):
        print(self.buttons[Mode.DELETE_WALLS.value].text())
        self.setMode(Mode.DELETE_WALLS)
    def createSignsCallback(self):
        print(self.buttons[7].text())
    def createLightsCallback(self):
        print(self.buttons[8].text())
    def loadJsonCallback(self):
        print(self.buttons[9].text())
        FILE_TYPES = "Json Files (*.json)"
        filePath = QFileDialog.getOpenFileName(self, "", "", FILE_TYPES)[0]
        objects = load_frontend_from_json(filePath)
        self.start = objects[0]
        finish = objects[1]
        size = objects[2]
        boxes = objects[3]
        self.walls = objects[4]
        self.update()
    def generateJsonCallback(self):
        print(self.buttons[10].text())
        create_json_from_gui(self.start, self.MAP_SIZE, None, self.walls)
    def createSdfCallback(self):
        print(self.buttons[11].text())
        create_sdf_from_json()
    def setMode(self, mode):
        """
        @brief set mode from class Mode(enum)
        """
        try:
            for i in range(0, 10):
                self.setButtonCollor(self.buttons[i], CollorCode.WHITE)
            self.setButtonCollor(self.buttons[mode.value], CollorCode.RED)
            self.mode = mode
        except:
            print("Error: mode must be Enum")

# ************ Methods which allow to create and delete walls ****************
    def mousePressEvent(self, e):
        pos = e.pos()
        if self.mode is Mode.CHOOSE_START_POSITION:
            self.start = self.calculateCellIndexes(pos.x(), pos.y())
            print("start pose was setted using mouse: " + str(self.start))
        elif self.mode is Mode.CREATE_WALLS:
            pos = self.calculateNodeIndexes(pos.x(), pos.y())
            if self.lastClickNumber is 1:
                self.lastClickNumber = 2
                self.pressedSecondNode = pos
                self.addWall([self.pressedFirstNode, self.pressedSecondNode])
            else:
                self.lastClickNumber = 1
                self.pressedFirstNode = pos
        elif self.mode is Mode.DELETE_WALLS:
            pos = self.calculateEdgeIndexes(pos.x(), pos.y())
            self.deleteWall(pos)
        else:
            print("Warning: you should choose mode")
        self.update()

    def addBox(self, pos):
        pass


    def addWall(self, nodesIndexes):
        """
        @brief Try to add new wall
        """
        if self.isWallPossible(nodesIndexes) is True:
            print("Wall was added: " + str(nodesIndexes))
            self.walls.append(nodesIndexes)

    def isWallPossible(self, nodesIndexes):
        """
        @brief Check if the wall is possible
        @note print the reason if wall is not possible
        """
        if self.isWallOutOfRange(nodesIndexes) is True:
            print("Warning: wall out of map: " + str(nodesIndexes))
        elif self.isThisWallPoint(nodesIndexes) is True:
            print("Warning: wall can't be point: " + str(nodesIndexes))
        elif self.isThisWallDiagonal(nodesIndexes) is True:
            print("Warning: wall can't be diagonal: " + str(nodesIndexes))
        elif self.isThereConflictBetweenWalls(nodesIndexes) is True:
            print("Warning: there is conflict between existing walls \
            and this: " + str(nodesIndexes))
        else:
            return True
        return False


    def deleteWall(self, pos):
        """
        @brief Delete wall
        """
        print(self.walls)
        try:
            isVerticalFound = False
            isHorizontalFound = False
            for wall in self.walls:
                if((wall[0][0] is pos[0]) and (wall[1][0] is pos[0])):
                    if(wall[0][1] <= pos[1] and wall[1][1] >= pos[1]) or \
                      (wall[1][1] <= pos[1] and wall[0][1] >= pos[1]):
                        isVerticalFound = True
                        break
                if(wall[0][1] is pos[1]) and (wall[1][1] is pos[1]):
                    if(wall[0][0] <= pos[0] and wall[1][0] >= pos[0]) or \
                      (wall[1][0] <= pos[0] and wall[0][0] >= pos[0]):
                        isHorizontalFound = True
                        break
            if isVerticalFound == True:
                print("delete vertical: " + str(wall) + " and " + str(pos))
                self.walls.remove(wall)
            elif isHorizontalFound == True:
                print("delete horizontal: " + str(wall) + " and " + str(pos))
                self.walls.remove(wall)
            self.update()
        except:
            print("Warning: it's not wall")


    def isThisWallPoint(self, nodesIndexes):
        return nodesIndexes[0] == nodesIndexes[1]
    def isWallOutOfRange(self, nodesIndexes):
        return  nodesIndexes[0][0] > self.CELLS_AMOUNT[0] or \
                nodesIndexes[0][0] < 0 or \
                nodesIndexes[1][0] > self.CELLS_AMOUNT[0] or \
                nodesIndexes[1][0] < 0 or \
                nodesIndexes[0][1] > self.CELLS_AMOUNT[1] or \
                nodesIndexes[0][1] < 0 or \
                nodesIndexes[1][1] > self.CELLS_AMOUNT[1] or \
                nodesIndexes[1][1] < 0
    def isThisWallDiagonal(self, nodesIndexes):
        return ((self.isThisWallVertical(nodesIndexes) is False) and \
                (self.isThisWallHorizontal(nodesIndexes) is False))
    def isThisWallVertical(self, nodesIndexes):
        return nodesIndexes[0][0] == nodesIndexes[1][0]
    def isThisWallHorizontal(self, nodesIndexes):
        return nodesIndexes[0][1] == nodesIndexes[1][1]
    def isThereConflictBetweenWalls(self, nodesIndexes):
        return False

    def paintEvent(self, event=None):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        for wall in self.walls:
            self.drawWall(qp, wall[0], wall[1])
        self.drawTable(qp)
        if self.start is not None:
            self.drawBox(qp, self.start)
        qp.end()


    def drawBox(self, qp, cellIndexes):
        """
        @brief Draw box on table
        @param cellIndexes - x and y indexes from 0 to CELLS_AMOUNT - 1
        """
        try:
            centerPos = self.calculateRealPositionByCellIndexes(cellIndexes)
            self.drawRectangle(qp, centerPos, self.cellsSize)
        except:
            print("Error")


    def drawWall(self, qp, indexesOfNode1, indexesOfNode2):
        """
        @brief Draw wall on table
        @param indexesOfNode1 - x and y indexes from 0 to CELLS_AMOUNT - 1
        @param indexesOfNode2 - x and y indexes from 0 to CELLS_AMOUNT - 1
        """
        posOfNode1 = self.calculateRealPositionByNodeIndexes(indexesOfNode1)
        posOfNode2 = self.calculateRealPositionByNodeIndexes(indexesOfNode2)
        self.drawLine(qp, posOfNode1, posOfNode2)


# *************** Low level methods: raw draw and calculations ***************
# *************** Basicaly methods below work with real window positions *****
    def calculateCellIndexes(self, point_x, point_y):
        """
        @brief Calculate cell coordinate using real mouse position on window
        """
        tablePose = [point_x - self.tableLeft, point_y - self.tableTop]
        node = [int()] * 2

        for axe in range(0, 2):
            node[axe] = int(tablePose[axe] / self.cellsSize[axe])
            if node[axe] > (self.CELLS_AMOUNT[axe] + 1) or (node[axe] < 0):
                return None
        return node

    def calculateNodeIndexes(self, point_x, point_y):
        """
        @brief Calculate node coordinate using real mouse position on window
        @note node indexes will be out of rate if point coordinate out of rate
        """
        tablePose = [point_x - self.tableLeft, point_y - self.tableTop]
        node = [int()] * 2

        for axe in range(0, 2):
            node[axe] = int(tablePose[axe] / self.cellsSize[axe])
            # Line below is needed because of unexpected work of division of
            # negative nubmers  
            if tablePose[axe] < 0: node[axe] -= 1 
            if tablePose[axe] % self.cellsSize[axe] > self.cellsSize[axe] / 2:
                node[axe] += 1
        return node

    def calculateEdgeIndexes(self, point_x, point_y):
        """
        @brief Calculate edge coordinate using real mouse position on window
        @note edge indexes will be out of rate if point coordinate out of rate
        """
        tablePose = [point_x - self.tableLeft, point_y - self.tableTop]
        node = [int()] * 2

        for axe in range(0, 2):
            node[axe] = int(tablePose[axe] / self.cellsSize[axe])
            fourthNode = self.cellsSize[axe]/4
            remnant = tablePose[axe] % self.cellsSize[axe]
            if (remnant >= fourthNode) and (remnant <= 3*fourthNode):
                node[axe] += 0.5
            elif remnant > 3*fourthNode:
                node[axe] += 1
        if(((node[0] % 1) is 0) and ((node[1] % 1) is not 0)) or \
          (((node[0] % 1) is not 0) and ((node[1] % 1) is 0)):
            return node
        return None
      

    def calculateRealPositionByCellIndexes(self, cellIndexes):
        """
        @brief Calculate real node coordinate using node indexes
        """
        return [self.tableLeft + (cellIndexes[0] + 1) * self.cellsSize[0],
                self.tableTop + (cellIndexes[1] + 1) * self.cellsSize[1]]
      

    def calculateRealPositionByNodeIndexes(self, nodeIndexes):
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


    def drawRectangle(self, qp, centerPosition, size, collor=QColor(255, 0, 0)):
        """ 
        @brief Draw rectangle
        @note it uses real window coordinates 
        """
        brush = QBrush(collor)
        qp.setBrush(brush)
        left = centerPosition[0] - self.cellsSize[0]
        top = centerPosition[1] - self.cellsSize[1]
        qp.drawRect(left, top, self.cellsSize[0], self.cellsSize[1])


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

        # It is important that table sizes must divided on cell size (or 
        # amount) without remainder
        self.tableLeft = self.tableLeft - ((self.tableLeft - self.tableRight) % self.CELLS_AMOUNT[0])
        self.tableTop = self.tableTop - ((self.tableTop - self.tableBot) % self.CELLS_AMOUNT[1])

        self.tableWidth = self.tableRight - self.tableLeft
        self.tableHeight = self.tableBot - self.tableTop
        self.cellsSize = [ int(self.tableWidth/self.CELLS_AMOUNT[0]), int(self.tableHeight/self.CELLS_AMOUNT[1]) ]

        for row in range(self.tableTop, self.tableBot + 1, self.cellsSize[1]):
            qp.drawLine(self.tableLeft, row, self.tableRight, row)
        for col in range(self.tableLeft, self.tableRight + 1, self.cellsSize[0]):
            qp.drawLine(col, self.tableTop, col, self.tableBot)


