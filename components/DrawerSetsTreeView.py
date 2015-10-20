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
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection);
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        #self.setDragEnabled(True)
        self.setDropIndicatorShown(True);
        self.popMenu = QtGui.QMenu(self)
        self.focusedIndex = None
        
    def init(self, root):
        
        self.root = root        
        self.model = DrawerSetsTreeMode(self.root,self)
        self.setModel(self.model)
        self.setItemDelegate(DrawerSetsDelegate(self.model));    
        self.connect(self, QtCore.SIGNAL("itemClicked(QModelIndex)"), self.itemClicked)
        self.connect(self, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.onContentMenu)
        self.setExpandsOnDoubleClick(False)
        self.setStyleSheet("QTreeView::item:hover{background-color:#999966;}")
        #self.setStyleSheet("QTreeView::item:hover{background-color:#999966;}")
        #self.layout().setContentsMargins(5, 5, 5, 5)        
        self.setDefaultDropAction(Qt.MoveAction)
        self.setMouseTracking(True);
        
    def mouseReleaseEvent (self, event):
        #if (event.button() & Qt.RightButton):
        #    self.emit(SIGNAL("customContextMenuRequested(QPoint)"), event.pos())
        if (event.button() & Qt.LeftButton):
            self.emit(SIGNAL("itemClicked (QModelIndex)"), self.indexAt(event.pos()))
 
    def mouseMoveEvent (self, event):
        focusedIndex = self.indexAt(event.pos())
        if(self.focusedIndex != focusedIndex):
            self.focusedIndex = focusedIndex
        self.model.dataChanged.emit(QModelIndex(), QModelIndex())
        #self.model.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), focusedIndex, focusedIndex) 
        #focusedItem = focusedIndex.internalPointer()
        #print(focusedItem)
        super(DrawerSetsTreeView, self).mouseMoveEvent(event);      
 
    def onContentMenu(self, pos):
        focusedIndex = self.indexAt(pos)
        focusedItem = focusedIndex.internalPointer()                 
        self.popMenu.clear() 
 
        if(focusedItem != None): 
            if not focusedItem.isLeafNode():
                #action = self.popMenu.addAction('Rename')
                rename_nodes_action = self.popMenu.addAction('Rename - ' + focusedItem.obj)
                rename_nodes_action.triggered.connect(lambda: self.onRenameNode(focusedItem))
                remove_nodes_action = self.popMenu.addAction('Remove - ' + focusedItem.obj)
                remove_nodes_action.triggered.connect(lambda: self.onRemoveNodes(focusedItem))
            else:
                remove_node_action = self.popMenu.addAction('Remove - ' + focusedItem.obj.getBlock().genusName)
                remove_node_action.triggered.connect(lambda: self.onRemoveNode(focusedItem))        
        
            self.popMenu.addSeparator()    
            
        expand_all_action = self.popMenu.addAction('Expand all')
        self.connect(expand_all_action,QtCore.SIGNAL("triggered()"),self.expandAll)    
        
        collapse_all_action = self.popMenu.addAction('Collapse all')    
        self.connect(collapse_all_action,QtCore.SIGNAL("triggered()"),self.collapseAll)    
        
        #self.connect(action,QtCore.SIGNAL("triggered()"),self,QtCore.SLOT("printItem('%s')" % item))    
        
        self.popMenu.exec_(self.mapToGlobal(pos))
   
    def onRenameNode(self, node):        
        old_name = node.obj
        new_name, ok = QtGui.QInputDialog.getText(self.window(), 'Rename variable','Change variable name from "{0}" to'.format(old_name), QtGui.QLineEdit.Normal, old_name)     
        node.obj = new_name
        index = self.model.getIndexForNode(node)
        self.model.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index) 
        
    def onRemoveNode(self,  node):
        self.model.removeNode(node)
        
    def onRemoveNodes(self,  rootNode):
        
        for node in rootNode.children:
            self.model.removeNode(node)        
        self.model.removeNode(rootNode) 
        
    def itemClicked (self, index):

        item = index.internalPointer(); 
            
        if (item != None and not item.isLeafNode()):
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)
 
    def drawRow( self, painter, option, index ) :
        item = index.internalPointer()        
        
        if (item !=None and not item.isLeafNode()):            
            focusedIndex = self.indexAt(self.mapFromGlobal(QtGui.QCursor.pos()))
            focusedItem = focusedIndex.internalPointer()
            serifFont = option.font
            
            if(focusedItem == item):
                brush = QBrush( QColor( 240, 240, 250 ) );
                pen = QColor( 100, 100, 255 )
                serifFont.setBold(True);
            else:
                brush = QBrush( QColor( 240, 240, 240 ) )
                pen = QColor( 200, 200, 200 ) 
                serifFont.setBold(False);
                
            option.font = serifFont;
            
            rect = option.rect
            rect.setX(2)
            rect.setY(rect.y() + 2)           

            rect.setWidth (self.viewport().width()-4)
            rect.setHeight  (rect.height()-2)
            
            painter.save()
            painter.setBrush (brush)
            painter.setPen(pen)
            #painter.fillRect( option.rect, brush) 
            painter.drawRect( rect) 
            painter.restore();

            #painter.end()
                
        super(DrawerSetsTreeView, self).drawRow( painter, option, index );  
 
    def drawBranches(self, painter, rect, index):
         super(DrawerSetsTreeView, self).drawBranches(painter, rect, index)

    def drawItem(self, painter, rect,  index,  option=None):
        pass
              
        
    def entered(self,  index):
        item = index.internalPointer();
        if (item !=None and not item.isLeafNode()):
            pass

    def getSaveString(self):
        #print('DrawerSetsTreeView.getSaveString()')
        return self.model.getSaveString()
        
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
 
    def getNodeInfo(self):
        drawerSetInfo = {}  
        if self.isRoot():
            drawerSetInfo['block_drawer_sets'] =  [node.getNodeInfo() for node in self.children]      
        elif not self._isLeaf:
            drawerSetInfo['drawer'] = self.obj
            drawerSetInfo['genus-list'] = [node.obj.getBlock().genusName for node in self.children]
        #else:
        #    drawerSetInfo['genus'] = self.obj.getBlock().genusName        
        
        #print(drawerSetInfo)
        return drawerSetInfo
        
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
    
    def nodeExist(self, node):
        for child_node in self.children:
            if(node.obj.getBlock().genusName == child_node.obj.getBlock().genusName):
                return True
        return False
        
class DrawerSetsTreeMode(QtCore.QAbstractItemModel):    
    def __init__(self, root, view):
        super(DrawerSetsTreeMode, self).__init__()        
        self.rootNode = DrawerSetsTreeNode(None, 'root')        
        self.root = root
        self.view = view
        self.drawerRBs = self.loadBlockDrawerSets(root)        

    def getSaveString(self):
        import json
        #print('DrawerSetsTreeMode.getSaveString()')
        return json.dumps(self.rootNode.getNodeInfo(), sort_keys=False, indent=2)
    
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
        elif (not item.isRoot()):
            return  QtCore.Qt.ItemIsDropEnabled
        
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
                if(parentNode.nodeExist(dragNode)): 
                    return True
                
                if(dragNode.parent() != None):
                    self.removeNode(dragNode)                    

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
            
            if(not item.isLeafNode()):
                return item.obj
            else:
                rb = item.obj
                return rb.getBlock().getGenusName()
                
        #if(role == QtCore.Qt.BackgroundRole):
        #    if(item != None and not item.isLeafNode()):
        #        return QtGui.QColor(240, 240, 240)
        #    else:
        #        return QtGui.QColor(255, 255, 255)
        #        #return QtGui.QApplication.palette("QTreeView").brush(QtGui.QPalette.Normal, QtGui.QPalette.Button).color();

        return None

    def hasChildren(self, parent) :
        item = parent.internalPointer();
        if(item != None and len(item.children) == 0):
            return False
        else:
            return True
 
    def buildNodes(self, data):
        from blocks.Block import Block
        from blocks.FactoryRenderableBlock import FactoryRenderableBlock        
        if 'block_drawer_sets' in data:
            block_drawer_sets = data['block_drawer_sets']
            for drawerElement in block_drawer_sets:
                if 'drawer' in drawerElement and 'genus-list' in drawerElement:
                    drawerName = drawerElement['drawer']
                    node = DrawerSetsTreeNode(self.rootNode, drawerName, False)
                    self.rootNode.children.append(node)                
                    member = drawerElement['genus-list']
                    for genusName in member:
                        newBlock = Block.createBlock(None, genusName, False)
                        rb = FactoryRenderableBlock.from_blockID(None, newBlock.blockID,False, QtGui.QColor(255,255,255,0))
                        sub_node = DrawerSetsTreeNode(node, rb)
                        node.children.append(sub_node)
 
    def loadBlockDrawerSets(self, path):
        import json
        f=open(path)
        data=json.load(f)
        self.buildNodes(data)
        return


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
        self.beginRemoveRows(parentIndex, row, row+count) 
        self.endRemoveRows() 
        return True 

    def removeNode(self, node):
        row = node.row()
        parent_index =  self.getIndexForNode(node.parent())
        node.parent().remove(node)
        self.removeRow(row, parent_index)
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), parent_index, parent_index) 
        
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
        else:
            size.setHeight(20)
            
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
        
