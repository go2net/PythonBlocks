
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class RestrictFileDialog(QFileDialog) :
    def __init__(self, parent):
        super(RestrictFileDialog, self).__init__(parent)
        print('__init__')
        self.mtopDir = ''
        self.directoryEntered.connect(self.checkHistory)
        self.directoryEntered.connect(self.checkGoToParent)
        self.findChild(QToolButton, "backButton").clicked.connect(self.checkGoToParent)
        self.findChild(QToolButton, "forwardButton").clicked.connect(self.checkGoToParent)
        self.findChild(QLineEdit, "fileNameEdit").textChanged.connect(self.checkLineEdit)

        self.findChild(QLineEdit, "fileNameEdit").installEventFilter(self)
        self.findChild(QWidget, "listView").installEventFilter(self)
        self.findChild(QWidget, "treeView").installEventFilter(self)
        
        self.findChild(QLineEdit, "fileNameEdit").completer().popup().installEventFilter(self);
        self.setOption(QFileDialog.DontUseNativeDialog, False);
    
    def getRelatedPath(self):
        return self.selectedFiles()[0][(len(self.mtopDir)+1):]

    def eventFilter(self, o, e):
        if (e.type() != QEvent.KeyPress):
            return False;
        key = e.key()
        if (o.objectName() == "listView" or o.objectName() == "treeView"):
            return (Qt.Key_Backspace == key and not self.pathFits(self.directory().absolutePath()))
        else:
            if (Qt.Key_Return != key and Qt.Key_Enter != key):
                return False;
            text = self.findChild(QLineEdit, "fileNameEdit").text()
            path = QDir.cleanPath(self.directory().absolutePath() + ("" if text.startswith("/") else "/") + text)
            a = QDir(text).isAbsolute()
            return not((not a and self.pathFits(path)) or (a and self.pathFits(text)));

    def setTopDir(self, path):
        if (path == self.mtopDir):
            return
            
        if(QFileInfo(path).isDir()) :
            self.mtopDir  = QFileInfo(path).absoluteFilePath()
        else:
            self.mtopDir  = ''
        
        if (not self.pathFits(path)):
            self.setDirectory(self.mtopDir);
            self.checkHistory();
            self.checkLineEdit(self.findChild(QLineEdit, "fileNameEdit").text());
        else:
            ledt = self.findChild(QLineEdit, "fileNameEdit")
            ledt.setText(ledt.text());
        self.findChild(QWidget,"lookInCombo").setEnabled(self.mtopDir == '');
        self.findChild(QWidget, "sidebar").setEnabled(self.mtopDir=='');
        self.checkGoToParent()


    def topDir(self) :
        return self.mtopDir;

    def pathFits(self, path):
        return self.mtopDir == '' or (path.startswith(self.mtopDir) and len(path) > len(self.mtopDir))

    def checkHistory(self):      
        list = self.history()
        for i in range(len(list) - 1, 0, -1):
            if (not self.pathFits(list[i])):
                del list[i]
        self.setHistory(list);

    def checkGoToParent(self):
        self.findChild(QToolButton,"toParentButton").setEnabled(self.pathFits(self.directory().absolutePath()))

    def checkLineEdit(self, text):
        btn = self.findChild(QDialogButtonBox,"buttonBox").buttons()[0];
        path = QDir.cleanPath(self.directory().absolutePath() + ("" if text.startswith("/") else "/") + text)
        a = QDir(text).isAbsolute();
        btn.setEnabled(btn.isEnabled() and ((not a and self.pathFits(path)) or (a and self.pathFits(text))))
