
from PyQt4 import QtCore

class Property(QtCore.QObject):
  def __init__(self, name, propertyObject, parent):
    super(Property, self).__init__(parent)
    print(propertyObject)
    self.m_propertyObject = propertyObject
    self.setObjectName(name);

  def isRoot(self):
    return self.m_propertyObject == None
    
  def value(self, role=None):
    if (self.m_propertyObject):
      return self.m_propertyObject
    else:
      return None;

  def isReadOnly(self):
    return False
    if( self.m_propertyObject.dynamicPropertyNames().contains( objectName().toLocal8Bit() ) ):
      return false;
    if (self.m_propertyObject and m_propertyObject.metaObject().property(self.m_propertyObject.metaObject().indexOfProperty(qPrintable(objectName()))).isWritable()):
      return false;
    else:
      return true;
