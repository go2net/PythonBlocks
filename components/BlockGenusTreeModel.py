#!/usr/bin/env python

from components.propertyeditor.QPropertyModel import  QPropertyModel
from components.propertyeditor.Property import Property
from components.ConnectorsInfoWnd import ConnectorsInfoWnd
from components.ImagesInfoWnd import ImagesInfoWnd
from blocks.BlockGenus import BlockGenus
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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
        self.mainWnd = mainWnd
        self.mainWnd.btnApply.clicked.connect(self.onApply)
        self.langDefLocation = langDefLocation
        self.setupModelData(self.tmpGenus, self.m_rootItem)
        self.isDirty = False
        self.popMenu = QMenu(self.view)

    def flags (self,  index ):
        if (not index.isValid()):
            return Qt.NoItemFlags;
        
        item = index.internalPointer()
        property_name = item.objectName()

        if 'Img #' in item.parent().objectName():
            img = item.parent().value()['img']
            if(property_name == 'height'):
                if not img.lockRatio:                
                    return Qt.ItemIsEnabled | Qt.ItemIsEditable;
                else:
                    return Qt.NoItemFlags

        return QPropertyModel.flags(self, index)
       
    def setupModelData(self, tmpGenus, parent):
        parents = [parent]
        self.showBlock(tmpGenus)       
    
        self.properties['genusName'] = Property('Genus Name', tmpGenus.genusName, parents[-1])         
        self.properties['kind'] = Property('Genus Kind', tmpGenus.kind, parents[-1], Property.COMBO_BOX_EDITOR, ['command', 'data', 'function', 'param','procedure','variable'])
        
        familyNameList = ['n/a']
        familyName = tmpGenus.familyName
        for name in BlockGenus.families:
            familyNameList.append(name)
        if(familyName == ''):
            familyName = 'n/a'
            
        self.properties['familyName'] = Property('Family Name', familyName, parents[-1], Property.COMBO_BOX_EDITOR,familyNameList)             

        labelList= []
        if familyName in BlockGenus.families:            
            family = BlockGenus.families[familyName]
            for name in family:
                labelList.append(family[name])  
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
        self.properties['connectors'] = Property('Connectors','', parents[-1],Property.ADVANCED_EDITOR)   
        self.properties['isStarter'] = Property('Starter', tmpGenus.isStarter, self.properties['connectors'] )
        self.properties['isTerminator'] = Property('Terminator', tmpGenus.isTerminator, self.properties['connectors'] ) 
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

        ############
        #      Language       #
        ############
        self.lang_root = Property('Language','', parents[-1],Property.ADVANCED_EDITOR) 
        
        module_name= tmpGenus.properties['module_name']
        self.properties['module_name'] = Property('module',module_name, self.lang_root,Property.ADVANCED_EDITOR)
        self.properties['module_name'].onAdvBtnClick = self.getModuleName
        self.properties['function_name'] = Property('function',tmpGenus.properties['function_name'] , self.lang_root,Property.COMBO_BOX_EDITOR , self.getModuleFuncList(module_name))

        for key in tmpGenus.properties:
            if(key != 'module_name' and key != 'function_name'):
                self.properties[key] = Property(key,tmpGenus.properties[key], self.lang_root)
    
    def addImages(self,  imgs_root, genus):
        img_index = 0
        for loc, img in self.tmpGenus.blockImageMap.items():           
            self.addImage(imgs_root, img_index, img)
            img_index += 1
   
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
 
        img_root = Property('Img #'+str(img_index),image_data, imgs_root,Property.IMAGE_EDITOR) 
        img_root.onAdvBtnClick = self.loadFromFile
        img_root.onMenuBtnClick = self.onShowImgSelMenu

        self.properties['Img #'+str(img_index)] = img_root
        self.properties['location'] = Property('location', img.location, img_root,Property.COMBO_BOX_EDITOR, ['CENTER', 'EAST', 'WEST', 'NORTH', 'SOUTH', 'SOUTHEAST', 'SOUTHWEST', 'NORTHEAST', 'NORTHWEST'] )
        self.properties['lock_ratio'] = Property('lock ratio',img.lockRatio, img_root  )
        self.properties['width'] = Property('width',img.width(), img_root  )
        self.properties['height'] = Property('height',img.height(),img_root)
        
        self.properties['editable'] = Property('editable', img.isEditable, img_root )
        self.properties['wraptext'] = Property('wraptext', img.wrapText, img_root )
        
    def fillConnectInfo(self,  socket,  parent):
        Property('label', socket.label,parent)
        Property('kind', socket.kind,parent,  Property.COMBO_BOX_EDITOR, ['socket', 'plug'])
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
            self.imgs_root.children().clear()
            
            for img in dlg.blockImages:
                self.tmpGenus.blockImageMap[img.location] = img
                
            self.addImages(self.imgs_root, self.tmpGenus)
            index = self.getIndexForNode(self.imgs_root)
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index) 
            
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
        dlg.exec_()

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

                if(labelList != []):
                    self.properties['initLabel'].editorType = Property.COMBO_BOX_EDITOR
                    self.properties['initLabel'].propertyData = labelList
                else:
                    self.properties['initLabel'].editorType = None
                
                #self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index) 
                
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
            
            
            if 'Img #' in property_name:
                img = value['img']
                img.icon = value['icon']
                img.url = value['url']
                    
            if 'Img #' in item.parent().objectName():         
                img = item.parent().value()['img']  
                
                items = item.parent().children()
                height_item = None
                for item in items:
                    if item.objectName() == 'height':
                        height_item = item
                        break
                
            
                if(property_name == 'location'):
                    img.location = value
                    
                if(property_name == 'editable'):
                    img.isEditable = value
                    
                if(property_name == 'wraptext'):
                    img.wrapText = value
                    
                if(property_name == 'lock ratio'):
                    if(value==True and img.lockRatio != value):
                        img.lockRatio = value
                        if (height_item != None):
                            height = img.width()*img.icon.height()/img.icon.width()
                            height_item.setValue(height)                        
                        img.setSize(img.width(), height, True)
                        
                    else:
                        img.lockRatio = value
                        
                if(property_name == 'width'):
                    if (img.lockRatio == True and height_item != None):
                        height = img.width()*img.icon.height()/img.icon.width()
                        height_item.setValue(height)
                    else:
                        height = img.height()
                        
                    img.setSize(value, height, True)
                    
                if(property_name == 'height'):
                    img.setSize(img.width(),  value)
                
            if(self.tmpGenus.plug != None and item.parent()  == self.properties['Left #0'] ):
                self.setConnectorProp(self.tmpGenus.plug,property_name, value )
            
            socket_index = 0
            for socket in self.tmpGenus.sockets:
                if(item.parent() == self.properties['Right #'+str(socket_index)] ):
                    self.setConnectorProp(socket,property_name, value )
                    break
                socket_index += 1
                
            for key in self.tmpGenus.properties:    
                if(property_name==key):
                    self.tmpGenus.properties[key] = value  
                    break
                
        self.showBlock(self.tmpGenus)

        #self.isDirty = self.tmpGenus != self.genus
        self.genus.isDirty = self.tmpGenus != self.genus
        if(not self.genus.isDirty): 
            self.mainWnd.wndApplyGenus.hide()
        else:
            self.mainWnd.wndApplyGenus.show()
            
        return ret    
    def setConnectorProp(self, connector, property_name, value):
        tt = 'connector.'+property_name+'=\'' + str(value)+'\''
        print(tt)
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
