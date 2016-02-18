from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
import os

class ConnectorsInfoWnd(QDialog):
    def __init__(self, treeModel, genus):
     
        super(ConnectorsInfoWnd, self).__init__()
        self.genus = genus
        self.treeModel = treeModel
        dirname, filename = os.path.split(os.path.abspath(__file__))
        loadUi(dirname+'\\connector_info.ui', self)   

        self.btnAdd.clicked.connect(self.onAddConnector)
        self.btnOk.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)

        self.header = ['Label', 'Kind', 'Type'] 

        connectors = []

        if(genus.plug != None):  
            connectors.append(genus.plug)
            
        for socket in self.genus.sockets: 
            connectors.append(socket)
    
        model = ConnectorTableModel(self, connectors, self.header)
        self.tableView.setModel(model)

        verticalHeader = self.tableView.verticalHeader();
        #verticalHeader.setDefaultAlignment (Qt.AlignLeft)
        verticalHeader.setResizeMode(QHeaderView.Fixed);
        verticalHeader.setDefaultSectionSize(18);

        self.tableView.setItemDelegate(MyDelegate(self.tableView));
        self.tableView.setEditTriggers(QAbstractItemView.AllEditTriggers)
        
    def onAddConnector(self):
        self.tableView.model().addConnector()
        
class ConnectorTableModel(QAbstractTableModel):    
    def __init__(self, parent, connectors, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.connectors = connectors
        self.header = header
        self.InfoWnd = parent
        
    def rowCount(self, parent):
        return len(self.connectors)
        
    def columnCount(self, parent):
        return len(self.header)

    def flags (self,  index ) :
      if (not index.isValid()):
        return Qt.ItemIsEnabled;

      return Qt.ItemIsDragEnabled |  Qt.ItemIsEnabled |  Qt.ItemIsEditable;

    def addConnector(self):
        return
        from blocks.BlockImageIcon import BlockImageIcon
        icon = QPixmap(os.getcwd() + "\\" + 'resource\\117-puzzle.png')
        img = BlockImageIcon('', 'CENTER', icon, 32, 32, False, False)
        self.blockImages.append(img)
        index = QModelIndex ()
        self.insertRow(len(self.blockImages), index)
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index) 
      
    def setData(self, index, value, role=Qt.DisplayRole):
      if (index.isValid() and role == Qt.EditRole):
        connector = self.connectors[index.row()]
        if(index.column() == 0):
          connector.label = value
          
        if(index.column() == 1):
          connector.kind = value
          
        if(index.column() == 2):
          connector.type = value
        
        #emit dataChanged(index, index);
        self.InfoWnd.treeModel.showBlock(self.InfoWnd.genus)
        return True;
      return False
      
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
          
        connector = self.connectors[index.row()]

        if(index.column() == 0):
            return connector.label

        if(index.column() == 1):
            return connector.kind

        if(index.column() == 2):
            return connector.type       

          
        return None

    def headerData(self, col, orientation, role):
      if orientation == Qt.Horizontal and role == Qt.DisplayRole:
          return self.header[col]
          
      if (role == Qt.TextAlignmentRole):
         return Qt.AlignLeft | Qt.AlignVCenter  
          
      return None
        
class MyDelegate(QItemDelegate):
    def __init__(self, parent):
        print('MyDelegate init')
        super(MyDelegate, self).__init__(parent)
    
    def createEditor(self, parent, option, index):
        if(index.column() == 0):
            return QItemDelegate.createEditor(self, parent, option, index);
      
        if(index.column() == 1):       
            combobox = QComboBox(parent)
            combobox.addItems(['socket', 'plug'])
            #combobox.currentIndexChanged[int].connect(self.currentIndexChanged)
            return combobox
      
        if(index.column() == 2):
            combobox = QComboBox(parent)
            combobox.addItems(['boolean','cmd','number','poly', 'poly-list', 'string'])
            #combobox.currentIndexChanged[int].connect(self.currentIndexChanged)
            return combobox   

        return None   
      
 
    def setEditorData (self, editor, index):


        #self.m_finishedMapper.blockSignals(True);
        text = index.model().data(index, Qt.DisplayRole)    

        if index.column() == 0:
            QItemDelegate.setEditorData(self, editor, index);

        if index.column() == 1:
            _ind = editor.findText(text)
            editor.setCurrentIndex(_ind)

        if index.column() == 2:
            _ind = editor.findText(text)
            editor.setCurrentIndex(_ind)
