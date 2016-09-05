#!/usr/bin/env python

from components.propertyeditor.QPropertyModel import  QPropertyModel
from components.propertyeditor.Property import Property
from components.ConnectorsInfoWnd import ConnectorsInfoWnd


class BlockPropTreeModel(QPropertyModel):

    def __init__(self, mainWnd, rb, parent=None):
        super(BlockPropTreeModel, self).__init__(parent)
        self.rb = rb
        self.block = rb.getBlock()
        self.properties = {}
        self.mainWnd = mainWnd
        self.setupModelData(rb, self.rootItem)
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
      
    def onShowConnectorsInfo(self):

        dlg = ConnectorsInfoWnd(self.mainWnd, self.all_connectors)
        dlg.exec_()
        print('onShowConnectorsInfo')

    def setData(self, index, value, role):
        ret = super(BlockPropTreeModel, self).setData(index, value, role)
        if(ret == True):
            item = index.internalPointer()
            property_name = item.objectName()            

            if(property_name == 'module'):
                self.block.properties['module_name'] = value
                
            if(property_name == 'function'):
                self.block.properties['function_name'] = value  

        return ret
