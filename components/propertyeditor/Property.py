
from PyQt4 import QtCore, QtGui

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from components.propertyeditor.ColorCombo import  ColorCombo
from components.propertyeditor.AdvanceEditor import  AdvanceEditor

class Property(QtCore.QObject):
    ROOT_NODE = 0
    ADVANCED_EDITOR = 1
    COMBO_BOX_EDITOR = 2
    COLOR_EDITOR = 3
    CHECKBOX_EDITOR = 4
  
    def __init__(self, name, obj_value, parent=None, obj_type = None,  obj_data=None):
        super(Property, self).__init__(parent)
        self._readOnly = False
        self.obj_type = obj_type
        self.obj_value = obj_value
        self.obj_data = obj_data
        self.setObjectName(name);
        
    def row(self):
        if self.parent():
            #print('children:')
            #print(self.parent().children())
            return self.parent().children().index(self)
        return 0

    def isRoot(self):
        return self.obj_value == None
        
    def value(self, role=None):
        return self.obj_value

    def setValue(self, val):
        self.obj_value = val

    @property
    def readOnly(self):
        return self._readOnly

    @readOnly.setter
    def readOnly(self, value):
        self._readOnly = value      

    @property
    def editorType(self):
        return self.obj_type

    @editorType.setter
    def editorType(self, value):
        self.obj_type = value

    @property
    def propertyData(self):
        return self.obj_data

    @propertyData.setter
    def propertyData(self, value):
        self.obj_data = value

    def createEditor(self, parent, option):
        editor = None
        if(self.obj_type == None or self.obj_type == Property.ROOT_NODE): return None

        if(self.obj_type == Property.ADVANCED_EDITOR):
            advancedEditor = AdvanceEditor(self, parent)
            advancedEditor.button.clicked.connect(lambda: self.onAdvBtnClick(advancedEditor))
            return advancedEditor
            
        if(self.obj_type == Property.CHECKBOX_EDITOR):
            #checked = self.obj_data
            chkBox = QCheckBox(parent)
            #chkBox.setChecked(checked)
            #QObject.connect(advancedEditor.button, SIGNAL('clicked()'),self.onAdvBtnClick);
            return chkBox
            
        if(self.obj_type == Property.COMBO_BOX_EDITOR):
            confiningChoices = self.obj_data
          
            confineCombo = QtGui.QComboBox(parent)
            confineCombo.addItems(confiningChoices)
            confineCombo.currentIndexChanged[int].connect(self.currentIndexChanged)
            return confineCombo
            
        if(self.obj_type == Property.COLOR_EDITOR):
            editor = ColorCombo(self, parent);
            return editor
        
        return None
   
  
    def onAdvBtnClick(self, editor):
        print('onAdvBtnClick')
 
    def setEditorData(self, editor, val):
        if(self.obj_type == None): return False
        
        if(self.obj_type == Property.COMBO_BOX_EDITOR):      
            index = editor.findText(val)
            editor.setCurrentIndex(index)
            return True
            
        if(self.obj_type == Property.ADVANCED_EDITOR): 
            editor.text = val
            return True       
            
        if(self.obj_type == Property.COLOR_EDITOR):
            editor.setColor(val);
            return True;
        else:
            return False;   

  
    def editorData(self, editor):

        if(self.obj_type == None): return False

        if(self.obj_type == Property.ADVANCED_EDITOR):
            return editor.text
            
        if(self.obj_type == Property.CHECKBOX_EDITOR):
            return True  
            
        if(self.obj_type == Property.COMBO_BOX_EDITOR):
            return editor.currentText()
          
        if(self.obj_type == Property.COLOR_EDITOR):  
            return editor.color()
        else:
            return None

  
    @QtCore.pyqtSlot(int)
    def currentIndexChanged(self):
        return
        #self.commitData.emit(self.sender())  
