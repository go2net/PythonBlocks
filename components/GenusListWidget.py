from PyQt4.QtCore import *
from PyQt4.QtGui import *

class GenusListWidget(QListWidget):
    def __init__(self, parent):
        super(GenusListWidget, self).__init__(parent)
        self.currentItemChanged.connect(self.onItemChanged)
        
    def setMainWnd(self, mainWnd):
        self.mainWnd = mainWnd   
    
    def mouseMoveEvent(self, e):
        from blocks.Block import Block
        from blocks.FactoryRenderableBlock import FactoryRenderableBlock
        
        if e.buttons() != Qt.LeftButton:
            return
        
        genusName =  self.currentItem().text()
        
        # write the relative cursor position to mime data
        mimeData = QMimeData()
        # simple string with 'x,y'
        mimeData.setText('%d,%d' % (e.x(), e.y())) 
        
        block = Block.createBlockFromID(None, genusName)
        factoryRB = FactoryRenderableBlock.from_block(None, block)
        
        #print(self.mainWnd.genusTreeModel.factoryRB)
        # let's make it fancy. we'll show a "ghost" of the button as we drag
        # grab the button to a pixmap
        pixmap = QPixmap.grabWidget(factoryRB)

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


    def onItemChanged(self, current, previous):
        from blocks.BlockGenus import BlockGenus
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
                self.setCurrentItem(previous)
                pass                
