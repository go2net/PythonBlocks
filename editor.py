import sys, os
from PyQt4 import QtGui, Qsci

class Window(Qsci.QsciScintilla):
    def __init__(self):
        Qsci.QsciScintilla.__init__(self)
        self.setLexer(Qsci.QsciLexerPython(self))
        self.setText(open(os.path.abspath(__file__)).read())

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 500, 500)
    window.show()
    sys.exit(app.exec_())
