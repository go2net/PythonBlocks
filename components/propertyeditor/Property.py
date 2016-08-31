
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import functools
from components.propertyeditor.ColorCombo import  ColorCombo
from components.propertyeditor.AdvanceEditor import  AdvanceEditor,AdvancedComboBox, ImageEditor, CustomerEditor

class Property(QtCore.QObject):
    ROOT_NODE = 0
    ADVANCED_EDITOR = 1    
    ADVANCED_EDITOR_WITH_MENU = 2
    CUSTOMER_EDITOR = 3
    COMBO_BOX_EDITOR = 4
    ADVANCED_COMBO_BOX = 5
    COLOR_EDITOR = 6
    CHECKBOX_EDITOR = 7
    IMAGE_EDITOR = 8
    EDITOR_NONE = 9
  
    def __init__(self, name, obj_value, parent=None, obj_type = None,  obj_data=None):
        super(Property, self).__init__(parent)
        self._readOnly = False
        self.obj_type = obj_type
        self.obj_value = obj_value
        self.obj_data = obj_data
        self.setObjectName(name);
        
        self.ui_file = ''
    
        self.signal_slot_maps = {}
    
    def addWidget(self,  widget):
        self.widgets.append(widget)
    
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

    #def remove(self, node):
    #    return self.children().remove(node)   

    def createEditor(self, delegate, parent, option):
        editor = None
        if(self.obj_type == None or self.obj_type == Property.ROOT_NODE): return None

        if(self.obj_type == Property.ADVANCED_EDITOR):
            advancedEditor = AdvanceEditor(self, parent)
            advancedEditor.button.clicked.connect(lambda: self.onAdvBtnClick(advancedEditor))
            return advancedEditor
        if(self.obj_type == Property.ADVANCED_EDITOR_WITH_MENU):
            advancedEditor = AdvanceEditor(self, parent, True)
            advancedEditor.button.clicked.connect(lambda: self.onAdvBtnClick(advancedEditor))
            advancedEditor.menuButton.clicked.connect(lambda: self.onMenuBtnClick(advancedEditor))
            return advancedEditor
            
        if(self.obj_type == Property.CUSTOMER_EDITOR):
            customerEditor = CustomerEditor(self, parent)
            if(self.ui_file != ''):
                customerEditor.loadUi(self.ui_file)
            
            for obj_str in self.signal_slot_maps:
                __obj = getattr(customerEditor, obj_str)
                print(len(self.signal_slot_maps[obj_str]))
                if(len(self.signal_slot_maps[obj_str]) == 3):
                    print(self.signal_slot_maps[obj_str][2])
                    __obj.setEnabled(self.signal_slot_maps[obj_str][2])
                __signal = getattr(__obj, self.signal_slot_maps[obj_str][0])
                __slot = self.signal_slot_maps[obj_str][1]
                __signal.connect(functools.partial(__slot, customerEditor, self))      
                
            return customerEditor 
        
    
        if(self.obj_type == Property.IMAGE_EDITOR):
            imageEditor = ImageEditor(self, delegate, parent, True)            
            imageEditor.button.clicked.connect(lambda: self.onAdvBtnClick(imageEditor))
            imageEditor.menuButton.clicked.connect(lambda: self.onMenuBtnClick(imageEditor))
            return imageEditor
        
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
            confineCombo.setEditable(False) 
            #confineCombo.currentIndexChanged.connect( lambda sender=confineCombo, _delegate=delegate: self.onIndexChanged(sender, _delegate)) 
            return confineCombo
            
        if(self.obj_type == Property.ADVANCED_COMBO_BOX):
            confiningChoices = self.obj_data
          
            advComboBox = AdvancedComboBox(self, parent)
            advComboBox.comboBox.addItems(confiningChoices)
            advComboBox.button.clicked.connect(lambda: self.onAdvBtnClick(advComboBox))
            advComboBox.comboBox.currentIndexChanged['QString'].connect( lambda val, sender=advComboBox:self.onIndexChanged(val, sender)) 
            return advComboBox            
            
        if(self.obj_type == Property.COLOR_EDITOR):
            editor = ColorCombo(self, parent);
            return editor
        
        return None
   
  
    def onAdvBtnClick(self, editor):
        print('onAdvBtnClick')        
       
    def editTextChanged(self,  text):
        print(text)
        pass
    
    def onMenuBtnClick(self, editor):
        print('onMenuBtnClick')        
        
 
    def setEditorData(self, editor, val):
        if(self.obj_type == None): return False
        
        if(self.obj_type == Property.COMBO_BOX_EDITOR):      
            index = editor.findText(val)
            editor.setCurrentIndex(index)
            return True
            
        if(self.obj_type == Property.ADVANCED_COMBO_BOX):      
            index = editor.comboBox.findText(val)
            editor.comboBox.setCurrentIndex(index)
            return True
            
        if(self.obj_type == Property.ADVANCED_EDITOR): 
            editor.text = val
            return True
            
        if(self.obj_type == Property.COLOR_EDITOR):
            editor.color = val
            return True; 

        if(self.obj_type == Property.IMAGE_EDITOR):
            if(val != None):
                editor.icon = val['icon']
                editor.text = val['url']
                editor.img = val['img']
            return True;
 
        return False;  
            
    def editorData(self, editor):

        if(self.obj_type == None): return False

        if(self.obj_type == Property.ADVANCED_EDITOR):
            return editor.text
            
        if(self.obj_type == Property.CHECKBOX_EDITOR):
            return True  
            
        if(self.obj_type == Property.COMBO_BOX_EDITOR):
            return editor.currentText()
            
        if(self.obj_type == Property.ADVANCED_COMBO_BOX):
            return editor.comboBox.currentText()   
            
        if(self.obj_type == Property.COLOR_EDITOR):  
            return editor.color
            
        if(self.obj_type == Property.IMAGE_EDITOR):  
            image_data = {}
            image_data['url'] = editor.text
            image_data['icon'] = editor.icon
            image_data['img'] = editor.img
            return image_data

        return None
      
    #@QtCore.pyqtSlot(int)
    def onIndexChanged(self, text, sender):
        print(sender)
        #delegate.commitData.emit(sender)
        #self.commitData.emit(self.sender())  
