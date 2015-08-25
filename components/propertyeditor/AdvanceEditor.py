
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class AdvanceEditor(QWidget):
    def __init__(self, property, parent):
        super(AdvanceEditor, self).__init__(parent)

        layout = QHBoxLayout(self)
        layout.setSpacing(0)    

        self.txtEditor = QTextEdit(self)
        self.txtEditor.setReadOnly(True)
        self.txtEditor.document().setDocumentMargin(0)
        self.txtEditor.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.txtEditor.setVerticalScrollBarPolicy (Qt.ScrollBarAlwaysOff) 
        self.txtEditor.setFrameStyle(QFrame.NoFrame);

        self.button = QPushButton(self)
        self.button.setText('...')
        self.button.setToolTip('Advanced...')
        self.button.setFixedSize(18, 18)

        layout.addWidget(self.txtEditor)
        layout.addWidget(self.button)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        #QObject.connect(button, SIGNAL('clicked()'),self.onButtonClick);

    @property
    def text(self):
        return self.txtEditor.toPlainText()
    @text.setter
    def text(self, value):
        self.txtEditor.setText(value)
