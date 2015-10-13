from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
import os

class ImagesInfoWnd(QDialog):
    def __init__(self, treeModel, genus):
        from MainWnd import MainWnd
        super(ImagesInfoWnd, self).__init__(MainWnd.getInstance())
        self.genus = genus
        self.treeModel = treeModel
        dirname, filename = os.path.split(os.path.abspath(__file__))
        loadUi(dirname+'\\connector_info.ui', self)   
        
        self.btnAdd.clicked.connect(self.onAddImage)
        self.btnOk.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        
        self.header = ['#','Image', 'Location', 'Size', 'Editable', 'Wraptext'] 

        self.blockImages= []
            
        for loc, img in genus.blockImageMap.items():
            self.blockImages.append(img)
    
        model = ImageTableModel(self, self.blockImages, self.header)
        self.tableView.setModel(model)

        verticalHeader = self.tableView.verticalHeader();
        #verticalHeader.setDefaultAlignment (Qt.AlignLeft)
        verticalHeader.setResizeMode(QHeaderView.Fixed);
        verticalHeader.setDefaultSectionSize(18)    
        
        delegate = MyDelegate(self.tableView)
        self.tableView.setItemDelegate(delegate)
        self.tableView.setEditTriggers(QAbstractItemView.AllEditTriggers)

    def onAddImage(self):
        self.tableView.model().addImage()
        #return self.createIndex(node.row(), 1, node)   
        #self.tableView.itemDelegate().dataChanged.emit(self.tableView)
      
class ImageTableModel(QAbstractTableModel):    
    def __init__(self, parent, blockImages, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.blockImages = blockImages
        self.header = header
        self.InfoWnd = parent
    
    def addImage(self):
        from blocks.BlockImageIcon import BlockImageIcon
        img = BlockImageIcon('', 'test', None, 32, 32, False, False)
        self.blockImages.append(img)
        index = QModelIndex ()
        self.insertRow(len(self.blockImages), index)
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index) 
    
    def rowCount(self, parent):
        return len(self.blockImages)
        
    def columnCount(self, parent):
        return len(self.header)

    def flags (self,  index ) :
        if (not index.isValid()):
            return Qt.ItemIsEnabled
            
        if (index.column() == 0):
            return Qt.ItemIsEnabled |  Qt.ItemIsSelectable 
            
        return Qt.ItemIsDragEnabled |  Qt.ItemIsEnabled |  Qt.ItemIsEditable;
      
    def setData(self, index, value, role=Qt.DisplayRole):
        if (index.isValid() and role == Qt.EditRole):
            image = self.blockImages[index.row()]
            if(image == None): return False
            if(index.column() == 0):
              image.label = value
              
            if(index.column() == 1):
              image.kind = value
              
            if(index.column() == 2):
              image.type = value

            #emit dataChanged(index, index);
            self.InfoWnd.treeModel.showBlock(self.InfoWnd.genus)
            return True;
        return False
    
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
          
        #image = self.blockImageMap[index.row()]

        if(index.column() == 0):
            return str(index.row())
        else:
            return ''
        
        '''  
        if(index.column() == 1):
        return image.kind

        if(index.column() == 2):
        return image.type       

        '''
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
          return self.header[col]
          
        if (role == Qt.TextAlignmentRole):
         return Qt.AlignLeft | Qt.AlignVCenter  
          
        return None

    def insertRow(self, row, parent): 
        return self.insertRows(row, 1, parent) 

    def insertRows(self, row, count, parent): 
        print('insertRows')
        self.beginInsertRows(parent, row, (row + (count - 1))) 
        self.endInsertRows() 
        return True 
        
class MyDelegate(QItemDelegate):
    def __init__(self, parent):
        super(MyDelegate, self).__init__(parent)
    
    def createEditor(self, parent, option, index):
        #if(index.column() == 0):
        #    return QItemDelegate.createEditor(self, parent, option, index);
      
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
