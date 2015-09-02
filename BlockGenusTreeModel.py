#!/usr/bin/env python

from components.propertyeditor.QPropertyModel import  QPropertyModel
from components.propertyeditor.Property import Property
from ConnectorsInfoWnd import ConnectorsInfoWnd
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class BlockGenusTreeModel(QPropertyModel):
  
    def __init__(self, mainWnd, genus, langDefLocation, parent=None):
        from blocks.BlockGenus import BlockGenus
        super(BlockGenusTreeModel, self).__init__(parent)
        self.genus = genus
        self.tmpGenus = BlockGenus(genus.genusName, '__previewGenus__')
        self.properties = {}
        self.mainWnd = mainWnd
        self.langDefLocation = langDefLocation
        self.setupModelData(self.tmpGenus, self.m_rootItem)

    def setupModelData(self, tmpGenus, parent):
        parents = [parent]
        self.showBlock(tmpGenus)
        
        #columnData = ['A','B']  
        #print(genusNode.attrib)
        #
        self.properties['genusName'] = Property('Genus Name', tmpGenus.genusName, parents[-1])    
        self.properties['kind'] = Property('Genus Kind', tmpGenus.kind, parents[-1], Property.COMBO_BOX_EDITOR, ['command', 'data', 'function', 'param','procedure','variable'])
        self.properties['initLabel'] = Property('Init Label', tmpGenus.initLabel, parents[-1])
        self.properties['labelPrefix'] = Property('Label Prefix', tmpGenus.labelPrefix, parents[-1])
        self.properties['labelSuffix'] = Property('Label Suffix', tmpGenus.labelSuffix, parents[-1])    
        self.properties['color'] = Property('Color',tmpGenus.color , parents[-1], Property.COLOR_EDITOR)
        self.properties['isStarter'] = Property('Starter', tmpGenus.isStarter, parents[-1])        

        
        self.properties['isTerminator'] = Property('Terminator', tmpGenus.isTerminator, parents[-1]) 
        
        self.properties['connectors'] = Property('Connectors','', parents[-1],Property.ADVANCED_EDITOR)    

        plug_index = 0
        socket_index = 0
        
        self.all_connectors = []
        
        if tmpGenus.plug != None:
            self.properties['Left #'+str(plug_index)]  = Property('Left #'+str(plug_index), '',  self.properties['connectors'])
            self.fillConnectInfo(tmpGenus.plug,self.properties['Left #'+str(plug_index)] )
            
        for connector in tmpGenus.sockets:
            self.properties['Right #'+str(socket_index)] = Property('Right #'+str(socket_index), '', self.properties['connectors'] ) 
            self.fillConnectInfo(connector, self.properties['Right #'+str(socket_index)] )
            socket_index += 1
            
        self.properties['connectors'].onAdvBtnClick = self.onShowConnectorsInfo

        self.lang_root = Property('Language','', parents[-1],Property.ADVANCED_EDITOR) 
        
        module_name = ''
        function_name = ''
        
        for key in tmpGenus.properties:
            if(key == 'module_name'):
                module_name = tmpGenus.properties['module_name']
            elif(key == 'function_name'):
                function_name = tmpGenus.properties['function_name'] 
                
            else:
                Property(key,tmpGenus.properties[key], self.lang_root)
        
        self.properties['module_name'] = Property('module',module_name, self.lang_root,Property.ADVANCED_EDITOR)
        self.properties['module_name'].onAdvBtnClick = self.getModuleName
        
        self.properties['function_name'] = Property('function',function_name, self.lang_root,Property.COMBO_BOX_EDITOR , self.getModuleFuncList(module_name))


    def fillConnectInfo(self,  socket,  parent):
        Property('label', socket.label,parent)
        Property('kind', socket.kind,parent,  Property.COMBO_BOX_EDITOR, ['socket', 'plug'])
        Property('type', socket.type,parent, Property.COMBO_BOX_EDITOR, ['boolean','cmd','number','poly', 'poly-list', 'string'])

    def onShowConnectorsInfo(self,  editor):

        dlg = ConnectorsInfoWnd(self, self.tmpGenus)
        dlg.exec_()

    def setData(self, index, value, role):

        ret = super(BlockGenusTreeModel, self).setData(index, value, role)
        if(ret == True):
            item = index.internalPointer()
            property_name = item.objectName()

            if(property_name == 'Color'):
                self.tmpGenus.color = value
            
            if(property_name == 'Genus Kind'):
                self.tmpGenus.kind = value

            if(property_name == 'Init Label'):
                self.tmpGenus.initLabel = value

            if(property_name == 'Label Prefix'):
                self.tmpGenus.labelPrefix = value        

            if(property_name == 'Label Suffix'):
                self.tmpGenus.labelSuffix = value

            if(property_name == 'Starter'):
                self.tmpGenus.isStarter = value        

            if(property_name == 'Terminator'):
                self.tmpGenus.isTerminator = value     

            if(property_name == 'module'):
                self.tmpGenus.properties['module_name'] = value
                
            if(property_name == 'function'):
                self.tmpGenus.properties['function_name'] = value  

            if(self.tmpGenus.plug != None and item.parent()  == self.properties['Left #0'] ):
                self.setConnectorProp(self.tmpGenus.plug,property_name, value )
            
            socket_index = 0
            for socket in self.tmpGenus.sockets:
                if(item.parent() == self.properties['Right #'+str(socket_index)] ):
                    self.setConnectorProp(socket,property_name, value )
                    break
                socket_index += 1

        self.showBlock(self.tmpGenus)

    
        if(self.tmpGenus == self.genus): 
            print('self.tmpGenus == self.genus')
            self.mainWnd.wndApplyGenus.hide()
        else:
            print('self.tmpGenus != self.genus')
            self.mainWnd.wndApplyGenus.show()
            
        return ret    
    def setConnectorProp(self, connector, property_name, value):
        tt = 'connector.'+property_name+'=\'' + str(value)+'\''
        print(tt)
        exec(tt)

    def showBlock(self, genus):
        from blocks.Block import Block
        from blocks.FactoryRenderableBlock import FactoryRenderableBlock
        from PyQt4.QtCore import Qt 
        
        if(genus == None): return        

        block = Block.createBlockFromID(None, genus.genusName)
        
        preview_wnd_layout  = self.mainWnd.wndPreview.layout()        

        #for i in reversed(range(preview_wnd_layout.count())):
        #    preview_wnd_layout.itemAt(i).widget().setParent(None)
        
        for i in reversed(range(preview_wnd_layout.count())):
            widget = preview_wnd_layout.itemAt(i).widget()
            widget.setParent(None)
            widget.deleteLater()
            
        factoryRB = FactoryRenderableBlock.from_block(None, block)
        #factoryRB.setParent(self.mainWnd.wndPreview)
        #print('%d:%d'%(factoryRB.getBlockWidth(), factoryRB.getBlockHeight()))
        factoryRB.setFixedSize(factoryRB.width(), factoryRB.height())
        preview_wnd_layout.addWidget(factoryRB, Qt.AlignCenter); 
    
        pass 
