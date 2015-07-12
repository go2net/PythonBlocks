from PyQt4 import QtGui, QtCore

class DockContents(QtGui.QWidget):
    _sizehint = None

    def setSizeHint(self, width, height):
        self._sizehint = QtCore.QSize(width, height)

    def sizeHint(self):
        print('sizeHint:', self._sizehint)
        if self._sizehint is not None:
            return self._sizehint
        return super(MyWidget, self).sizeHint()

class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setCentralWidget(QtGui.QTextEdit(self))

        self.dock = QtGui.QDockWidget('Tool Widget', self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock)

        contents = DockContents(self)
        contents.setSizeHint(400, 100)
        layout = QtGui.QVBoxLayout(contents)
        layout.setContentsMargins(0, 0, 0, 0)
        self.toolwidget = QtGui.QListWidget(self)
        layout.addWidget(self.toolwidget)

        self.dock.setWidget(contents)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 600, 400)
    window.show()
    sys.exit(app.exec_())
