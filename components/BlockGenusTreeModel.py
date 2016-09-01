#!/usr/bin/env python

from components.propertyeditor.QPropertyModel import  QPropertyModel
from components.propertyeditor.Property import Property
from components.ConnectorsInfoWnd import ConnectorsInfoWnd
from components.ImagesInfoWnd import ImagesInfoWnd
from components.FamilyInfoWnd import FamilyInfoWnd

from blocks.BlockGenus import BlockGenus
from blocks.BlockConnector import BlockConnector
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os

class BlockGenusTreeView(QTreeView):
    def __init__(self, parent):
        super(BlockGenusTreeView, self).__init__(parent)
        self.isDirty = False        
        
class BlockGenusTreeModel(QPropertyModel):
  
    def __init__(self, view,  mainWnd, genus, langDefLocation, parent=None):
        from blocks.BlockGenus import BlockGenus
        super(BlockGenusTreeModel, self).__init__(parent)
        self.view = view
        self.genus = genus
        self.tmpGenus = BlockGenus(genus.genusName, '__previewGenus__')
        self.properties = {}
        self.properties['sockets'] = []
        self.mainWnd = mainWnd
        self.mainWnd.btnApply.clicked.connect(self.onApply)
        self.langDefLocation = langDefLocation
        self.setupModelData(self.tmpGenus, self.rootItem)
        self.isDirty = False
        self.popMenu = QMenu(self.view)

    def flags (self,  index ):
        if (not index.isValid()):
            return Qt.ItemIsEnabled;
        
        item = index.internalPointer()
        property_name = item.name

        if property_name == 'Genus Name':
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

        elif item.parent() != None and item.parent().name == 'Img':
            img = item.parent().value()['img']
            if(property_name == 'height'):
                if not img.lockRatio:                
                    return Qt.ItemIsEnabled | Qt.ItemIsEditable;
                else:
                    return Qt.ItemIsEnabled

        return QPropertyModel.flags(self, index)
       
    def setupModelData(self, tmpGenus, parent):
        parents = [parent]
        self.showBlock(tmpGenus)
        
        parent = parents[-1]
        
        ###############
        #      Genus Name          #
        ###############        
        parent.insertChildren(parent.childCount(), 1)        
        prop = parent.child(parent.childCount() -1)
        prop.name = 'genusName'
        prop.label = 'Genus Name'
        prop.value = self.genus.genusName

        ###############
        #      Genus Kind           #
        ###############           
        parent.insertChildren(parent.childCount(), 1)
        prop = parent.child(parent.childCount() -1)
        prop.name = 'kind'
        prop.label = 'Genus Kind'
        prop.value = tmpGenus.kind
        prop.editor_type = Property.COMBO_BOX_EDITOR
        prop.editor_data =  ['command', 'data', 'function', 'param','procedure','variable']

        ###############
        #      Family Name         #
        ###############          
        familyNameList = ['n/a']
        familyName = tmpGenus.familyName
        for name in BlockGenus.families:
            familyNameList.append(name)
            
        if(familyName == ''):
            familyName = 'n/a'

        parent.insertChildren(parent.childCount(), 1)
        prop = parent.child(parent.childCount() -1)
        prop.name = 'familyName'
        prop.label = 'Family Name'
        prop.value = familyName
        prop.editor_type = Property.ADVANCED_COMBO_BOX
        prop.editor_data =  familyNameList
        prop.onAdvBtnClick = self.onShowFamilyInfo
        prop.onIndexChanged = self.onFamilyChanged 

        ###############
        #      Init Label            #
        ###############   
        labelList= []
        if familyName in BlockGenus.families:            
            family = BlockGenus.families[familyName]
            for varName in family:                
                labelList.append(family[varName])  

        parent.insertChildren(parent.childCount(), 1)
        prop = parent.child(parent.childCount() -1)
        prop.name = 'initLabel'
        prop.label = 'Init Label'
        prop.value = tmpGenus.initLabel        
        
        if(labelList != []):
            prop.editor_type = Property.COMBO_BOX_EDITOR
            prop.editor_data =  labelList

        ###############
        #      Label Prefix          #
        ###############  
        parent.insertChildren(parent.childCount(), 1)        
        prop = parent.child(parent.childCount() -1)
        prop.name = 'labelPrefix'
        prop.label = 'Label Prefix'
        prop.value = tmpGenus.labelPrefix
        
        ###############
        #      Label Suffix         #
        ###############  
        parent.insertChildren(parent.childCount(), 1)        
        prop = parent.child(parent.childCount() -1)
        prop.name = 'labelSuffix'
        prop.label = 'Label Suffix'
        prop.value = tmpGenus.labelSuffix
        
        ###############
        #      Color                   #
        ###############  
        parent.insertChildren(parent.childCount(), 1)        
        prop = parent.child(parent.childCount() -1)
        prop.name = 'color'
        prop.label = 'Color'
        prop.value = tmpGenus.color
        prop.editor_type = Property.COLOR_EDITOR
          
        ############
        #      Images         #
        ############
        parent.insertChildren(parent.childCount(), 1)        
        prop = parent.child(parent.childCount() -1)
        prop.name = 'images'
        prop.label = 'Images'
        prop.value = ''
        prop.editor_type = Property.ADVANCED_EDITOR     
        prop.onAdvBtnClick = self.onShowImagesInfo   
        
        self.addImages(prop, tmpGenus)
        
        ############
        #      Connector     #
        ############
        parent.insertChildren(parent.childCount(), 1)        
        connectors_prop = parent.child(parent.childCount() -1)
        connectors_prop.name = 'connectors'
        connectors_prop.label = 'Connectors'
        connectors_prop.value = ''
        connectors_prop.editor_type = Property.CUSTOMER_EDITOR    
        connectors_prop.ui_file = os.path.dirname(os.path.realpath(__file__))+'/connector_prop.ui'
        connectors_prop.signal_slot_maps['btnAddPlug'] = ['clicked', self.onAddPlug, tmpGenus.getInitPlug()==None]
        connectors_prop.signal_slot_maps['btnAddSocket'] = ['clicked', self.onAddSocket]

     
        ############
        #      Starter       #
        ############ 
        connectors_prop.insertChildren(connectors_prop.childCount(), 1)        
        prop = connectors_prop.child(connectors_prop.childCount() -1)
        prop.name = 'isStarter'
        prop.label = 'Starter'
        prop.value = tmpGenus.isStarter

        ############
        #      Terminator   #
        ############ 
        connectors_prop.insertChildren(connectors_prop.childCount(), 1)        
        prop = connectors_prop.child(connectors_prop.childCount() -1)
        prop.name = 'isTerminator'
        prop.label = 'Terminator'
        prop.value = tmpGenus.isTerminator

        ############
        #      Plug             #
        ############         
        if tmpGenus.plug != None:
            connectors_prop.insertChildren(connectors_prop.childCount(), 1)        
            prop = connectors_prop.child(connectors_prop.childCount() -1)
            prop.name = 'plug'
            prop.label = 'Plug'
            prop.value = ''
            prop.data = tmpGenus.plug
            prop.editor_type = Property.CUSTOMER_EDITOR    
            prop.ui_file = os.path.dirname(os.path.realpath(__file__))+'/remove_connector.ui'
            prop.signal_slot_maps['btnRemoveConn'] = ['clicked', self.onDelPlug]

            self.fillConnectInfo(prop, tmpGenus.plug)

        ############
        #      socket      #
        ############         
        for connector in tmpGenus.sockets:
            connectors_prop.insertChildren(connectors_prop.childCount(), 1)        
            prop = connectors_prop.child(connectors_prop.childCount() -1)
            prop.name = 'socket'
            prop.label = 'Socket'
            prop.value = ''
            prop.data = connector
            prop.editor_type = Property.CUSTOMER_EDITOR    
            prop.ui_file = os.path.dirname(os.path.realpath(__file__))+'/remove_connector.ui'
            prop.signal_slot_maps['btnRemoveConn'] = ['clicked', self.onDelSocket]            
            
            self.fillConnectInfo(prop, connector)

        ###########
        # Properties       #
        ###########
        parent.insertChildren(parent.childCount(), 1)        
        props_root = parent.child(parent.childCount() -1)
        props_root.name = 'properties'
        props_root.label = 'Properties'
        props_root.value = ''
        props_root.editor_type = Property.ADVANCED_EDITOR    
        
        ###########
        #      module       #
        ###########       
        module_name= tmpGenus.properties['module_name']
        props_root.insertChildren(props_root.childCount(), 1)        
        prop = props_root.child(props_root.childCount() -1)
        prop.name = 'module_name'
        prop.label = 'module'
        prop.value = module_name
        prop.editor_type = Property.ADVANCED_EDITOR           
        prop.onAdvBtnClick = self.getModuleName   
        
        ###########
        #      function       #
        ###########       
        props_root.insertChildren(props_root.childCount(), 1)        
        prop = props_root.child(props_root.childCount() -1)
        prop.name = 'function_name'
        prop.label = 'function'
        prop.value = tmpGenus.properties['function_name']
        prop.editor_type = Property.ADVANCED_EDITOR           
        prop.onAdvBtnClick = self.getModuleName  
        prop.editor_data = self.getModuleFuncList(module_name)

        ###########
        #      misc  prop   #
        ###########   
        for key in tmpGenus.properties:
            if(key != 'module_name' and key != 'function_name'):
                props_root.insertChildren(props_root.childCount(), 1)        
                prop = props_root.child(props_root.childCount() -1)
                prop.name = key
                prop.label = key
                prop.value = tmpGenus.properties[key]
    
    def insertChild(self,  index, name,  label,  value):
        
        item = index.internalPointer()        
        row = item.childCount()

        if not self.insertRow(row, index):
            return None

        child = item.child(row)
        child.name = name
        child.label = label
        child.value = value
        
        label_index = self.index(row, 0, index)
        self.setData(label_index, label, Qt.EditRole)

        val_index = self.index(row, 1, index)
        self.setData(val_index, value, Qt.EditRole)

        return child
    
    def onAddPlug(self,  editor,  item):
        index = self.getIndexForNode(item)
        isTerminator_item = self.getPropItem('isTerminator', item)
        row = isTerminator_item.row()+1
        
        if not self.insertRow(row, index):
            return 
            
        initKind = 'plug'
        initType = 'string'
        idConnected = ""
        label = "";
        isExpandable = False;
        isLabelEditable = True;
        position = 0  
        
        plug = BlockConnector(
            initKind,
            initType,
            position, 
            label, 
            isLabelEditable,
            isExpandable,
            idConnected);    
            
        plug_item = item.child(row)
        plug_item.name = 'plug'
        plug_item.label = 'Plug'
        plug_item.value = plug
        plug_item.editor_type = Property.CUSTOMER_EDITOR
        plug_item.ui_file = os.path.dirname(os.path.realpath(__file__))+'/remove_connector.ui'
        plug_item.signal_slot_maps['btnRemoveConn'] = ['clicked', self.onDelPlug]  
        plug_item.data = plug
        prop_label_index = self.index(row, 0, index)
        self.setData(prop_label_index, plug_item.label, Qt.EditRole)
        
        prop_val_index = self.index(row, 1, index)
        self.setData(prop_val_index, plug_item.value, Qt.EditRole)        
        
        prop = self.insertChild(prop_label_index,  'label', 'label',  '')
        prop = self.insertChild(prop_label_index,  'type', 'type',  'string')   
        prop.editor_type = Property.COMBO_BOX_EDITOR   
        prop.editor_data = ['boolean','cmd','number','poly', 'poly-list', 'string'] 
        prop.signal_slot_maps['btnAddPlug'] = ['clicked', self.onAddPlug, False]
        
    def onDelPlug(self,  editor,  item):
        index = self.getIndexForNode(item)
        self.removeRow(index.row(), index.parent())
        self.tmpGenus.plug = None
        self.chkDirty()    
        self.showBlock(self.tmpGenus)        
        item.parentItem.signal_slot_maps['btnAddPlug'] = ['clicked', self.onAddPlug, True]
        
    def onAddSocket(self,  editor,  item):
        index = self.getIndexForNode(item)
        row = item.childCount()
        if not self.insertRow(row, index):
            return 
            
        initKind = 'socket'
        initType = 'string'
        idConnected = ""
        label = "";
        isExpandable = False;
        isLabelEditable = True;
        position = 0  
        
        socket = BlockConnector(
            initKind,
            initType,
            position, 
            label, 
            isLabelEditable,
            isExpandable,
            idConnected);    
            
        socket_item = item.child(row)
        socket_item.name = 'socket'
        socket_item.label = 'Socket'
        socket_item.value = socket
        socket_item.editor_type = Property.CUSTOMER_EDITOR
        socket_item.ui_file = os.path.dirname(os.path.realpath(__file__))+'/remove_connector.ui'
        socket_item.signal_slot_maps['btnRemoveConn'] = ['clicked', self.onDelSocket]  
        socket_item.data = socket
        
        socket_index = self.getIndexForNode(socket_item)
        self.setData(socket_index, socket_item.data, Qt.EditRole)
        
        #prop_label_index = self.index(row, 0, index)
        #self.setData(prop_label_index, socket_item.label, Qt.EditRole)
        
        #prop_val_index = self.index(row, 1, index)
        #self.setData(prop_val_index, socket_item.value, Qt.EditRole) 
        
        socket_item.insertChildren(socket_item.childCount(), 1)
        prop = socket_item.child(socket_item.childCount() -1)
        prop.name = 'label'
        prop.label = 'label'
        prop.value = ''
   
        socket_item.insertChildren(socket_item.childCount(), 1)
        prop = socket_item.child(socket_item.childCount() -1)
        prop.name = 'type'
        prop.label = 'type'
        prop.value = 'string'
        prop.editor_type = Property.COMBO_BOX_EDITOR   
        prop.editor_data = ['boolean','cmd','number','poly', 'poly-list', 'string']


    def onDelSocket(self,  editor,  item):
        index = self.getIndexForNode(item)
        self.removeRow(index.row(), index.parent())
        self.tmpGenus.sockets.remove(item.data)
        self.chkDirty()    
        self.showBlock(self.tmpGenus)
        
    def onShowFamilyInfo(self,  editor):
        dlg = FamilyInfoWnd(self, self.tmpGenus)
        retCode = dlg.exec_()
        
        if retCode == QDialog.Accepted:
            BlockGenus.families = {}
            editor.comboBox.clear()
            editor.comboBox.addItem('n/a')
            for familyName in dlg.allFamilyNames():
                editor.comboBox.addItem(familyName)
                BlockGenus.families[familyName] = []
                for variName in dlg.families[familyName]:
                    BlockGenus.families[familyName].append(variName)    
   
    def onFamilyChanged(self, familyName, sender,  item):
        initLabel_Item = self.getPropItem('initLabel')
        print(initLabel_Item)
        if(initLabel_Item == None): return        
        if familyName != 'n/a' and familyName in BlockGenus.families:
            initLabel_Item.editor_type = Property.COMBO_BOX_EDITOR        
            var_list = []
            for key in BlockGenus.families[familyName]:
                var_list.append(BlockGenus.families[familyName][key])
            #print(var_list)
            initLabel_Item.editor_data = var_list
        else:
            initLabel_Item.editor_type = None
            initLabel_Item.editor_data = None           
    
    def addImages(self,  imgs_root, genus):
        for img_index in range(len(self.tmpGenus.blockImages)):           
            self.addImage(imgs_root, img_index, self.tmpGenus.blockImages[img_index])
   
    def addImage(self,  imgs_root, img_index,  img):
        url = QUrl(img.url) 
        if(img.icon != None and not img.icon.isNull() and img.width() > 0 and img.height() > 0): 
            icon = img.icon
        else:
            icon = self.loadImage(url)
            img.icon = icon
            
        image_data = {}
        image_data['icon'] = icon
        image_data['url'] = url.toString()
        image_data['img'] = img
 
        img_root = Property('Img',image_data, imgs_root,Property.IMAGE_EDITOR) 
        img_root.onAdvBtnClick = self.loadFromFile
        img_root.onMenuBtnClick = self.onShowImgSelMenu

        self.properties['Img #'+str(img_index)] = img_root
        self.properties['location'] = Property('location', img.location, img_root,Property.COMBO_BOX_EDITOR, ['CENTER', 'EAST', 'WEST', 'NORTH', 'SOUTH', 'SOUTHEAST', 'SOUTHWEST', 'NORTHEAST', 'NORTHWEST'] )
        self.properties['lock_ratio'] = Property('lock ratio',img.lockRatio, img_root  )
        self.properties['width'] = Property('width',img.width(), img_root  )
        self.properties['height'] = Property('height',img.height(),img_root)
        
        self.properties['editable'] = Property('editable', img.isEditable, img_root )
        self.properties['wraptext'] = Property('wraptext', img.wrapText, img_root )    
    
    def fillConnectInfo(self, parent,  connector):
        ###############
        #             label             #
        ###############             
        parent.insertChildren(parent.childCount(), 1)
        prop = parent.child(parent.childCount() -1)
        prop.name = 'label'
        prop.label = 'label'
        prop.value = connector.label
        
        ###############
        #             label             #
        ###############             
        parent.insertChildren(parent.childCount(), 1)
        prop = parent.child(parent.childCount() -1)
        prop.name = 'type'
        prop.label = 'type'
        prop.value = connector.type               
        prop.editor_type = Property.COMBO_BOX_EDITOR   
        prop.editor_data = ['boolean','cmd','number','poly', 'poly-list', 'string']
        
    def onLoadImageFromFile(self,  editor):        
        editor.text = QFileDialog.getOpenFileName(None, 'Open File', '.', "All file(*.*);;JPG (*.jpg);;PNG(*.png);;GIF(*.gif);;BMP(*.bmp)")

        blockImageIcon = self.loadImageFromUrl(QUrl.fromLocalFile(editor.text))
        editor.icon = blockImageIcon
    
    def loadImage(self, url):
        from blocks.BlockImageIcon import FileDownloader
        
        icon = QPixmap()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            downloader = FileDownloader(url)
            imgData = downloader.downloadedData()
            icon.loadFromData(imgData)
        finally:
            QApplication.restoreOverrideCursor()
            
        return icon
    
    def onShowImagesInfo(self, editor):
        dlg = ImagesInfoWnd(self, self.tmpGenus)
        retCode = dlg.exec_()
        
        if retCode == QDialog.Accepted:
            root_index = self.getIndexForNode(self.imgs_root)
            
            # Remove rows from view
            self.removeRows(0, len(self.imgs_root.children()),root_index)
            self.imgs_root.children().clear()
            
            # Remove rows from model
            for item in self.imgs_root.children():
                item.setParent(None)
            
            # Clear blockImages
            self.tmpGenus.blockImages = []
            for img in dlg.blockImages:
                self.tmpGenus.blockImages.append(img)

            self.addImages(self.imgs_root, self.tmpGenus)

            #self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), root_index, root_index) 
     
    def onShowImgSelMenu(self,  editor):
        
        self.popMenu.clear() 

        choose_file_action = self.popMenu.addAction('Choose file')
        choose_file_action.triggered.connect(lambda: self.loadFromFile(editor))
        
        from_url_action = self.popMenu.addAction('From URL')
        from_url_action.triggered.connect(lambda: self.loadFromURL(editor))
        
        self.popMenu.exec_(QCursor().pos())
    
    def loadFromFile(self, editor):
        filename = QFileDialog.getOpenFileName(None, 'Open File', '.', "All file(*.*);;JPG (*.jpg);;PNG(*.png);;GIF(*.gif);;BMP(*.bmp)")
        if not filename:
            return
            
        url = QUrl.fromLocalFile(filename)    
        editor.text = url.toString()    
        editor.icon = self.loadImage(url)

        return filename
        
    def loadFromURL(self, editor):
        input, ok = QInputDialog.getText(self.mainWnd, 'URL', 'Enter url:')
        if ok:  
            url = QUrl(input)
            #url = QUrl.fromLocalFile(filename)
            editor.text = url.toString()
            editor.icon = self.loadImage(url)
        
    def onShowConnectorsInfo(self,  editor):
        dlg = ConnectorsInfoWnd(self, self.tmpGenus)
        retCode = dlg.exec_()
        if retCode == QDialog.Accepted:
            pass
            
    def setData(self, index, value, role):
        
        if role != Qt.EditRole:
            return False

        item = index.internalPointer()
        result = item.setData(index.column(), value) 
        
        if(result == True):
            item = index.internalPointer()
            property_name = item.name
            
            if(item.parent() == self.rootItem and hasattr(self.tmpGenus, property_name)):
                setattr(self.tmpGenus,property_name, value )
            
            if(property_name == 'familyName'):
                labelList= []
                initLabel_Item = self.getPropItem('initLabel')
                if(initLabel_Item != None):
                    if value in BlockGenus.families:            
                        family = BlockGenus.families[value]
                        for name in family:
                            labelList.append(family[name])    
                        initLabel_Item.editorType = Property.COMBO_BOX_EDITOR
                        initLabel_Item.propertyData = labelList
                    else:
                        initLabel_Item.editorType = None
            elif (property_name == 'Img') :
                img = value['img']
                img.icon = value['icon']
                img.url = value['url']
                
            elif (property_name == 'plug') :
                plug = item.data
                self.tmpGenus.plug = plug
                
            elif (property_name == 'socket') :
                socket = item.data
                if(socket not in self.tmpGenus.sockets):
                    self.tmpGenus.sockets.append(socket)                    
            elif (item.parent() != None and item.parent().name == 'Img'):
                img = item.parent().value()['img'] 
                items = item.parent().children()
                height_item = None
                for item in items:
                    if item.name == 'height':
                        height_item = item
                        break            
                if(property_name == 'location'):
                    img.location = value                    
                elif(property_name == 'editable'):
                    img.isEditable = value                    
                elif(property_name == 'wraptext'):
                    img.wrapText = value                    
                elif(property_name == 'lock ratio'):
                    if(value==True and img.lockRatio != value):
                        if (height_item != None):
                            height = img.width()*img.icon.height()/img.icon.width()
                            height_item.setValue(height)                        
                        img.setSize(img.width(), height, False)
                    else:
                        img.lockRatio = value
                    img.lockRatio = value
                    self.tmpGenus.properties['height'] = img.height
                    
                elif(property_name == 'width'):
                    if (img.lockRatio == True and height_item != None):
                        height = img.width()*img.icon.height()/img.icon.width()
                        height_item.setValue(height)
                    else:
                        height = img.height()                        
                    img.setSize(value, height, False)                                            
                    self.tmpGenus.properties['height'] = img.height
                    
                elif(property_name == 'height'):
                    img.setSize(img.width(),  value)
            elif (item.parent() != None and item.parent().name == 'plug'):    
                if(self.tmpGenus.plug != None):
                    plug = item.parent().data
                    setattr(plug, property_name,  value)
            elif (item.parent() != None and item.parent().name == 'socket'):             
                socket = item.parent().data
                setattr(socket, property_name,  value)
                
            elif (item.parent() != None and item.parent().name == 'Properties'):    
                if(property_name=='module'):
                    self.tmpGenus.properties['module_name'] = value                    
                elif(property_name=='function'):    
                    self.tmpGenus.properties['function_name'] = value
                else:        
                    for key, value in self.tmpGenus.properties.items():
                        if(key == property_name):
                            self.tmpGenus.properties[property_name] = value
                            break
                
        self.showBlock(self.tmpGenus)

        self.chkDirty()    
        
        self.dataChanged.emit(index, index) 

        return result    
        
    def chkDirty(self):
        self.genus.isDirty = (self.genus != self.tmpGenus)
        
        if(not self.genus.isDirty): 
            self.mainWnd.wndApplyGenus.hide()
        else:
            self.mainWnd.wndApplyGenus.show()
            
    def setConnectorProp(self, connector, property_name, value):
        tt = 'connector.'+property_name+'=\'' + str(value)+'\''
        exec(tt)

    def onApply(self):
        self.genus.copyDataFrom(self.tmpGenus)
        self.mainWnd.wndApplyGenus.hide()
        self.genus.isDirty = False

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
            
        self.factoryRB = FactoryRenderableBlock.from_block(None, block)
        self.factoryRB.updateBuffImg()
        #factoryRB.setParent(self.mainWnd.wndPreview)
        #print('%d:%d'%(factoryRB.getBlockWidth(), factoryRB.getBlockHeight()))
        self.factoryRB.setFixedSize(self.factoryRB.width(), self.factoryRB.height())
        preview_wnd_layout.addWidget(self.factoryRB, Qt.AlignCenter); 
    
        pass 
