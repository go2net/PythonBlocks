
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ColorCombo(QComboBox):
    def __init__(self, property, parent):
        super(ColorCombo, self).__init__(parent)
        self.property = property
        #self.delegate = delegate
        colorNames = QColor.colorNames();
        self.m_init = QColor(0, 0, 255)
        index = 0
        for name in  colorNames:
            color = QColor(name);
            self.insertItem(index, name);
            self.setItemData(index, color, Qt.DecorationRole);
            index += 1
        self.addItem("Custom", QVariant.UserType);
        #self.connect(self, QtCore.SIGNAL("currentIndexChanged(int)"), self, SLOT(self.currentChanged));
        self.currentIndexChanged[int].connect(self.currentChanged)
        #self.setMinimumHeight(21)
    
    @property
    def color(self):
        return self.itemData(self.currentIndex(), Qt.DecorationRole);

    @color.setter
    def color(self, value):
        self.m_init = value;
        self.setCurrentIndex(self.findData(value,Qt.DecorationRole));
        if (self.currentIndex() == -1):
            self.addItem(value.name());
            self.setItemData(self.count()-1, value, Qt.DecorationRole);
            self.setCurrentIndex(self.count()-1);     

    def currentChanged(self,  index):

        if (self.itemData(index) == QVariant.UserType):
            color = QColorDialog.getColor(self.m_init, self);
            if (color.isValid()):
                if (self.findData(color, Qt.DecorationRole) == -1):
                    self.addItem(color.name());
                    self.setItemData(self.count()-1, color, Qt.DecorationRole);
              
                self.setCurrentIndex(self.count()-1);

            else:
                self.setCurrentIndex(self.findData(self.m_init));
                
        #self.delegate.commitData.emit(self)
        #self.emit(SIGNAL("commitData(QWidget*)"), self.parent())
        
        #self.commitData.emit(self.sender())
        #self.property.setValue(self.color())
        #self.parent().update()

