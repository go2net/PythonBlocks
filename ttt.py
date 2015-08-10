#!/usr/bin/env python

import sys

from PyQt4.QtCore import SIGNAL

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QTreeView
from PyQt4.QtGui import QTreeWidgetItem

class MyTreeItem(QTreeWidgetItem):

    def __init__(self, s, parent = None):

        super(MyTreeItem, self).__init__(parent, [s])

class MyTree(QTreeView):

    def __init__(self, parent = None):

        super(MyTree, self).__init__(parent)
        self.setMinimumWidth(200)
        self.setMinimumHeight(200)
        for s in ['foo', 'bar']:
            MyTreeItem(s, self)
        self.connect(self, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.onClick)

    def onClick(self, item, column):

        print(item)

class MainWindow(QMainWindow):

    def __init__(self, parent = None):

        super(MainWindow, self).__init__(parent)
        self.tree = MyTree(self)

def main():

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()

if __name__ == '__main__':
    main()
