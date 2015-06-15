#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      A21059
#
# Created:     10/03/2015
# Copyright:   (c) A21059 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PyQt4 import QtGui,QtCore, uic

class ConnectorTag():
   def __init__(self,connector):
      self.aLoc = QtCore.QPoint(0,0);
      self.dimension = None;
      self.connector = connector;
      self.label = None
      self.zoom = 1.0;

   def getSocket(self):
      return self.connector;

   def setLabel(self,label):
   	self.label = label;

   def getLabel(self):
   	return self.label;

   def getDimension(self):
      if(self.dimension == None):
         return None;
      else:
         return QtCore.QSize((self.dimension.width()/self.zoom), (int)(self.dimension.height()/self.zoom));

   def setDimension(self,dimension):
   	self.dimension=dimension;


   def setAbstractLocation(self, p):
      # we can't do aLoc=loc because then we can mutate aLoc by mutating loc
      self.aLoc = p;

   def getAbstractLocation(self):
      #w e can't do aLoc=loc because then we can mutate aLoc by mutating loc
      return self.aLoc;

   def rescale(self, x):
   	return x*self.zoom

   def getPixelLocation(self):
      return QtCore.QPoint(self.rescale(self.aLoc.x()), self.rescale(self.aLoc.y()));

if __name__ == '__main__':
    main()
