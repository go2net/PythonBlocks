#!/usr/bin/env python

from components.propertyeditor.QPropertyModel import  QPropertyModel
from components.propertyeditor.Property import Property
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

    def setupModelData(self, rb, parent):
        parents = [parent]

        #columnData = ['A','B']  
        #print(genusNode.attrib)
        #
        self.properties['genusName'] = Property('Genus Name', self.block.getGenusName(), parents[-1])    
        self.properties['genusName'].readOnly = True

        #self.properties['kind'] = Property('Genus Kind', genus.kind, parents[-1], Property.COMBO_BOX_EDITOR, ['command', 'data', 'function', 'param','procedure','variable'])
        self.properties['label'] = Property('Label', self.block.getBlockLabel(), parents[-1])
        self.properties['label'].readOnly = True
         
        #self.properties['labelPrefix'] = Property('Label Prefix', genus.labelPrefix, parents[-1])
        #self.properties['labelSuffix'] = Property('Label Suffix', genus.labelSuffix, parents[-1])    
        #self.properties['color'] = Property('Color',genus.color , parents[-1], Property.COLOR_EDITOR)
        #self.properties['isStarter'] = Property('Starter', genus.isStarter, parents[-1]) 
        #self.properties['isTerminator'] = Property('Terminator', genus.isTerminator, parents[-1]) 
        #self.properties['connectors'] = Property('Connectors','', parents[-1],Property.ADVANCED_EDITOR)    

        #self.all_connectors = genus.sockets

        #plug_index = 0
        #socket_index = 0

        #if genus.plug != None:
        #  Property('Plug #'+str(plug_index), '',  self.properties['connectors'])

        #for connector in genus.sockets:
          
        #  connector_kind = connector.kind
        #  if(connector_kind == 0):
        #    Property('Socket #'+str(socket_index), '',  self.properties['connectors'])
        #    socket_index += 1
        #  else:
        #    Property('Plug #'+str(plug_index), '',  self.properties['connectors'])
        #    plug_index += 1

        lang_root = Property('Language','', parents[-1],Property.ADVANCED_EDITOR) 
        for key in self.block.properties:
            self.properties[key] = Property(key,self.block.properties[key], lang_root)

        if( 'module_name' not in self.block.properties):
            if( 'module_name' in self.block.getGenus().properties):
                self.properties['module_name'] = Property('module',self.block.getGenus().properties['module_name'], lang_root,Property.ADVANCED_EDITOR)
            else:
                self.properties['module_name'] = Property('module','', lang_root, lang_root,Property.ADVANCED_EDITOR)
            self.properties['module_name'].onAdvBtnClick = self.getModuleName
            
        if( 'function_name' not in self.block.properties):
            if( 'function_name' in self.block.getGenus().properties):
                self.properties['function_name'] = Property('function',self.block.getGenus().properties['function_name'], lang_root)
            else:
                self.properties['function_name'] = Property('function','', lang_root)
          
        #self.properties['connectors'].onAdvBtnClick = self.onShowConnectorsInfo

    def getModuleName(self):
        filename = QFileDialog.getOpenFileName(None, 'Choose module file', '.', "All python files(*.py)")
        
    def onShowConnectorsInfo(self):

        dlg = ConnectorsInfoWnd(self.mainWnd, self.all_connectors)
        dlg.exec_()
        print('onShowConnectorsInfo')

    def setData(self, index, value, role):
        ret = super(BlockPropTreeModel, self).setData(index, value, role)
        if(ret == True):
            item = index.internalPointer()
            property_name = item.objectName()
          
            if(property_name == 'Color'):
                self.genus.color = value
            
            if(property_name == 'Genus Kind'):
                self.genus.kind = value
            
            if(property_name == 'Init Label'):
                self.genus.initLabel = value
            
            if(property_name == 'Label Prefix'):
                self.genus.labelPrefix = value        
            
            if(property_name == 'Label Suffix'):
                self.genus.labelSuffix = value
            
            if(property_name == 'Starter'):
                self.genus.isStarter = value        
            
            if(property_name == 'Terminator'):
                self.genus.isTerminator = value     
            
        return ret
