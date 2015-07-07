from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *

class ConnectorsInfoWnd(QDialog):
  def __init__(self, parent, all_connectors):
    super(ConnectorsInfoWnd, self).__init__(parent)
    loadUi('connector_info.ui', self)   
    
    self.header = ['Label', 'Kind', 'Type'] 
    
    connectors = []
    
    for row in range(len(all_connectors)):      
      connector_info = {}
      connector_node = all_connectors[row]

      label = ''
      if('label' in connector_node.attrib):
        label = connector_node.attrib["label"]   
      connector_info['label'] = label
      
      kind = ''
      if('connector-kind' in connector_node.attrib):
        kind = connector_node.attrib["connector-kind"]   
    
      connector_info['kind'] = kind  
      
      type = ''
      if('connector-type' in connector_node.attrib):
        type = connector_node.attrib["connector-type"]
      
      connector_info['type'] = type  
      connectors.append(connector_info)
    
    model = ConnectorTableModel(self, connectors, self.header)
    self.tableView.setModel(model)

    verticalHeader = self.tableView.verticalHeader();
    #verticalHeader.setDefaultAlignment (Qt.AlignLeft)
    verticalHeader.setResizeMode(QHeaderView.Fixed);
    verticalHeader.setDefaultSectionSize(18);

    self.tableView.setItemDelegate(MyDelegate(self.tableView));
    self.tableView.setEditTriggers(QAbstractItemView.AllEditTriggers)
      
class ConnectorTableModel(QAbstractTableModel):    
    def __init__(self, parent, connectors, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.connectors = connectors

        self.header = header
        
    def rowCount(self, parent):
        return len(self.connectors)
        
    def columnCount(self, parent):
        return len(self.header)

    def flags (self,  index ) :
      if (not index.isValid()):
        return Qt.ItemIsEnabled;

      return Qt.ItemIsDragEnabled |  Qt.ItemIsEnabled |  Qt.ItemIsEditable;
      
    def setData(self, index, value, role=Qt.DisplayRole):
      if (index.isValid() and role == Qt.EditRole):
        connector_info = self.connectors[index.row()]
        if(index.column() == 0):
          connector_info['label'] = value
          
        if(index.column() == 1):
          connector_info['kind'] = value
          
        if(index.column() == 2):
          connector_info['type'] = value
        
        #emit dataChanged(index, index);
        return True;
      return False;

    
    def data(self, index, role):
      if not index.isValid():
          return None
      elif role != Qt.DisplayRole:
          return None
          
      connector_info = self.connectors[index.row()]

      if(index.column() == 0):
        return connector_info['label']
        
      if(index.column() == 1):
        return connector_info['kind']
        
      if(index.column() == 2):
        return connector_info['type']       

          
      return None

    def headerData(self, col, orientation, role):
      if orientation == Qt.Horizontal and role == Qt.DisplayRole:
          return self.header[col]
          
      if (role == Qt.TextAlignmentRole):
         return Qt.AlignLeft | Qt.AlignVCenter  
          
      return None
        
class MyDelegate(QItemDelegate):
  def __inti__(self, parent):
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
        combobox.addItems(['boolean','number', 'string'])
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
