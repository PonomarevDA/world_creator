#!/usr/bin/env python3

"""
This create gui that allow to create json and sdf files.
"""

from gui import *

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

