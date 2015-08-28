#!/usr/bin/env python

from components.propertyeditor.QPropertyModel import  QPropertyModel
from components.propertyeditor.Property import Property
from ConnectorsInfoWnd import ConnectorsInfoWnd

class BlockGenusTreeModel(QPropertyModel):
  
    def __init__(self, mainWnd, genus, langDefLocation, parent=None):
        super(BlockGenusTreeModel, self).__init__(parent)
        self.genus = genus
        self.properties = {}
        self.mainWnd = mainWnd
        self.langDefLocation = langDefLocation
        self.setupModelData(genus, self.m_rootItem)

    def setupModelData(self, genus, parent):
        parents = [parent]
        self.mainWnd.showBlock(genus)
        
        #columnData = ['A','B']  
        #print(genusNode.attrib)
        #
        self.properties['genusName'] = Property('Genus Name', genus.genusName, parents[-1])    
        self.properties['kind'] = Property('Genus Kind', genus.kind, parents[-1], Property.COMBO_BOX_EDITOR, ['command', 'data', 'function', 'param','procedure','variable'])
        self.properties['initLabel'] = Property('Init Label', genus.initLabel, parents[-1])
        self.properties['labelPrefix'] = Property('Label Prefix', genus.labelPrefix, parents[-1])
        self.properties['labelSuffix'] = Property('Label Suffix', genus.labelSuffix, parents[-1])    
        self.properties['color'] = Property('Color',genus.color , parents[-1], Property.COLOR_EDITOR)
        self.properties['isStarter'] = Property('Starter', genus.isStarter, parents[-1]) 
        self.properties['isTerminator'] = Property('Terminator', genus.isTerminator, parents[-1]) 
        self.properties['connectors'] = Property('Connectors','', parents[-1],Property.ADVANCED_EDITOR)    

        self.all_connectors = genus.sockets
        
        plug_index = 0
        socket_index = 0
        
        if genus.plug != None:
            Property('Plug #'+str(plug_index), '',  self.properties['connectors'])
        
        for connector in genus.sockets:
          
            connector_kind = connector.kind
            if(connector_kind == 0):
                Property('Socket #'+str(socket_index), '',  self.properties['connectors'])
                socket_index += 1
            else:
                Property('Plug #'+str(plug_index), '',  self.properties['connectors'])
                plug_index += 1 
            
            self.properties['connectors'].onAdvBtnClick = self.onShowConnectorsInfo

        self.lang_root = Property('Language','', parents[-1],Property.ADVANCED_EDITOR) 
        
        module_name = ''
        function_name = ''
        
        for key in genus.properties:
            if(key == 'module_name'):
                module_name = genus.properties['module_name']
            elif(key == 'function_name'):
                function_name = genus.properties['function_name'] 
                
            else:
                Property(key,genus.properties[key], self.lang_root)
        
        self.properties['module_name'] = Property('module',module_name, self.lang_root,Property.ADVANCED_EDITOR)
        self.properties['module_name'].onAdvBtnClick = self.getModuleName
        
        self.properties['function_name'] = Property('function',function_name, self.lang_root,Property.COMBO_BOX_EDITOR , self.getModuleFuncList(module_name))


    def onShowConnectorsInfo(self):

        dlg = ConnectorsInfoWnd(self.mainWnd, self.all_connectors)
        dlg.exec_()
        print('onShowConnectorsInfo')

    def setData(self, index, value, role):
        ret = super(BlockGenusTreeModel, self).setData(index, value, role)
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

            if(property_name == 'module'):
                self.genus.properties['module_name'] = value
                
            if(property_name == 'function'):
                self.genus.properties['function_name'] = value  

            self.mainWnd.showBlock(self.genus)
        return ret

 
