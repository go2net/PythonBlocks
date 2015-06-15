#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      A21059
#
# Created:     04/03/2015
# Copyright:   (c) A21059 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PyQt4 import QtCore,QtGui
from blocks.Block import Block
from blocks.RenderableBlock import RenderableBlock
from blocks.FactoryRenderableBlock import FactoryRenderableBlock


class FactoryCanvas(QtGui.QFrame):

   BORDER_WIDTH = 10

   def __init__(self,parent,name,color=QtGui.QColor(0xCC,0xCC,0xCC)):

      QtGui.QFrame.__init__(self,parent)
      self.setStyleSheet(" background-color: rgba(0,0,0,0); ")

      values = "{r}, {g}, {b}, {a}".format(r = color.red(),
                                           g = color.green(),
                                           b = color.blue(),
                                           a = color.alpha(),
                                           )
      self.components = []
      #self.setFrameShape(QtGui.QFrame.Box)
      #self.setStyleSheet("background-color: rgb(255,0,0); margin:0px; border:1px solid rgb(0, 255, 0); ")
      self.fillPanel = QtGui.QFrame()
      self.fillPanel.setStyleSheet(" background-color: rgba(%s); "%values)

      self.captionPanel = QtGui.QFrame(self)
      #self.captionPanel.setFrameShape(QtGui.QFrame.Box)
      self.captionPanel.setStyleSheet(" background-color: rgba(170,170,127,255); ")
      self.captionPanel.setFixedHeight(25)

      self.label  = QtGui.QLabel(self.captionPanel)
      self.label.setText(name)
      self.label.setAlignment(QtCore.Qt.AlignCenter);

      self.captionPanel.setLayout(QtGui.QVBoxLayout(None))
      self.captionPanel.layout().addWidget(self.label)

      #p = self.captionPanel.palette()
      #p.setColor(self.captionPanel.backgroundRole(),  QtGui.QColor( 0, 0, 255,100 ) )
      #self.captionPanel.setPalette(p)
      #self.captionPanel.setAutoFillBackground(True)


      self.scrollPanel = QtGui.QScrollArea(self)
      self.scrollPanel.setWidget(self.fillPanel)
      self.scrollPanel.setHorizontalScrollBarPolicy (QtCore.Qt.ScrollBarAlwaysOff)
      self.scrollPanel.setStyleSheet(" background-color: rgba(200,200,200,200); ")


      #self.scrollPanel.move(0,25)

      self.parent = parent
      width =parent.width()
      height =parent.height()

      # The highlight of this canvas
      highlight = None
      # The color of this canvas
      self.color = color

      #self.setBackground(QtCore.Qt.gray);
      self.setName (name);

      self.setColor(color);
      #self.mygroupbox = QtGui.QGroupBox(name)

      #self.setWidget(self.mygroupbox)


      self.setLayout(QtGui.QVBoxLayout(None))
      self.layout().setSpacing(0);
      self.layout().setMargin(0);
      self.layout().setContentsMargins(0,0,0,0)
      self.captionPanel.layout().setContentsMargins(0, 0, -1,  0)
      #self.scrollPanel.layout().setContentsMargins( 0, -1, -1, -1)

      self.layout().addWidget(self.captionPanel)
      self.layout().addWidget(self.scrollPanel)

   def setName(self, name):
      QtGui.QWidget.setObjectName(self,name)
      self.repaint()

   def getName(self):
      return self.objectName()

   def setColor(self, color):
      if (color == None):
         self.color = QtCore.Qt.blue
      else:
         self.color = color;

   def addBlock(self,block):
      # make sure block isn't a null instance
      if(block == None or Block.NULL == block.getBlockID()): return
      self.addToBlockLayer(block)

      #print("Add block -- "+Block.ALL_BLOCKS[block.getBlockID()].getGenusName())
      #block.setHighlightParent(self)
      #block.addComponentListener(self)

   def addBlocks(self,blocks):

      index = 0
      y = 0
      for block in blocks:
         #print("Add block -- "+Block.ALL_BLOCKS[block.getBlockID()].getGenusName())
         block.parent = self.fillPanel
         self.layout.addWidget(block)
         #block.move(5,y + 10)
         y += (block.height() + 10)

      width  = self.width()
      height = self.height()

      self.scrollPanel.resize(self.width(),self.height()-self.getCaptionHeight())
      self.fillPanel.resize(self.width(),y)
         #self.canvas.addBlock(block)
      #self.setMinimumSize(200,400);
      # make sure block isn't a null instance
      #if(block == None or Block.NULL == block.getBlockID()): return
      #self.addToBlockLayer(block)

      #print("Add block -- "+Block.ALL_BLOCKS[block.getBlockID()].getGenusName())
      #block.setHighlightParent(self)
      #block.addComponentListener(self)

   def addToBlockLayer(self,c):
      c.setParent(self.fillPanel)
      self.components.append(c)

   def layoutBlocks(self):
      maxWidth = 20;

      tx=FactoryCanvas.BORDER_WIDTH;
      ty=FactoryCanvas.BORDER_WIDTH;

      for rb in self.components:
         if isinstance(rb,RenderableBlock):
            rb.move(tx, ty)
            #rb.setBounds(tx, ty, rb.getBlockWidth(), rb.getBlockHeight());
            ty = ty + FactoryCanvas.BORDER_WIDTH + rb.getBlockHeight();
            #rb.repaint();
            maxWidth = max(maxWidth,rb.getBlockWidth() + FactoryCanvas.BORDER_WIDTH)

      self.resize(maxWidth+FactoryCanvas.BORDER_WIDTH, ty)
      self.fillPanel.resize(maxWidth+FactoryCanvas.BORDER_WIDTH,ty)
      #self.scrollPanel.resize(self.width(),self.height()-25)

      #print("height="+str(ty))

   def getCaptionHeight(self):
      return self.captionPanel.height()

   def getCanvasHeight(self):
      return self.fillPanel.height()

   def getCanvasWidth(self):
      return self.fillPanel.width()

   def resizeEvent(self, event):
      self.scrollPanel.resize(self.width(),self.height()-self.captionPanel.height())
      self.captionPanel.resize(self.width(),self.captionPanel.height())
