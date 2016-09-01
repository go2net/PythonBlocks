from PyQt4 import  QtCore, QtGui
from components.propertyeditor.Property import Property
from components.RestrictFileDialog import RestrictFileDialog
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class QPropertyModel(QtCore.QAbstractItemModel):
    def __init__(self, parent):
        super(QPropertyModel, self).__init__(parent)
        self.rootItem = Property("Root", "Root", 0, None);   
  
    def index (self,  row, column, parent):
        parentItem = self.rootItem;
        
        if (parent.isValid()):
            parentItem = parent.internalPointer()
            
        if (row >= parentItem.childCount() or row < 0):
            return QtCore.QModelIndex();      

        return self.createIndex(row, column, parentItem.child(row)) 
  
    def getIndexForNode(self, node):
        return self.createIndex(node.row(), 1, node)    
  
    def getPropItem(self,  name,  parent=None):
        if(parent == None):
            parent = self.rootItem
        for item in parent.childItems:
            if(item.name == name):
                return item
                
        return None
  
    def headerData (self,  section, orientation, role) :
    
        if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole) :
            if (section == 0) :
               return "Property"
            elif (section == 1) :
               return "Value"
               
        return None # QtCore.QVariant();

    def flags (self,  index ):
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

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()

        parentItem = childItem.parentItem
        
        if parentItem == None or parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.childCount(), 0, parentItem)

    def rowCount ( self,  parent ):
        parentItem = self.rootItem;
        if (parent.isValid()):
            parentItem = parent.internalPointer()
        return len(parentItem.childItems)

    def columnCount (self,  parent):
        return 2

    def data (self,  index, role):
        if (not index.isValid()):
            return None

        item = index.internalPointer()

        if(item.editor_type == Property.IMAGE_EDITOR):
            if (index.column() == 0) and (
                role == QtCore.Qt.ToolTipRole or
                role == QtCore.Qt.DecorationRole or
                role == QtCore.Qt.DisplayRole or
                role == QtCore.Qt.EditRole):
                return item.label.replace('_', ' ');            
            if (index.column() == 1):
                if(role == QtCore.Qt.DecorationRole):
                    if(item.value['icon'] != None and not item.value['icon'].isNull()):
                        return item.value['icon'].scaled(18, 18)
                    else:
                        return None
                        
                if(role == QtCore.Qt.DisplayRole):
                    return item.value['url'] 
                if(role == QtCore.Qt.EditRole):
                    return item.value            
        else:
            if(role == QtCore.Qt.ToolTipRole or
               role == QtCore.Qt.DecorationRole or
               role == QtCore.Qt.DisplayRole or
               role == QtCore.Qt.EditRole):
                if (index.column() == 0):
                    return item.label.replace('_', ' ');
                if (index.column() == 1):
                    return item.value
        
        if(role == QtCore.Qt.BackgroundRole):
            if (item.isRoot()): 
                return QtGui.QApplication.palette("QTreeView").brush(QtGui.QPalette.Normal, QtGui.QPalette.Button).color();

        return None

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows)
        self.endInsertRows()

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    # edit methods
    def setData(self, index, value, role = QtCore.Qt.EditRole):

        if (index.isValid() and role == Qt.EditRole):
            item = index.internalPointer()
            item.setValue(value)
            self.dataChanged.emit(index, index) 
            return True;

        return False;

    def getModuleFuncList(self, module_name):
        import inspect
        from importlib import import_module
        func_list = []
        
        if(module_name != ''):            
            all_functions = inspect.getmembers(import_module(module_name), inspect.isfunction)       
            for function in all_functions:
                func_list.append(function[0])        
    
        return func_list
    
    def getModuleName(self, editor):
            
        dlg = RestrictFileDialog(None)
        dlg.setDirectory('.')
        dlg.setWindowTitle( 'Choose module file' )
        dlg.setViewMode( QFileDialog.Detail )
        dlg.setNameFilters( [self.tr('All python files(*.py)'), self.tr('All Files (*)')] )
        dlg.setDefaultSuffix( '.py' ) 
        dlg.setTopDir('.')
        
        if (dlg.exec_()):
            fileName = dlg.getRelatedPath()
            fileName = fileName.replace('.py', '')
            module_name = fileName.replace('/', '.')
            
            self.properties['module_name'].setValue(module_name)            
            module_name_index = self.getIndexForNode(self.properties['module_name']) 
            self.dataChanged.emit(module_name_index, module_name_index) 
            
            self.properties['function_name'].editorType = Property.COMBO_BOX_EDITOR
            self.properties['function_name'].propertyData = self.getModuleFuncList(module_name)
            function_name_index = self.getIndexForNode(self.properties['function_name'])            
            self.dataChanged.emit(function_name_index, function_name_index) 
