from PyQt4 import  QtCore, QtGui
from components.propertyeditor.Property import Property
from components.RestrictFileDialog import RestrictFileDialog
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,  os

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
        for row in range(rows):
            success = parentItem.insertChild(position+row) != None
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

        return False

    def import_module_from_file(self, full_path_to_module):
        """
        Import a module given the full path/filename of the .py file

        Python 3.4

        """
        module = None

        # Get module name and path from full path
        module_dir, module_file = os.path.split(full_path_to_module)
        module_name, module_ext = os.path.splitext(module_file)
            
        if(sys.version_info >= (3,4)):    
            import importlib
            # Get module "spec" from filename
            spec = importlib.util.spec_from_file_location(module_name,full_path_to_module)
            module = spec.loader.load_module()
        else:
            import imp
            module = imp.load_source(module_name,full_path_to_module)
            
        return module
        
    def getModuleFuncList(self, module_name):
        import inspect
        func_list = []
        if(module_name != ''): 
            try:
                module_name = os.getcwd() + '\\' + module_name
                module = self.import_module_from_file(module_name)
                all_functions = inspect.getmembers(module, inspect.isfunction) 
                for function in all_functions:
                    func_list.append(function[0]) 
            except:
                pass
    
        return func_list
    
    def getModuleName(self, editor):
        
        module_name = QFileDialog.getOpenFileName(None, 'Open File', '.', "All file(*.*);;Python (*.py)")
        module_name = os.path.relpath(module_name, os.getcwd())

        if (module_name == ''): return
        
        prop_root = self.getPropItem('properties')
        module_name_prop= self.getPropItem('module_name', prop_root)
        
        module_name_prop.setValue(module_name)
        module_name_index = self.getIndexForNode(module_name_prop) 
        self.dataChanged.emit(module_name_index, module_name_index)
        
        function_name_prop= self.getPropItem('function_name', prop_root)
        function_name_prop.editor_type = Property.COMBO_BOX_EDITOR
        
        function_name_prop.editor_data = self.getModuleFuncList(module_name)
        function_name_index = self.getIndexForNode(function_name_prop)            
        self.dataChanged.emit(function_name_index, function_name_index) 
