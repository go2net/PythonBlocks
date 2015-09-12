#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *    
from components.PyMimeData import PyMimeData
from copy import deepcopy 

class DrawerSetsTreeView (QtGui.QTreeView):
    def __init__(self, parent=None):
        super(DrawerSetsTreeView, self).__init__(parent)
        self.header() .close ()        
        #self.setDragDropMode(QAbstractItemView.InternalMove)
        #self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection);
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        #self.setDragEnabled(True)
        self.setDropIndicatorShown(True);

    def init(self, root):
        self.root = root
        
        self.model = DrawerSetsTreeMode(self.root,self)
        self.setModel(self.model)
        self.setItemDelegate(DrawerSetsDelegate(self.model));    
        self.connect(self, QtCore.SIGNAL("itemClicked(QModelIndex)"), self.itemClicked)
        self.connect(self, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.onContentMenu)
        self.setExpandsOnDoubleClick(False)
        #self.setStyleSheet("QTreeView::item:hover{background-color:#FFFF00;}");
        self.setStyleSheet("QTreeView::item:hover{background-color:#999966;}")
        #self.layout().setContentsMargins(5, 5, 5, 5)        
        self.setDefaultDropAction(Qt.MoveAction)
        
    def mouseReleaseEvent (self, event):
        if (event.button() & Qt.RightButton):
            self.emit(SIGNAL("customContextMenuRequested(QPoint)"), event.pos())
        elif (event.button() & Qt.LeftButton):
            self.emit(SIGNAL("itemClicked (QModelIndex)"), self.indexAt(event.pos()))
 
    def onContentMenu(self, pos):
        print('onContentMenu')
        
    def itemClicked (self, index):

        item = index.internalPointer(); 
            
        if (item != None and not item.isLeafNode()):
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)

    def drawRow (self, painter,option, index) :
        item = index.internalPointer(); 
        newOption = option
        if (item !=None and not item.isLeafNode()):
            #painter.fillRect(option.rect, QtCore.Qt.green);
            #newOption.palette.setBrush( QPalette.AlternateBase, Qt.green);
            focusedIndex = self.indexAt(self.mapFromGlobal(QtGui.QCursor.pos()))
            focusedItem = focusedIndex.internalPointer();   
            #print('******BEGIN******')
            #print(focusedItem)
            #print(item)
            #print('******END******')
            if(focusedIndex == index):
            #    print('focusedIndex')
                painter.setPen(QtGui.QColor(0, 0, 240) )
            else:
                painter.setPen(QtGui.QColor(200, 200, 200) )
            painter.drawRect(option.rect);


        QtGui.QTreeView.drawRow(self, painter, newOption, index);
        
    def entered(self,  index):
        item = index.internalPointer();
        if (item !=None and not item.isLeafNode()):
            pass

    #def startDrag(self, supportedActions):
    #    if(self.defaultDropAction() != Qt.IgnoreAction and 
    #       supportedActions & self.defaultDropAction()):
    #        defaultDropAction = self.defaultDropAction()
    #    elif(supportedActions & Qt.CopyAction and
    #         self.dragDropMode() != QAbstractItemView.InternalMove):
    #        defaultDropAction = Qt.CopyAction
    #    return defaultDropAction
    
#    def dragEnterEvent(self, event):
#        if (event.mimeData().hasFormat('application/x-ets-qt4-instance')):
#            print('acceptProposedAction')
#            event.acceptProposedAction() 
 
class DrawerSetsTreeNode(QObject):
    def __init__(self,  parent, obj,  isLeaf = True):
        super(DrawerSetsTreeNode, self).__init__(parent)
        #self.parent = parent
        self.obj = obj
        self.children = []
        self._isLeaf = isLeaf        
       
    def isRoot(self):
        return self.parent() == None    
    
    def row(self):
        if self.parent():
            return self.parent().children.index(self)
        return 0
    
    def isLeafNode(self):
        return self._isLeaf
   
    def removeChild(self, row):
        del self.children[row]
    
    def insert(self, row, node):
        if(not self._isLeaf):
            self.children.insert(row,node)
            node.setParent(self)
            
    def pop(self, row=-1):
        return self.children.pop(row)
        
    def remove(self, node):
        return self.children.remove(node)        
            
class DrawerSetsTreeMode(QtCore.QAbstractItemModel):    
    def __init__(self, root, view):
        super(DrawerSetsTreeMode, self).__init__()        
        self.rootNode = DrawerSetsTreeNode(None, 'root')        
        self.root = root
        self.view = view
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
    
    def getIndexForNode(self, node):
        return self.createIndex(node.row(), 0, node) 
        
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
            
        item = index.internalPointer()        
        
        if(item.isLeafNode()):      
            
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | \
                      QtCore.Qt.ItemIsDragEnabled   
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | \
                      QtCore.Qt.ItemIsDropEnabled     
        
        if (not index.isValid()):
          return QtCore.Qt.ItemIsEnabled;



        if (index.column() == 0):
            return QtCore.Qt.ItemIsEnabled |  QtCore.Qt.ItemIsSelectable 
            
        # only allow change of value attribute
        if (item.isRoot()):
          return  QtCore.Qt.ItemIsEnabled;  
        elif (item.isReadOnly()):
          return  QtCore.Qt.ItemIsDragEnabled 
        else:
          return  QtCore.Qt.ItemIsDragEnabled |  QtCore.Qt.ItemIsEnabled |  QtCore.Qt.ItemIsEditable;

    def nodeFromIndex(self, index): 
        return index.internalPointer() if index.isValid() else self.root 
   
    def mimeTypes(self):
        return ['application/x-ets-qt4-instance']

    def mimeData(self, indices):
        node = self.nodeFromIndex(indices[0])       
        mimeData = PyMimeData(node) 
        return mimeData 
        
        mimeData = QtCore.QMimeData()
        encodedData = QtCore.QByteArray()
        stream = QtCore.QDataStream(encodedData, QtCore.QIODevice.WriteOnly)
 
        for index in indices:
            if not index.isValid():
                continue
            node = index.internalPointer()

            # variant = QtCore.QVariant(node)

            # add all the items into the stream
            stream << node

        print("Encoding drag with: ", "application/block.genus")
        mimeData.setData("application/block.genus", encodedData)
        return mimeData

    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        dragNode = None
        parentNode = None
        
        if action == Qt.IgnoreAction: 
            return True 
        else:
            dragNode = mimedata.instance()
            parentNode = self.nodeFromIndex(parentIndex) 
        
        if action == Qt.MoveAction:
            #old_row = dragNode.row()
            if(dragNode.parent() ==  parentNode):
                parentNode.insert(row,parentNode.pop(dragNode.row()))
            else:               
                if(dragNode.parent() != None):
                    dragNode.parent().remove(dragNode)
                    old_parent_index =  self.getIndexForNode(dragNode.parent())
                    self.removeRow(row, old_parent_index)
                    self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), old_parent_index, old_parent_index) 
                parentNode.insert(row,dragNode)
                self.insertRow(row, parentIndex)                
           
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), parentIndex, parentIndex) 

            return True
        elif action == Qt.CopyAction: 
            dragNode = mimedata.instance() 
            parentNode = self.nodeFromIndex(parentIndex) 

            # make an copy of the node being moved 
            newNode = deepcopy(dragNode)             
            newNode.setParent(parentNode) 
            newNode.newParent = parentNode
            self.insertRow(len(parentNode)-1, parentIndex) 
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), parentIndex, parentIndex) 
            return True 
        elif action == Qt.LinkAction: 
            pass
        else:
            print(Qt.LinkAction)
            print(action)
            print('Invalid action')
            return False
            
    def parent ( self,  index ) :

        if (not index.isValid()):
            return QtCore.QModelIndex()

        childItem = index.internalPointer();
        parentItem = childItem.parent();

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
            
            if(item.parent() == self.rootNode):
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
                        node = DrawerSetsTreeNode(self.rootNode, drawerName, False)
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

    def supportedDropActions(self):   
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction 
        
    def insertRow(self, row, parent): 
        return self.insertRows(row, 1, parent) 

    def insertRows(self, row, count, parent): 
        print('insertRows')
        self.beginInsertRows(parent, row, (row + (count - 1))) 
        self.endInsertRows() 
        return True 

    def removeRow(self, row, parentIndex): 
        return self.removeRows(row, 1, parentIndex) 


    def removeRows(self, row, count, parentIndex): 
        self.beginRemoveRows(parentIndex, row, row) 
        #node = self.nodeFromIndex(parentIndex) 
        #node.removeChild(row) 
        self.endRemoveRows() 

        return True 

class DrawerSetsDelegate(QtGui.QItemDelegate):
    def __init__(self, treeModel):
        super(DrawerSetsDelegate, self).__init__()
        self.treeModel = treeModel
        
    def sizeHint (self, option, index):
        size=QtGui.QItemDelegate.sizeHint(self, option, index);
        #h=size.height();
        item = index.internalPointer();
        
        if(item.isLeafNode()):
            rb = item.obj
            size.setHeight(rb.height()+10)

        return size;
        
    def paint(self, painter, option, index):
        item = index.internalPointer();
        
        if(item.isLeafNode()):
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
        
