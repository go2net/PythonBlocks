
from PyQt4 import QtCore, QtGui
from components.propertyeditor.ColorCombo import  ColorCombo

class Property(QtCore.QObject):
  COMBO_BOX_EDITOR = 1
  COLOR_EDITOR = 2
  
  def __init__(self, name, obj_value, parent=None, obj_type = None,  obj_data=None):
    super(Property, self).__init__(parent)
    print(parent)
    self.obj_type = obj_type
    self.obj_value = obj_value
    self.obj_data = obj_data
    self.setObjectName(name);

  def isRoot(self):
    return self.obj_value == None
    
  def value(self, role=None):
    if (self.obj_value):
      return self.obj_value
    else:
      return None;

  def setValue(self, val):
    if (self.obj_value != None):
      self.obj_value = val

  def isReadOnly(self):
    return False
    if( self.m_propertyObject.dynamicPropertyNames().contains( objectName().toLocal8Bit() ) ):
      return false;
    if (self.m_propertyObject and m_propertyObject.metaObject().property(self.m_propertyObject.metaObject().indexOfProperty(qPrintable(objectName()))).isWritable()):
      return false;
    else:
      return true;

  def createEditor(self, parent, option):
    editor = None
    if(self.obj_type == None): return None

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
    
  def setEditorData(self, editor, val):
    if(self.obj_type == None): return False
    
    if(self.obj_type == Property.COMBO_BOX_EDITOR):
      index = editor.findData(val)
      editor.setCurrentIndex(index)
      return True
      
    if(self.obj_type == Property.COLOR_EDITOR):
      editor.setColor(val);
      return True;
    else:
      return False;	

  
  def editorData(self, editor):
    print('editorData')
    if(self.obj_type == None): return False
    
    if(self.obj_type == Property.COMBO_BOX_EDITOR):
      return editor.currentText();
      
    if(self.obj_type == Property.COLOR_EDITOR):  
      return editor.color();
    else:
      return None

  
  @QtCore.pyqtSlot(int)
  def currentIndexChanged(self):
      return
      #self.commitData.emit(self.sender())  
