from MainWnd import MainWnd
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWnd.getInstance()
    sys.exit(app.exec_())
