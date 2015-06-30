
from PyQt4 import QtGui
from components.propertyeditor.QPropertyModel import  QPropertyModel
from components.propertyeditor.QVariantDelegate import QVariantDelegate

class QPropertyEditorWidget(QtGui.QTreeView):
  def __inti__(self, parent):

    super(QPropertyEditorWidget, self).__init__(parent)

    self.m_model = QPropertyModel(self);		
    self.setModel(self.m_model);
    self.setItemDelegate(QVariantDelegate(self));
