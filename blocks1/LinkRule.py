#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      shijq
#
# Created:     26/03/2015
# Copyright:   (c) shijq 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PyQt4 import QtGui,QtCore, uic

class LinkRule(QtCore.QObject):
   def canLink(self, block1, block2, socket1, socket2):
      pass

   def isMandatory(self):
      pass