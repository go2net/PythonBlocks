from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *


class ConnectorsInfoWnd(QDialog):
  def __init__(self, parent, all_connectors):
    super(ConnectorsInfoWnd, self).__init__(parent)
    loadUi('connector_info.ui', self)   
    
    self.header = ['Label', 'Kind', 'Type'] 
    
    model = ConnectorTableModel(self, all_connectors, self.header)
    self.tableView.setModel(model)

    verticalHeader = self.tableView.verticalHeader();
    #verticalHeader.setDefaultAlignment (Qt.AlignLeft)
    verticalHeader.setResizeMode(QHeaderView.Fixed);
    verticalHeader.setDefaultSectionSize(18);

    self.tableView.setItemDelegate(MyDelegate(self.tableView));
    
    for row in range(len(all_connectors)):      
      
      connector_node = all_connectors[row]

      label = ''
      if('label' in connector_node.attrib):
        label = connector_node.attrib["label"]   
      index = model.index(row, 0, QModelIndex())  
      model.setData(index, label)
  
      kind = ''
      if('connector-kind' in connector_node.attrib):
        kind = connector_node.attrib["connector-kind"]   
      index = model.index(row, 1, QModelIndex())  
      model.setData(index, kind)      
        
      type = ''
      if('connector-type' in connector_node.attrib):
        type = connector_node.attrib["connector-type"]
      index = model.index(row, 2, QModelIndex())    
      model.setData(index, type) 
      
class ConnectorTableModel(QAbstractTableModel):    
    def __init__(self, parent, all_connectors, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.all_connectors = all_connectors
        self.header = header
        
    def rowCount(self, parent):
        return len(self.all_connectors)
        
    def columnCount(self, parent):
        return len(self.header)

    def flags (self,  index ) :
      if (not index.isValid()):
        return Qt.ItemIsEnabled;

      return Qt.ItemIsDragEnabled |  Qt.ItemIsEnabled |  Qt.ItemIsEditable;
      
    def setData(self, index, value, role=Qt.DisplayRole):
      if (index.isValid() and role == Qt.EditRole):
        item = index.internalPointer()
        item.setValue(value)
        #emit dataChanged(index, index);
        return True;
      return False;

    
    def data(self, index, role):
      if not index.isValid():
          return None
      elif role != Qt.DisplayRole:
          return None
          
      data = index.model().data(index, Qt.EditRole);	
      return data
          
    '''          
      connector_node = self.all_connectors[index.row()]
      
  
      if(index.column() == 0):
        if('label' in connector_node.attrib):
          return connector_node.attrib["label"]   
        else:
          return ''      
      
      if(index.column() == 1):
        if('connector-kind' in connector_node.attrib):
          return connector_node.attrib["connector-kind"]   
        else:
          return ''
      if(index.column() == 2):
        if('connector-type' in connector_node.attrib):
          return connector_node.attrib["connector-type"]   
        else:
          return ''        

          
      return self.all_connectors[index.row()][index.column()]
    '''
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
        combobox.addItems(['number', 'string'])
        #combobox.currentIndexChanged[int].connect(self.currentIndexChanged)
        return combobox   

      return None   
      
 
  def setEditorData (self, editor, index):

    #self.m_finishedMapper.blockSignals(True);
    data = index.model().data(index, Qt.EditRole);	
    print(data)
    
    if(index.column() == 0):         
      QItemDelegate.setEditorData(self, editor, index);
 
    if(index.column() == 1 or index.column() == 2):       
      index = editor.findData(data)
      editor.setCurrentIndex(index)
    
