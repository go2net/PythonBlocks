
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os

class AdvanceEditor(QWidget):
    def __init__(self, property, parent, showMenuButton=False):
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
        
        if(showMenuButton):
            self.menuButton = QPushButton(self)
            self.menuButton.setText('')
            self.menuButton.setToolTip('Advanced...')
            self.menuButton.setIcon(QIcon(os.getcwd() +'\\resource\\arrow_triangle-down.png'))
            self.menuButton.setFixedSize(18, 18)  
            layout.addWidget(self.menuButton)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        #QObject.connect(button, SIGNAL('clicked()'),self.onButtonClick);

    @property
    def text(self):
        return self.txtEditor.toPlainText()
    @text.setter
    def text(self, value):
        self.txtEditor.setText(value)

class ImageEditor(QWidget):
    def __init__(self, property, delegate, parent, showMenuButton=False):
        super(ImageEditor, self).__init__(parent)
        self.delegate = delegate
        layout = QHBoxLayout(self)
        layout.setSpacing(0)    
        
        self._icon = None
        self._img = None
        
        #self.label = QLabel(self)
        #self.label.resize(self.width(), self.height())
        self.txtEditor = QTextEdit(self)
        #self.txtEditor.setReadOnly(True)
        self.txtEditor.document().setDocumentMargin(0)
        self.txtEditor.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.txtEditor.setVerticalScrollBarPolicy (Qt.ScrollBarAlwaysOff) 
        #self.txtEditor.setFrameStyle(QFrame.NoFrame);

        self.button = QPushButton(self)
        self.button.setText('...')
        self.button.setToolTip('Advanced...')
        self.button.setFixedSize(18, 18)
        
        pol = QSizePolicy (QSizePolicy.Expanding,QSizePolicy.Expanding);
        self.txtEditor.setSizePolicy(pol);
        #policy = self.txtEditor.sizePolicy()
        #policy.setVerticalStretch(1)
        #self.txtEditor.setSizePolicy(policy)
        
        #layout.addWidget(self.label)
        layout.addWidget(self.txtEditor)
        layout.addWidget(self.button)
        
        if(showMenuButton):
            self.menuButton = QPushButton(self)
            self.menuButton.setText('')
            self.menuButton.setToolTip('Advanced...')
            self.menuButton.setIcon(QIcon(os.getcwd() +'\\resource\\arrow_triangle-down.png'))
            self.menuButton.setFixedSize(18, 18)  
            layout.addWidget(self.menuButton)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        #QObject.connect(button, SIGNAL('clicked()'),self.onButtonClick);

    @property
    def text(self):
        return self.txtEditor.toPlainText()
        
    @text.setter
    def text(self, value):
        self.txtEditor.setText(value)
        self.delegate.commitData.emit(self)

    @property
    def icon(self):
        return self._icon
        
    @icon.setter
    def icon(self, value):
        self._icon = value
        self.delegate.commitData.emit(self)
        #tmp_icon =self._icon.scaled(18, 18)
        #self.label.setPixmap(tmp_icon)
        
    @property
    def img(self):
        return self._img
        
    @img.setter
    def img(self, value):
        self._img = value
        self.delegate.commitData.emit(self)
        #tmp_icon =self._icon.scaled(18, 18)
        #self.label.setPixmap(tmp_icon)
                
