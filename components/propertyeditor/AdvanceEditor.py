
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class AdvanceEditor(QWidget):
  def __init__(self, property, parent):
    super(AdvanceEditor, self).__init__(parent)
    
    layout = QHBoxLayout(self)
    layout.setSpacing(0)    

    editor = QTextEdit(self)
    editor.setReadOnly(True)
    editor.document().setDocumentMargin(0)
    editor.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    editor.setVerticalScrollBarPolicy (Qt.ScrollBarAlwaysOff) 
    editor.setFrameStyle(QFrame.NoFrame);
    
    self.button = QPushButton(self)
    self.button.setText('...')
    self.button.setToolTip('Advanced...')
    self.button.setFixedSize(18, 18)
    
    layout.addWidget(editor)
    layout.addWidget(self.button)

    layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(layout)

    #QObject.connect(button, SIGNAL('clicked()'),self.onButtonClick);
    
  #def onButtonClick(self):
  #  print('onButtonClick')
