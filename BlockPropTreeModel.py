#!/usr/bin/env python

from components.propertyeditor.QPropertyModel import  QPropertyModel
from components.propertyeditor.Property import Property
from components.RestrictFileDialog import RestrictFileDialog
from ConnectorsInfoWnd import ConnectorsInfoWnd
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []
     
    def columnCount(self):
        return len(self.itemData)
      
    def childCount(self):
        return len(self.childItems)
      
    def child(self, row):
        return self.childItems[row]
      
    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None
          
    def parent(self):
        return self.parentItem
        
    def appendChild(self, item):
        self.childItems.append(item)

class BlockPropTreeModel(QPropertyModel):

    def __init__(self, mainWnd, rb, parent=None):
        super(BlockPropTreeModel, self).__init__(parent)
        self.rb = rb
        self.block = rb.getBlock()
        self.properties = {}
        self.mainWnd = mainWnd
        self.rootItem = TreeItem(("Property", "Value"))
        self.setupModelData(rb, self.m_rootItem)
        self.lang_root = None
        
    def setupModelData(self, rb, parent):
        parents = [parent]

        self.properties['genusName'] = Property('Genus Name', self.block.getGenusName(), parents[-1])    
        self.properties['genusName'].readOnly = True

        self.properties['label'] = Property('Label', self.block.getBlockLabel(), parents[-1])
        self.properties['label'].readOnly = True

        self.lang_root = Property('Language','', parents[-1],Property.ADVANCED_EDITOR) 
        
        #for key in self.block.properties:
        #    self.properties[key] = Property(key,self.block.properties[key], self.lang_root)

        module_name = ''
        if( 'module_name' in self.block.properties):
            module_name = self.block.properties['module_name'] 
        elif( 'module_name' in self.block.getGenus().properties):
            module_name = self.block.getGenus().properties['module_name']            
        
        self.properties['module_name'] = Property('module',module_name, self.lang_root,Property.ADVANCED_EDITOR)
        self.properties['module_name'].onAdvBtnClick = self.getModuleName
    
        function_name = ''
        if( 'function_name' in self.block.properties):
            function_name = self.block.properties['function_name'] 
        elif( 'function_name' in self.block.getGenus().properties):
            function_name = self.block.getGenus().properties['function_name']
        
        self.properties['function_name'] = Property('function',function_name, self.lang_root,Property.COMBO_BOX_EDITOR , self.getModuleFuncList(module_name))
                
    def getModuleFuncList(self, module_name):
        import inspect
        from importlib import import_module
        all_functions = inspect.getmembers(import_module(module_name), inspect.isfunction)       
        
        func_list = []
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

        
    def onShowConnectorsInfo(self):

        dlg = ConnectorsInfoWnd(self.mainWnd, self.all_connectors)
        dlg.exec_()
        print('onShowConnectorsInfo')

    def setData(self, index, value, role):
        ret = super(BlockPropTreeModel, self).setData(index, value, role)
        if(ret == True):
            item = index.internalPointer()
            property_name = item.objectName()
            
            print(property_name), print(value)
            if(property_name == 'module'):
                self.block.properties['module_name'] = value
                
            if(property_name == 'function'):
                self.block.properties['function_name'] = value  
            
            print(self.block.properties)
        return ret
