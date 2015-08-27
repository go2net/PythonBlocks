from PyQt4 import  QtCore, QtGui
from components.propertyeditor.Property import Property
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class QPropertyModel(QtCore.QAbstractItemModel):
    def __init__(self, parent):
        super(QPropertyModel, self).__init__(parent)
        self.m_rootItem = Property("Root",0, None);   
  
    def index (self,  row, column, parent):
        parentItem = self.m_rootItem;
        if (parent.isValid()):
            parentItem = parent.internalPointer();    
        if (row >= len(parentItem.children()) or row < 0):
            return QtCore.QModelIndex();      

        return self.createIndex(row, column, parentItem.children()[row])    
  
    def getIndexForNode(self, node):
        node_row =  node.row()
        if(node.parent() == None):
            paretn_index = QtCore.QModelIndex()
        else:
            paretn_index = self.getIndexForNode(node.parent())
        print(paretn_index)    
        return self.index(node_row, 0, paretn_index)
  
    def headerData (self,  section, orientation, role) :
    
        if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole) :
            if (section == 0) :
               return "Property"
            elif (section == 1) :
               return "Value"
               
        return None # QtCore.QVariant();

    def flags (self,  index ) :
        if (not index.isValid()):
            return QtCore.Qt.ItemIsEnabled;
        
        item = index.internalPointer();
        
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEnabled |  QtCore.Qt.ItemIsSelectable 
            
        # only allow change of value attribute
        if (item.isRoot()):
            return  QtCore.Qt.ItemIsEnabled;  
        elif (item.readOnly):
            return  QtCore.Qt.ItemIsDragEnabled 
        else:
            return  QtCore.Qt.ItemIsDragEnabled |  QtCore.Qt.ItemIsEnabled |  QtCore.Qt.ItemIsEditable;

    def parent ( self,  index ) :

        if (not index.isValid()):
            return QtCore.QModelIndex()

        childItem = index.internalPointer();
        parentItem = childItem.parent();

        if (not parentItem or parentItem == self.m_rootItem):
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem);

    def rowCount ( self,  parent ):
        parentItem = self.m_rootItem;
        if (parent.isValid()):
            parentItem = parent.internalPointer()
        return len(parentItem.children())


    def columnCount (self,  parent):
        return 2

    def data (self,  index, role):
        if (not index.isValid()):
            return None

        item = index.internalPointer();

        if(role == QtCore.Qt.ToolTipRole or
           role == QtCore.Qt.DecorationRole or
           role == QtCore.Qt.DisplayRole or
           role == QtCore.Qt.EditRole):
            if (index.column() == 0):
                return item.objectName().replace('_', ' ');
            if (index.column() == 1):
                return item.value(role);
          
        if(role == QtCore.Qt.BackgroundRole):
            if (item.isRoot()): 
                return QtGui.QApplication.palette("QTreeView").brush(QtGui.QPalette.Normal, QtGui.QPalette.Button).color();

        return None

    # edit methods
    def setData(self, index, value, role = QtCore.Qt.EditRole):

        if (index.isValid() and role == Qt.EditRole):
            item = index.internalPointer()
            item.setValue(value)
            self.dataChanged.emit(index, index) 
            return True;

        return False;

