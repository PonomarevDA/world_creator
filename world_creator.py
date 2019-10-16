#!/usr/bin/env python3

"""
This create gui that allow to create json and sdf files.
"""

from tests import *

MODE_CREATE_WORLD_FROM_OLD_GUI = "CreateWorldFromOldGui"
MODE_CREATE_WORLD_FROM_NEW_GUI = "CreateWorldFromNEWGui"
MODE_CREATE_WORLD_FROM_TEST_JSON = "CreateWorldFromTestJson"
mode = MODE_CREATE_WORLD_FROM_NEW_GUI

if __name__=="__main__":
    if mode == MODE_CREATE_WORLD_FROM_OLD_GUI:
        from gui_old import *
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec_()
    elif mode == MODE_CREATE_WORLD_FROM_NEW_GUI:
        from gui_new import *
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec_()
    elif mode == MODE_CREATE_WORLD_FROM_TEST_JSON:
        testJsonCreation()
        createWorldFromJson()

