#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DrawerSetsTreeView (QtGui.QTreeView):
    def __init__(self, parent=None):
        super(DrawerSetsTreeView, self).__init__(parent)
        self.header() .close ()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
    def init(self, root):
        self.root = root
        
        self.model = DrawerSetsTreeMode(self.root)
        self.setModel(self.model)
        self.setItemDelegate(DrawerSetsDelegate(self.model));    
        self.connect(self, QtCore.SIGNAL("itemClicked(QModelIndex)"), self.itemClicked)
        self.connect(self, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.onContentMenu)
        self.setExpandsOnDoubleClick(False)
        #self.setStyleSheet("QTreeView::item:hover{background-color:#FFFF00;}");
        self.setStyleSheet("QTreeView::item:hover{background-color:#999966;}")
        #self.layout().setContentsMargins(5, 5, 5, 5)        
    
    def mouseReleaseEvent (self, event):
        if (event.button() & Qt.RightButton):
            self.emit(SIGNAL("customContextMenuRequested(QPoint)"), event.pos())
        elif (event.button() & Qt.LeftButton):
            self.emit(SIGNAL("itemClicked (QModelIndex)"), self.indexAt(event.pos()))
 
    def onContentMenu(self, pos):
        print('onContentMenu')
        
    def itemClicked (self, index):

        item = index.internalPointer(); 
            
        if (item.parent == self.model.rootNode):
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)

    def drawRow (self, painter,option, index) :
        item = index.internalPointer(); 
        newOption = option
        if (item !=None and item.parent == self.model.rootNode):
            #painter.fillRect(option.rect, QtCore.Qt.green);
            #newOption.palette.setBrush( QPalette.AlternateBase, Qt.green);
            focusedIndex = self.indexAt(self.mapFromGlobal(QtGui.QCursor.pos()))
            focusedItem = focusedIndex.internalPointer();   
            #print('******BEGIN******')
            #print(focusedItem)
            #print(item)
            #print('******END******')
            #if(focusedIndex == index):
            #    print('focusedIndex')
            #    painter.setPen(QtGui.QColor(0, 0, 240) )
            #else:
            #    painter.setPen(QtGui.QColor(200, 200, 200) )
            #painter.drawRect(option.rect);


        QtGui.QTreeView.drawRow(self, painter, newOption, index);
        
    def entered(self,  index):
        item = index.internalPointer();
        if (item !=None and item.parent == self.model.rootNode):
            pass
    
    def dragEnterEvent(self, event):
        print(event.mimeData().formats())
        if (event.mimeData().hasFormat("text/plain")):
            print('acceptProposedAction')
            event.acceptProposedAction() 
 
class DrawerSetsTreeNode():
    def __init__(self,  parent, obj):
        self.parent = parent
        self.obj = obj
        self.children = []
    def isRoot(self):
        return self.parent == None    
    
    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0
    def flags (self,  index ) :
        return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled; 

        if (not index.isValid()):
          return QtCore.Qt.ItemIsEnabled;

        item = index.internalPointer();

        if (index.column() == 0):
            return QtCore.Qt.ItemIsEnabled |  QtCore.Qt.ItemIsSelectable 
            
        # only allow change of value attribute
        if (item.isRoot()):
          return  QtCore.Qt.ItemIsEnabled;  
        elif (item.isReadOnly()):
          return  QtCore.Qt.ItemIsDragEnabled 
        else:
          return  QtCore.Qt.ItemIsDragEnabled |  QtCore.Qt.ItemIsEnabled |  QtCore.Qt.ItemIsEditable;
      
class DrawerSetsTreeMode(QtCore.QAbstractItemModel):    
    def __init__(self, root):
        super(DrawerSetsTreeMode, self).__init__()
        
        self.rootNode = DrawerSetsTreeNode(None, 'root')
        
        self.root = root
        self.drawerRBs = self.loadBlockDrawerSets(root)        
        
    def columnCount (self,  parent):
        return 1

    def rowCount ( self,  parent ):
        count = len(self.rootNode.children)
        return count

    def index (self,  row, column, parent):
        #return QtCore.QModelIndex();       
        parentItem = self.rootNode
        if (parent.isValid()):
            parentItem = parent.internalPointer();  
        
        if (row >= len(parentItem.children) or row < 0):
            return QtCore.QModelIndex()

        return self.createIndex(row, column, parentItem.children[row])
 
    def parent ( self,  index ) :

        if (not index.isValid()):
            return QtCore.QModelIndex()

        childItem = index.internalPointer();
        parentItem = childItem.parent;

        if (not parentItem or parentItem == self.rootNode):
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem);
 
    def data (self,  index, role):

        if (not index.isValid()):
            return None

        item = index.internalPointer();

        if (role == QtCore.Qt.ToolTipRole or
            role == QtCore.Qt.DecorationRole or
            role == QtCore.Qt.DisplayRole or
            role == QtCore.Qt.EditRole):
            
            if(item.parent == self.rootNode):
                return item.obj
            else:
                rb = item.obj
                return rb.getBlock().getGenusName()
                
        if(role == QtCore.Qt.BackgroundRole):
            if(item != None and item.parent == self.rootNode):
                return QtGui.QColor(240, 240, 240)
            else:
                return QtGui.QColor(QtCore.Qt.green)
                #return QtGui.QApplication.palette("QTreeView").brush(QtGui.QPalette.Normal, QtGui.QPalette.Button).color();

        return None

    def hasChildren(self, parent) :
        item = parent.internalPointer();
        if(item != None and len(item.children) == 0):
            return False
        else:
            return True
 
    def loadBlockDrawerSets(self, root):
        from blocks.Block import Block
        from blocks.FactoryRenderableBlock import FactoryRenderableBlock

        drawerSetNodes = root.findall("BlockDrawerSets/BlockDrawerSet")

        for drawerSetNode in drawerSetNodes:
            drawerNodes=drawerSetNode.getchildren()

            # retreive drawer information of this bar
            for drawerNode in drawerNodes:
                if(drawerNode.tag == "BlockDrawer"):
                    if("name" in drawerNode.attrib):
                        drawerName = drawerNode.attrib["name"]
                        node = DrawerSetsTreeNode(self.rootNode, drawerName)
                        self.rootNode.children.append(node)

                        #manager.addStaticDrawerNoPos(drawerName, QtGui.QColor(100,100,100,0));

                        drawerBlocks = drawerNode.getchildren()
                        blockNode = None
                        for blockNode in drawerBlocks:
                            if(blockNode.tag == "BlockGenusMember"):
                                genusName = blockNode.text
                                newBlock = Block.createBlock(None, genusName, False)
                                rb = FactoryRenderableBlock.from_blockID(None, newBlock.blockID,False, QtGui.QColor(225,225,225,100))
                                sub_node = DrawerSetsTreeNode(node, rb)
                                node.children.append(sub_node)
                                

                #manager.addStaticBlocks(drawerRBs, drawerName);
        return self.rootNode

    def OnContextMenuRequested(self, index, globalPos):
        print('OnContextMenuRequested')

    def dropMimeData(self, data, action, row, column, parent):
       print('dropMimeData')

class DrawerSetsDelegate(QtGui.QItemDelegate):
    def __init__(self, treeModel):
        super(DrawerSetsDelegate, self).__init__()
        self.treeModel = treeModel
        
    def sizeHint (self, option, index):
        size=QtGui.QItemDelegate.sizeHint(self, option, index);
        #h=size.height();
        item = index.internalPointer();
        
        if(item.parent != self.treeModel.rootNode):
            rb = item.obj
            size.setHeight(rb.height()+10)

        return size;
        
    def paint(self, painter, option, index):
        item = index.internalPointer();
        
        if(item.parent != self.treeModel.rootNode):
            #print(option.rect)
            rb = item.obj
            #rb.redrawFromTop()
            #painter.begin(None)
            #rb.reformBlockShape()
            #rb.updateBuffImg(); #this method also moves connected blocks
            pixmap = QPixmap.grabWidget(rb)
            painter.drawImage(option.rect.left(),option.rect.top(), pixmap.toImage ());
            #painter.end()
        else:
            
            super(DrawerSetsDelegate, self).paint(painter, option, index)    
        
