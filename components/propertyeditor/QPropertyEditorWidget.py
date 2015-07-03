
from PyQt4 import QtGui
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
    self.setEditTriggers(QAbstractItemView.AllEditTriggers)

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


    
