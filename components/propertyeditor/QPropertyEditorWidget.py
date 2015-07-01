
from PyQt4 import QtGui, QtCore
#from components.propertyeditor.QPropertyModel import  QPropertyModel
#from components.propertyeditor.QVariantDelegate import QVariantDelegate

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class QPropertyEditorWidget(QtGui.QTreeView):
  def __inti__(self, parent):
    super(QPropertyEditorWidget, self).__init__(parent)
    
    #self.m_model = QPropertyModel(self);		
    #self.setModel(self.m_model);
    #self.setItemDelegate(QVariantDelegate(self));
    # create objects


  def init(self):
    self.setAlternatingRowColors(True);

    p = self.palette();
    p.setColor( QPalette.AlternateBase, QColor(226, 237, 253) );
    self.setPalette(p);   


  def drawRow (self, painter,option, index) :

    newOption = option
    if (True):
      #painter.fillRect(option.rect, QtCore.Qt.green);
      #newOption.palette.setBrush( QPalette.AlternateBase, Qt.green);
      
      painter.setPen(QColor(240, 240, 240) );
      painter.drawRect(option.rect);
    else:
      newOption.palette.setColor( QPalette.Base, QColorr(0, 0, 255) );
      newOption.palette.setColor( QPalette.Base, QColor(0, 0, 200) );

    QtGui.QTreeView.drawRow(self, painter, newOption, index);


        
####################################################################
class MyDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)
        print('MyDelegate')

    def paint(self, painter, option, index):
        painter.save()

        # set background color
        painter.setPen(QPen(Qt.NoPen))
        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(Qt.red))
        else:
            painter.setBrush(QBrush(Qt.white))
        painter.drawRect(option.rect)

        # set text color
        painter.setPen(QPen(Qt.black))
        value = index.data(Qt.DisplayRole)
        if value:
            print(value)
            text = str(value)
            painter.drawText(option.rect, Qt.AlignLeft, text)

        painter.restore()

####################################################################
class MyListModel(QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.listdata = datain

    def rowCount(self, parent=QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return self.listdata[index.row()]
        else:
            return None # QVariant()
    
