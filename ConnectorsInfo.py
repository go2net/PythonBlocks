from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *

class ConnectorsInfo(QDialog):
  def __init__(self, parent):
    super(ConnectorsInfo, self).__init__(parent)
    loadUi('connector_info.ui', self)
