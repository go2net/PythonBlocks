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
        self.setupModelData(self.tmpGenus, self.m_rootItem)
        self.isDirty = False
        self.popMenu = QMenu(self.view)

    def flags (self,  index ):
        if (not index.isValid()):
            return Qt.ItemIsEnabled;
        
        item = index.internalPointer()
        property_name = item.objectName()

        if property_name == 'Genus Name':
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

        elif item.parent() != None and item.parent().objectName() == 'Img':
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
    
        self.properties['genusName'] = Property('Genus Name', self.genus.genusName, parents[-1])         
        self.properties['kind'] = Property('Genus Kind', tmpGenus.kind, parents[-1], Property.COMBO_BOX_EDITOR, ['command', 'data', 'function', 'param','procedure','variable'])
        
        familyNameList = ['n/a']
        familyName = tmpGenus.familyName
        for name in BlockGenus.families:
            familyNameList.append(name)
            
        if(familyName == ''):
            familyName = 'n/a'
            
        self.properties['familyName'] = Property('Family Name', familyName, parents[-1], Property.ADVANCED_COMBO_BOX,familyNameList)             
        self.properties['familyName'].onAdvBtnClick = self.onShowFamilyInfo
        self.properties['familyName'].onIndexChanged = self.onFamilyChanged
        
        labelList= []
        if familyName in BlockGenus.families:            
            family = BlockGenus.families[familyName]
            for varName in family:                
                labelList.append(family[varName])  
        if(labelList != []):
            self.properties['initLabel'] = Property('Init Label', tmpGenus.initLabel, parents[-1], Property.COMBO_BOX_EDITOR,labelList)
        else:
            self.properties['initLabel'] = Property('Init Label', tmpGenus.initLabel, parents[-1])
        
        self.properties['labelPrefix'] = Property('Label Prefix', tmpGenus.labelPrefix, parents[-1])
        self.properties['labelSuffix'] = Property('Label Suffix', tmpGenus.labelSuffix, parents[-1])    
        self.properties['color'] = Property('Color',tmpGenus.color , parents[-1], Property.COLOR_EDITOR)
          
        ############
        #      Image          #
        ############
        self.imgs_root = Property('Images','',  parents[-1],Property.ADVANCED_EDITOR) 
        self.imgs_root.onAdvBtnClick = self.onShowImagesInfo
        self.addImages(self.imgs_root, tmpGenus)
        
        ############
        #      Connector     #
        ############
        self.properties['connectors'] = Property('Connectors','', parents[-1],Property.CUSTOMER_EDITOR)
        self.properties['connectors'].ui_file = os.path.dirname(os.path.realpath(__file__))+'/connector_prop.ui'
        self.properties['connectors'].signal_slot_maps['btnAddPlug'] = ['clicked', self.onAddPlug, tmpGenus.getInitPlug()==None]
        self.properties['connectors'].signal_slot_maps['btnAddSocket'] = ['clicked', self.onAddSocket]
         
        #self.properties['connectors'] = prop
        
        self.properties['isStarter'] = Property('Starter', tmpGenus.isStarter, self.properties['connectors'] )
        self.properties['isTerminator'] = Property('Terminator', tmpGenus.isTerminator, self.properties['connectors'] ) 

        socket_index = 0
        
        self.all_connectors = []
        
        if tmpGenus.plug != None:
            item  = Property('Plug', '',  self.properties['connectors'], Property.CUSTOMER_EDITOR, self.tmpGenus.plug)
            self.fillConnectInfo(0, tmpGenus.plug, item)
            item.ui_file = os.path.dirname(os.path.realpath(__file__))+'/remove_connector.ui'
            item.signal_slot_maps['btnRemoveConn'] = ['clicked', self.onDelPlug]            
            self.properties['Plug'] = item
            
        for connector in tmpGenus.sockets:
            item = Property('Socket', '', self.properties['connectors'] , Property.CUSTOMER_EDITOR, connector)
            self.fillConnectInfo(socket_index, connector, item)
            item.ui_file = os.path.dirname(os.path.realpath(__file__))+'/remove_connector.ui'
            item.signal_slot_maps['btnRemoveConn'] = ['clicked', self.onDelSocket]
            self.properties['sockets'].append(item)
            socket_index += 1
            
        self.properties['connectors'].onAdvBtnClick = self.onShowConnectorsInfo

        ###########
        # Properties #
        ###########
        self.prop_root = Property('Properties','', parents[-1],Property.ADVANCED_EDITOR) 
        
        module_name= tmpGenus.properties['module_name']
        self.properties['module_name'] = Property('module',module_name, self.prop_root,Property.ADVANCED_EDITOR)
        self.properties['module_name'].onAdvBtnClick = self.getModuleName
        self.properties['function_name'] = Property('function',tmpGenus.properties['function_name'] , self.prop_root,Property.COMBO_BOX_EDITOR , self.getModuleFuncList(module_name))

        for key in tmpGenus.properties:
            if(key != 'module_name' and key != 'function_name'):
                self.properties[key] = Property(key,tmpGenus.properties[key], self.prop_root)
    
    def onAddPlug(self,  editor,  item):
        '''
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()

        if not model.insertRow(index.row()+1, index.parent()):
            return

        self.updateActions()

        for column in range(model.columnCount(index.parent())):
            child = model.index(index.row()+1, column, index.parent())
            model.setData(child, "[No data]", QtCore.Qt.EditRole)
        '''        
        
        
        initKind = None;
        initType = None;
        idConnected = ""
        label = "";
        isExpandable = False;
        isLabelEditable = False;
        position = 0        
        plug = BlockConnector(initKind, initType,position, label, isLabelEditable, isExpandable, idConnected)
        #self.tmpGenus.sockets.append(socket)
        item = Property('Plug', '', self.properties['connectors'], Property.CUSTOMER_EDITOR,  plug)
        item.ui_file = os.path.dirname(os.path.realpath(__file__))+'/remove_connector.ui'
        item.signal_slot_maps['btnRemoveConn'] = ['clicked', self.onDelPlug]
        self.fillConnectInfo(0,  plug, item)
       
        index = self.getIndexForNode(item)
        
        self.beginInsertRows(index.parent(), 2, 2) 
        self.properties['plug'] = item
        self.setData(index, plug,  Qt.EditRole)       
        self.sender().setEnabled(False)
        self.properties['connectors'].signal_slot_maps['btnAddPlug'] = ['clicked', self.onAddPlug, False]
        self.endInsertRows()   
        
    def onDelPlug(self,  editor,  item):
        index = self.getIndexForNode(item)             
        self.removeNode(item)        
        self.chkDirty()    
        self.dataChanged.emit(index, index)
        self.showBlock(self.tmpGenus)
        self.properties['connectors'].signal_slot_maps['btnAddPlug'] = ['clicked', self.onAddPlug, True]
    
    def onAddSocket(self,  editor,  item):
        '''
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()

        if not model.insertRow(index.row()+1, index.parent()):
            return

        self.updateActions()

        for column in range(model.columnCount(index.parent())):
            child = model.index(index.row()+1, column, index.parent())
            model.setData(child, "[No data]", QtCore.Qt.EditRole)
        '''
        
        
        
        initKind = 'socket'
        initType = 'string'
        idConnected = ""
        label = "";
        isExpandable = False;
        isLabelEditable = True;
        position = 0        
        socket = BlockConnector(initKind, initType,position, label, isLabelEditable, isExpandable, idConnected);
        item = Property('Socket', '', self.properties['connectors'], Property.CUSTOMER_EDITOR,  socket)
        item.ui_file = os.path.dirname(os.path.realpath(__file__))+'/remove_connector.ui'
        item.signal_slot_maps['btnRemoveConn'] = ['clicked', self.onDelSocket]
        self.fillConnectInfo(len(self.properties['sockets']),  socket, item)  
        index = self.getIndexForNode(item)
        self.properties['sockets'].append(item)
        self.insertRow(index.row(), index.parent())
        self.setData(index, socket,  Qt.EditRole)
    
    def onDelSocket(self,  editor,  item):
        index = self.getIndexForNode(item) 
            
        self.removeNode(item)
        
        self.chkDirty()    
        self.dataChanged.emit(index, index)
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
    
    def onFamilyChanged(self, familyName, sender):
        if familyName != 'n/a' and familyName in BlockGenus.families:            
            self.properties['initLabel'].editorType = Property.COMBO_BOX_EDITOR
            
            var_list = []
            for key in BlockGenus.families[familyName]:
                var_list.append(BlockGenus.families[familyName][key])
            #print(var_list)
            self.properties['initLabel'].obj_data = var_list
        else:
            self.properties['initLabel'].editorType = None
            self.properties['initLabel'].obj_data = None           
    
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
        
    def fillConnectInfo(self,  index,  socket,  parent):
        #Property('index', str(index), parent)
        Property('label', socket.label,parent)
        #Property('kind', socket.kind,parent,  Property.COMBO_BOX_EDITOR, ['socket', 'plug'])
        Property('type', socket.type,parent, Property.COMBO_BOX_EDITOR, ['boolean','cmd','number','poly', 'poly-list', 'string'])

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

    def insertRow(self, row, parent): 
        print('insertRow')
        return self.insertRows(row, 1, parent) 

    def insertRows(self, row, count, parent): 
        self.beginInsertRows(parent, row, (row + (count - 1)))
        self.endInsertRows() 
        return True
    
    def removeRow(self, row, parentIndex): 
        return self.removeRows(row, 1, parentIndex) 

    def removeRows(self, row, count, parentIndex): 
        self.beginRemoveRows(parentIndex, row, row+count) 
        self.endRemoveRows() 
        return True 

    def removeNode(self, node):
        row = node.row()
        #print(node)
        #print(row)
        # item.row() is index row index in connector node
        # in order to get index in self.tmpGenus.sockets list, need minus 2 for before and after connector
        prop_row = row -2
        
        # if there has plug, we need minus 1
        if(self.tmpGenus.getInitPlug() != None):
            prop_row -= 1           
        
        index =  self.getIndexForNode(node)
        self.beginRemoveRows(index.parent(), row, row) 
        node.setParent(None)
        #print(prop_row)
        #print(self.properties['sockets'])
        self.properties['sockets'].pop(prop_row)
        #print(self.properties['sockets'])
        self.tmpGenus.sockets.pop(prop_row)         
        self.endRemoveRows()
        
        #self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), parent_index, parent_index) 
    
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
        ret = super(BlockGenusTreeModel, self).setData(index, value, role)
        if(ret == True):
            item = index.internalPointer()
            property_name = item.objectName()

            if(property_name == 'Family Name'):
                self.tmpGenus.familyName = value
                labelList= []
                if value in BlockGenus.families:            
                    family = BlockGenus.families[value]
                    for name in family:
                        labelList.append(family[name])    
                    self.properties['initLabel'].editorType = Property.COMBO_BOX_EDITOR
                    self.properties['initLabel'].propertyData = labelList
                else:
                    self.properties['initLabel'].editorType = None
            elif(property_name == 'Color'):
                self.tmpGenus.color = value            
            elif(property_name == 'Genus Kind'):
                self.tmpGenus.kind = value
            elif(property_name == 'Init Label'):
                self.tmpGenus.initLabel = value
            elif(property_name == 'Label Prefix'):
                self.tmpGenus.labelPrefix = value
            elif(property_name == 'Label Suffix'):
                self.tmpGenus.labelSuffix = value
            elif(property_name == 'Starter'):
                self.tmpGenus.isStarter = value
            elif(property_name == 'Terminator'):
                self.tmpGenus.isTerminator = value            
            elif (property_name == 'Img') :
                img = value['img']
                img.icon = value['icon']
                img.url = value['url']
            elif (property_name == 'Plug') :
                plug = value
                self.tmpGenus.plug = plug
            elif (property_name == 'Socket') :
                socket = value
                if(socket not in self.tmpGenus.sockets):
                    self.tmpGenus.sockets.append(socket)                    
            elif (item.parent() != None and item.parent().objectName() == 'Img'):
                img = item.parent().value()['img']  
                
                items = item.parent().children()
                height_item = None
                for item in items:
                    if item.objectName() == 'height':
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
            elif (item.parent() != None and item.parent().objectName() == 'Plug'):    
                if(self.tmpGenus.plug != None and item.parent()  == self.properties['Plug'] ):
                    plug = item.parent().obj_data
                    setattr(plug, property_name,  value)
            elif (item.parent() != None and item.parent().objectName() == 'Socket'):             
                socket = item.parent().obj_data
                setattr(socket, property_name,  value)
                
            elif (item.parent() != None and item.parent().objectName() == 'Properties'):    
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
  
        return ret    
        
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
