from PyQt4.QtCore import *
from PyQt4.QtGui import *

class GenusListWidget(QListWidget):
    def __init__(self, parent):
        super(GenusListWidget, self).__init__(parent)
        #self.currentItemChanged.connect(self.onCurrentItemChanged)
        #self.itemChanged.connect(self.onItemChanged)
        self.viewport().installEventFilter(self); 
        self.installEventFilter(self); 
        #self.setMouseTracking(True);
    def setMainWnd(self, mainWnd):
        self.mainWnd = mainWnd
    
    def eventFilter(self, source,  event):
        #from blocks.FactoryRenderableBlock import FactoryRenderableBlock
        ret = False
        if (event.type() ==  QEvent.MouseButtonPress):
            if event.button() == Qt.LeftButton:
                item  = self.itemAt(event.pos()) 
                previous = self.currentItem()
                ret = self.onItemChanging(item, previous)

        elif (event.type() ==  QEvent.KeyPress):
            previous = self.currentItem()
            item = None
            row = self.currentRow()
            if(event.key() == Qt.Key_Up):
                if(previous != None and row >0):                    
                    item = self.item(row-1)
                        
            if(event.key() == Qt.Key_Down):
                if(previous != None and row < self.count()-1):
                    item = self.item(row+1)
            ret = self.onItemChanging(item, previous)

        if(ret == False):
            return QListWidget.eventFilter(self, source,  event);
        else:
            return True
            
    def onItemChanging(self,current, previous ):  
        from blocks.BlockGenus import BlockGenus
        if(previous == None or current==previous): return False
        genusName =  previous.text()
        genus = BlockGenus.getGenusWithName(genusName)
        if(genus.isDirty):
            tmpGenus = BlockGenus.getGenusWithName('__previewGenus__')
            msgBox = QMessageBox()
            msgBox.setText("The Genus Block has been modified.")
            msgBox.setInformativeText("Do you want to apply your changes?")
            msgBox.setStandardButtons(QMessageBox.Apply | QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Apply)
            ret = msgBox.exec_()
            if ret  == QMessageBox.Apply:
                genus.copyDataFrom(tmpGenus)
                genus.isDirty = False
                self.mainWnd.wndApplyGenus.hide()
            if ret  == QMessageBox.Discard:
                genus.isDirty = False
                self.mainWnd.wndApplyGenus.hide()
            if ret  == QMessageBox.Cancel:
                return True        
        return False
    
    def mouseMoveEvent(self, e):
        from blocks.Block import Block
        from blocks.FactoryRenderableBlock import FactoryRenderableBlock
        from components.PyMimeData import PyMimeData
        from components.DrawerSetsTreeView import DrawerSetsTreeNode        

        if e.buttons() != Qt.LeftButton:
            return
        
        genusName =  self.currentItem().text()
        newBlock = Block.createBlock(None, genusName, False)
        rb = FactoryRenderableBlock.from_blockID(None, newBlock.blockID,False, QColor(225,225,225,100))
        sub_node = DrawerSetsTreeNode(None, rb)        
        mimeData = PyMimeData(sub_node) 
        
        # write the relative cursor position to mime data
        #mimeData = QMimeData()
        
        #item = self.currentItem()
        #mimeData.setText(item.text())
        
        #block = Block.createBlockFromID(None, genusName)
        #factoryRB = FactoryRenderableBlock.from_block(None, block)
        
        #print(self.mainWnd.genusTreeModel.factoryRB)
        # let's make it fancy. we'll show a "ghost" of the button as we drag
        # grab the button to a pixmap
        pixmap = QPixmap.grabWidget(rb)
        mimeData.setImageData(pixmap)
        
        # below makes the pixmap half transparent
        painter = QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QColor(0, 0, 0, 127))
        painter.end()        

        # make a QDrag
        drag = QDrag(self)
        # put our MimeData
        drag.setMimeData(mimeData)
        # set its Pixmap
        drag.setPixmap(pixmap)
        # shift the Pixmap so that it coincides with the cursor position
        drag.setHotSpot(QPoint (0, 0))

        # start the drag operation
        # exec_ will return the accepted action from dropEvent
        if drag.exec_(Qt.CopyAction | Qt.MoveAction) == Qt.MoveAction:
            print ('moved')
        else:
            print ('copied')
    
    '''
    def onItemChanged(self, item):
        from blocks.BlockGenus import BlockGenus
        #return
        #print('onItemChanged')
        return
        
        previous = self.currentItem()
        
        if previous == None: return

        genusName =  previous.text()
        genus = BlockGenus.getGenusWithName(genusName)
        print(current.text())
        if(genus.isDirty):
            tmpGenus = BlockGenus.getGenusWithName('__previewGenus__')
            msgBox = QMessageBox()
            msgBox.setText("The Genus Block has been modified.")
            msgBox.setInformativeText("Do you want to apply your changes?")
            msgBox.setStandardButtons(QMessageBox.Apply | QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Apply)
            ret = msgBox.exec_()
            if ret  == QMessageBox.Apply:
                genus.copyDataFrom(tmpGenus)
                pass
            if ret  == QMessageBox.Discard:
                genus.isDirty = False
                self.mainWnd.wndApplyGenus.hide()
                pass
            if ret  == QMessageBox.Cancel:
                return
                pass    
        
        
        
    def onCurrentItemChanged(self, current, previous):
        from blocks.BlockGenus import BlockGenus
        print('onCurrentItemChanged')
        return
        if previous == None: return

        genusName =  previous.text()
        genus = BlockGenus.getGenusWithName(genusName)
        print(current.text())
        if(genus.isDirty):
            tmpGenus = BlockGenus.getGenusWithName('__previewGenus__')
            msgBox = QMessageBox()
            msgBox.setText("The Genus Block has been modified.")
            msgBox.setInformativeText("Do you want to apply your changes?")
            msgBox.setStandardButtons(QMessageBox.Apply | QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Apply)
            ret = msgBox.exec_()
            if ret  == QMessageBox.Apply:
                genus.copyDataFrom(tmpGenus)
                pass
            if ret  == QMessageBox.Discard:
                genus.isDirty = False
                self.mainWnd.wndApplyGenus.hide()
                pass
            if ret  == QMessageBox.Cancel:
                self.currentItem = previous
                QTimer.singleShot(0, self.goBack);
                pass                

    def goBack(self):
        #qDebug("GoBack: %d", currentRow);
        self.setCurrentItem(self.currentItem);
    '''
