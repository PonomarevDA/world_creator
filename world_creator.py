#!/usr/bin/env python3

"""
This create gui that allow to create json and sdf files.
"""

from tests import *
from gui import *

MODE_CREATE_WORLD_FROM_GUI = "CreateWorldFromGui"
MODE_CREATE_WORLD_FROM_TEST_JSON = "CreateWorldFromTestJson"
mode = MODE_CREATE_WORLD_FROM_GUI

if __name__=="__main__":
    if mode == MODE_CREATE_WORLD_FROM_GUI:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec_()
    elif mode == MODE_CREATE_WORLD_FROM_TEST_JSON:
        testJsonCreation()
        createWorldFromJson()

