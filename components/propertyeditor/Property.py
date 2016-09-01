
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import functools
from components.propertyeditor.ColorCombo import  ColorCombo
from components.propertyeditor.AdvanceEditor import  AdvanceEditor,AdvancedComboBox, ImageEditor, CustomerEditor

class Property(object):
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
  
    def __init__(self, name='', value=None, parent=None, editor_type = None,  data=None):
        self.parentItem = parent
        self._readOnly = False
        self.editor_type = editor_type
        self.value = value
        self.data = data
        self.name = name
        self.childItems = []
        self.ui_file = ''
    
        self.signal_slot_maps = {}
    
    def child(self, row):
        return self.childItems[row]
        
    def parent(self):
        print('hello')
        return self.parentItem
    
    def addWidget(self,  widget):
        self.widgets.append(widget)
    
    def row(self):
        if self.parent():
            #print('children:')
            #print(self.parent().children())
            return self.parent().children().index(self)
        return 0

    def childCount(self):
        return len(self.childItems)        

    def isRoot(self):
        return self.value == None
        
    def value(self, role=None):
        return self.value

    def setValue(self, val):
        self.value = val

    def insertChildren(self, position, count):
        if position < 0 or position > len(self.childItems):
            return False
            
        for row in range(count):
            item = Property()
            self.childItems.insert(position, item)
        return True

    @property
    def readOnly(self):
        return self._readOnly

    @readOnly.setter
    def readOnly(self, value):
        self._readOnly = value      

    @property
    def editorType(self):
        return self.editor_type

    @editorType.setter
    def editorType(self, value):
        self.editor_type = value

    @property
    def propertyData(self):
        return self.data

    @propertyData.setter
    def propertyData(self, value):
        self.data = value

    #def remove(self, node):
    #    return self.children().remove(node)   

    def createEditor(self, delegate, parent, option):
        editor = None
        if(self.editor_type == None or self.editor_type == Property.ROOT_NODE): return None

        if(self.editor_type == Property.ADVANCED_EDITOR):
            advancedEditor = AdvanceEditor(self, parent)
            advancedEditor.button.clicked.connect(lambda: self.onAdvBtnClick(advancedEditor))
            return advancedEditor
        if(self.editor_type == Property.ADVANCED_EDITOR_WITH_MENU):
            advancedEditor = AdvanceEditor(self, parent, True)
            advancedEditor.button.clicked.connect(lambda: self.onAdvBtnClick(advancedEditor))
            advancedEditor.menuButton.clicked.connect(lambda: self.onMenuBtnClick(advancedEditor))
            return advancedEditor
            
        if(self.editor_type == Property.CUSTOMER_EDITOR):
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
        
    
        if(self.editor_type == Property.IMAGE_EDITOR):
            imageEditor = ImageEditor(self, delegate, parent, True)            
            imageEditor.button.clicked.connect(lambda: self.onAdvBtnClick(imageEditor))
            imageEditor.menuButton.clicked.connect(lambda: self.onMenuBtnClick(imageEditor))
            return imageEditor
        
        if(self.editor_type == Property.CHECKBOX_EDITOR):
            #checked = self.data
            chkBox = QCheckBox(parent)
            #chkBox.setChecked(checked)
            #QObject.connect(advancedEditor.button, SIGNAL('clicked()'),self.onAdvBtnClick);
            return chkBox
            
        if(self.editor_type == Property.COMBO_BOX_EDITOR):
            confiningChoices = self.data
          
            confineCombo = QtGui.QComboBox(parent)
            confineCombo.addItems(confiningChoices)
            confineCombo.setEditable(False) 
            #confineCombo.currentIndexChanged.connect( lambda sender=confineCombo, _delegate=delegate: self.onIndexChanged(sender, _delegate)) 
            return confineCombo
            
        if(self.editor_type == Property.ADVANCED_COMBO_BOX):
            confiningChoices = self.data
          
            advComboBox = AdvancedComboBox(self, parent)
            advComboBox.comboBox.addItems(confiningChoices)
            advComboBox.button.clicked.connect(lambda: self.onAdvBtnClick(advComboBox))
            advComboBox.comboBox.currentIndexChanged['QString'].connect( lambda val, sender=advComboBox:self.onIndexChanged(val, sender)) 
            return advComboBox            
            
        if(self.editor_type == Property.COLOR_EDITOR):
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
        if(self.editor_type == None): return False
        
        if(self.editor_type == Property.COMBO_BOX_EDITOR):      
            index = editor.findText(val)
            editor.setCurrentIndex(index)
            return True
            
        if(self.editor_type == Property.ADVANCED_COMBO_BOX):      
            index = editor.comboBox.findText(val)
            editor.comboBox.setCurrentIndex(index)
            return True
            
        if(self.editor_type == Property.ADVANCED_EDITOR): 
            editor.text = val
            return True
            
        if(self.editor_type == Property.COLOR_EDITOR):
            editor.color = val
            return True; 

        if(self.editor_type == Property.IMAGE_EDITOR):
            if(val != None):
                editor.icon = val['icon']
                editor.text = val['url']
                editor.img = val['img']
            return True;
 
        return False;  
            
    def editorData(self, editor):

        if(self.editor_type == None): return False

        if(self.editor_type == Property.ADVANCED_EDITOR):
            return editor.text
            
        if(self.editor_type == Property.CHECKBOX_EDITOR):
            return True  
            
        if(self.editor_type == Property.COMBO_BOX_EDITOR):
            return editor.currentText()
            
        if(self.editor_type == Property.ADVANCED_COMBO_BOX):
            return editor.comboBox.currentText()   
            
        if(self.editor_type == Property.COLOR_EDITOR):  
            return editor.color
            
        if(self.editor_type == Property.IMAGE_EDITOR):  
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
