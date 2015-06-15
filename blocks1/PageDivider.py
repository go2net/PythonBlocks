#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      shijq
#
# Created:     25/04/2015
# Copyright:   (c) shijq 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PyQt4 import QtGui, uic,QtCore
class PageDivider(QtGui.QFrame):

   def __init__(self,leftPage):
      QtGui.QFrame.__init__(self)
      self.leftPage = leftPage
      pass

   def getLeftPage(self):
      return self.leftPage

   def paintEvent(self,event):
      QtGui.QWidget.paintEvent(self,event);
      painter = QtGui.QPainter(self);
		#painter.setColor(DIVIDER_COLOR);
      painter.drawLine(self.width() / 2, 0, self.width() / 2, self.height());
      #if (mouseIn):
      #   g.fillRect(getWidth() / 2 - 1, 0, 3, getHeight());
