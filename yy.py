import sys 
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from copy import deepcopy 
from pickle import dumps, load, loads 
#from cStringIO import StringIO 
    

class PyMimeData(QMimeData): 
    """ 
    The PyMimeData wraps a Python instance as MIME data. 
    """ 
    # The MIME type for instances. 
    MIME_TYPE = 'application/x-ets-qt4-instance' 

    def __init__(self, data=None): 
        """ 
        Initialise the instance. 
        """ 
        QMimeData.__init__(self) 

        # Keep a local reference to be returned if possible. 
        self._local_instance = data 

        if data is not None: 
            # We may not be able to pickle the data. 
            try: 
                pdata = dumps(data) 
            except: 
                return 

            # This format (as opposed to using a single sequence) allows the 
            # type to be extracted without unpickling the data itself. 
            self.setData(self.MIME_TYPE, dumps(data.__class__) + pdata) 

    @classmethod 
    def coerce(cls, md): 
        """ 
        Coerce a QMimeData instance to a PyMimeData instance if possible. 
        """ 
        # See if the data is already of the right type.  If it is then we know 
        # we are in the same process. 
        if isinstance(md, cls): 
            return md 

        # See if the data type is supported. 
        if not md.hasFormat(cls.MIME_TYPE): 
            return None 

        nmd = cls() 
        nmd.setData(cls.MIME_TYPE, md.data()) 

        return nmd 

    def instance(self): 
        """ 
        Return the instance. 
        """ 
        if self._local_instance is not None: 
            return self._local_instance 

        io = StringIO(str(self.data(self.MIME_TYPE))) 

        try: 
            # Skip the type. 
            load(io) 

            # Recreate the instance. 
            return load(io) 
        except: 
            pass 

        return None 

    def instanceType(self): 
        """ 
        Return the type of the instance. 
        """ 
        if self._local_instance is not None: 
            return self._local_instance.__class__ 

        try: 
            return loads(str(self.data(self.MIME_TYPE))) 
        except: 
            pass 

        return None 


class myNode(object): 
    def __init__(self, name, state, description, parent=None): 

        self.name = name
        self.state = state
        self.description = description

        self.parent = parent 
        self.children = [] 

        self.setParent(parent) 

    def setParent(self, parent): 
        if parent != None: 
            self.parent = parent 
            self.parent.appendChild(self) 
        else: 
            self.parent = None 

    def appendChild(self, child): 
        self.children.append(child) 

    def childAtRow(self, row): 
        return self.children[row] 

    def rowOfChild(self, child):       
        for i, item in enumerate(self.children): 
            if item == child: 
                return i 
        return -1 

    def removeChild(self, row): 
        value = self.children[row] 
        self.children.remove(value) 

        return True 

    def __len__(self): 
        return len(self.children) 


class myModel(QAbstractItemModel): 

    def __init__(self, parent=None): 
        super(myModel, self).__init__(parent) 

        self.treeView = parent 
        self.headers = ['Item','State','Description'] 

        self.columns = 3 

        # Create items 
        self.root = myNode('root', 'on', 'this is root', None) 

        itemA = myNode('itemA', 'on', 'this is item A', self.root) 
        itemA1 = myNode('itemA1', 'on', 'this is item A1', itemA) 

        itemB = myNode('itemB', 'on', 'this is item B', self.root) 
        itemB1 = myNode('itemB1', 'on', 'this is item B1', itemB) 

        itemC = myNode('itemC', 'on', 'this is item C', self.root) 
        itemC1 = myNode('itemC1', 'on', 'this is item C1', itemC) 


    def supportedDropActions(self): 
        return Qt.CopyAction | Qt.MoveAction 


    def flags(self, index): 
        defaultFlags = QAbstractItemModel.flags(self, index) 

        if index.isValid(): 
            return Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | defaultFlags 

        else: 
            return Qt.ItemIsDropEnabled | defaultFlags 


    def headerData(self, section, orientation, role): 
        if orientation == Qt.Horizontal and role == Qt.DisplayRole: 
            return self.headers[section]
        return None

    def mimeTypes(self): 
        types = []
        types.append('application/x-ets-qt4-instance') 
        return types 

    def mimeData(self, index): 
        node = self.nodeFromIndex(index[0])       
        mimeData = PyMimeData(node) 
        return mimeData 


    def dropMimeData(self, mimedata, action, row, column, parentIndex): 
        if action == Qt.IgnoreAction: 
            return True 

        dragNode = mimedata.instance() 
        parentNode = self.nodeFromIndex(parentIndex) 

        # make an copy of the node being moved 
        newNode = deepcopy(dragNode) 
        newNode.setParent(parentNode) 
        self.insertRow(len(parentNode)-1, parentIndex) 
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), parentIndex, parentIndex) 
        return True 


    def insertRow(self, row, parent): 
        return self.insertRows(row, 1, parent) 


    def insertRows(self, row, count, parent): 
        self.beginInsertRows(parent, row, (row + (count - 1))) 
        self.endInsertRows() 
        return True 


    def removeRow(self, row, parentIndex): 
        return self.removeRows(row, 1, parentIndex) 


    def removeRows(self, row, count, parentIndex): 
        self.beginRemoveRows(parentIndex, row, row) 
        node = self.nodeFromIndex(parentIndex) 
        node.removeChild(row) 
        self.endRemoveRows() 

        return True 


    def index(self, row, column, parent): 
        node = self.nodeFromIndex(parent) 
        return self.createIndex(row, column, node.childAtRow(row)) 


    def data(self, index, role): 
        if role == Qt.DecorationRole: 
            return None 

        if role == Qt.TextAlignmentRole: 
            return int(Qt.AlignTop | Qt.AlignLeft)

        if role != Qt.DisplayRole: 
            return None

        node = self.nodeFromIndex(index) 

        if index.column() == 0: 
            return node.name

        elif index.column() == 1: 
            return node.state

        elif index.column() == 2: 
            return node.description
        else: 
            return None 


    def columnCount(self, parent): 
        return self.columns 


    def rowCount(self, parent): 
        node = self.nodeFromIndex(parent) 
        if node is None: 
            return 0 
        return len(node) 


    def parent(self, child): 
        if not child.isValid(): 
            return QModelIndex() 

        node = self.nodeFromIndex(child) 

        if node is None: 
            return QModelIndex() 

        parent = node.parent 

        if parent is None: 
            return QModelIndex() 

        grandparent = parent.parent 
        if grandparent is None: 
            return QModelIndex() 
        row = grandparent.rowOfChild(parent) 

        assert row != - 1 
        return self.createIndex(row, 0, parent) 


    def nodeFromIndex(self, index): 
        return index.internalPointer() if index.isValid() else self.root 



class myTreeView(QTreeView): 

    def __init__(self, parent=None): 
        super(myTreeView, self).__init__(parent) 

        self.myModel = myModel() 
        self.setModel(self.myModel) 

        self.dragEnabled() 
        self.acceptDrops() 
        self.showDropIndicator() 
        self.setDragDropMode(QAbstractItemView.InternalMove) 

        self.connect(self.model(), SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.change) 
        self.expandAll() 

    def change(self, topLeftIndex, bottomRightIndex): 
        self.update(topLeftIndex) 
        self.expandAll() 
        self.expanded() 

    def expanded(self): 
        for column in range(self.model().columnCount(QModelIndex())): 
            self.resizeColumnToContents(column) 



class Ui_MainWindow(object): 
    def setupUi(self, MainWindow): 
        MainWindow.setObjectName("MainWindow") 
        MainWindow.resize(600, 400) 
        self.centralwidget = QWidget(MainWindow) 
        self.centralwidget.setObjectName("centralwidget") 
        self.horizontalLayout = QHBoxLayout(self.centralwidget) 
        self.horizontalLayout.setObjectName("horizontalLayout") 
        self.treeView = myTreeView(self.centralwidget) 
        self.treeView.setObjectName("treeView") 
        self.horizontalLayout.addWidget(self.treeView) 
        MainWindow.setCentralWidget(self.centralwidget) 
        self.menubar = QMenuBar(MainWindow) 
        self.menubar.setGeometry(QRect(0, 0, 600, 22)) 
        self.menubar.setObjectName("menubar") 
        MainWindow.setMenuBar(self.menubar) 
        self.statusbar = QStatusBar(MainWindow) 
        self.statusbar.setObjectName("statusbar") 
        MainWindow.setStatusBar(self.statusbar) 

        self.retranslateUi(MainWindow) 
        QMetaObject.connectSlotsByName(MainWindow) 

    def retranslateUi(self, MainWindow): 
        MainWindow.setWindowTitle(QApplication.translate("MainWindow", "MainWindow", None, QApplication.UnicodeUTF8)) 


if __name__ == "__main__": 
    app = QApplication(sys.argv) 
    MainWindow = QMainWindow() 
    ui = Ui_MainWindow() 
    ui.setupUi(MainWindow) 
    MainWindow.show() 
    sys.exit(app.exec_()) 
