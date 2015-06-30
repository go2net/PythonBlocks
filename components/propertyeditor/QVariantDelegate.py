from PyQt4 import QtGui

class QVariantDelegate(QtGui.QItemDelegate):
  def __inti__(self, parent):
    super(QVariantDelegate, self).__init__(parent)
