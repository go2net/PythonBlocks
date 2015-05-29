#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      A21059
#
# Created:     05/03/2015
# Copyright:   (c) A21059 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PyQt4 import QtGui, QtCore
from Blocks.WorkspaceWidget import WorkspaceWidget

class TrashCan(QtGui.QWidget,WorkspaceWidget):

   def __init__(self,parent,trashCanImage, openedTrashCanImage):
      QtGui.QWidget.__init__(self,parent)

      self.setMouseTracking(True)

      self.workspace = parent
      self.tcImage = trashCanImage
      self.openedTcImage = openedTrashCanImage;
      self.currentImage = self.tcImage;
      width=0
      height=0

      if(self.tcImage.width() > self.openedTcImage.width()):
         width = self.tcImage.width();
      else:
         width = self.openedTcImage.width();

      if(self.tcImage.height() > self.openedTcImage.height()):
         height = self.tcImage.height();
      else:
         height = self.openedTcImage.height();

      if(width >0 and height > 0):
         self.resize(width,height);
         #setPreferredSize(Dimension(width,height))
      else:
         self.resize(150,200);
         #setPreferredSize(Dimension(150,200));
      #self.setStyleSheet("background-color: rgb(255, 255, 0);")

      #layout = self.layout()

      #self.resizeEvent = onResize

      #Set the widget's location.
      #self.setLocation(500, 400);

		#addMouseListener(this);
		#Workspace.getInstance().addComponentListener(this);

   def paintEvent(self, event):
      painter = QtGui.QPainter();
      painter.begin(self)
      if(self.currentImage ==  None):
      	painter.setPen(currentColor);
      	painter.fillRect(0,0,150,200);
      else:
      	painter.drawPixmap(QtCore.QPoint(0,0),self.currentImage);
      painter.end()

   def blockEntered(self,block):
      '''
       * Called when a RenderableBlock is being dragged and goes from being
       * outside this Widget to being inside the Widget.
       * @param block the RenderableBlock being dragged
      '''
      bitmap = QtGui.QPixmap("support\\DeleteCursor.png")
      cursor = QtGui.QCursor(bitmap,0,0)
      #cursor.setMask(cursor.mask())
      QtGui.QApplication.setOverrideCursor(cursor);
      self.currentImage = self.openedTcImage
      self.repaint();

   def blockExited(self, block):
      '''
      * Called when a RenderableBlock that was being dragged over this Widget
      * goes from being inside this Widget to being outside the Widget.
      * @param block the RenderableBlock being dragged
      '''
      #self.currentColor = Color.BLACK;
      self.currentImage = self.tcImage;
      QtGui.QApplication.restoreOverrideCursor()
      self.repaint();

   def rePosition(self):
      if (self.parent() != None):
         self.move(self.parent().width() - self.width() - 26, self.parent().height() - self.height() - 26 )
      self.repaint()


   def blockDropped(self, block):
      from Blocks.BlockUtilities import BlockUtilities
      # remove the block from the land of the living
      BlockUtilities.deleteBlock(block);
      #selfcurrentColor = Color.BLACK;
      self.currentImage = self.tcImage;
      #self.revalidate();
      QtGui.QApplication.restoreOverrideCursor()
      self.repaint();

   def contains(self,point):
      return self.rect().contains(point)
