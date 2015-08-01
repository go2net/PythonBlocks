
from PyQt4 import QtGui
from blocks.RenderableBlock import RenderableBlock
from blocks.BlockUtilities import BlockUtilities
from blocks.Block import Block

class FactoryRenderableBlock(RenderableBlock):
   factoryRBs = {}
   def __init__(self):
      RenderableBlock.__init__(self)
      pass

   @classmethod
   def from_block(cls, workspaceWidget, block, isLoading=False,back_color=QtGui.QColor(225,225,225,255)):
     obj = super(FactoryRenderableBlock, cls).from_block(workspaceWidget,block,False, back_color)
     obj.setBlockLabelUneditable()
     obj.createdRB = None
     obj.createdRB_dragged = False

     FactoryRenderableBlock.factoryRBs[block.getGenusName()] = obj

     return  obj
     
   @classmethod     
   def from_blockID(cls, workspaceWidget, blockID, isLoading=False,back_color=QtGui.QColor(225,225,225,255)):
     return  FactoryRenderableBlock.from_block(workspaceWidget,Block.getBlock(blockID),False, back_color)
     
     
   def createNewInstance(self):
      rb = BlockUtilities.cloneBlock(self.getBlock())
      return rb


   def mousePressEvent(self, event):
      if(self.workspaceWidget == None): return
      
      self.workspaceWidget.OnPressed(self.workspaceWidget.active_button)
      self.createdRB = self.createNewInstance();
      self.createdRB.setParent(self.parentWidget())
      self.createdRB.move(self.x(), self.y());
      self.createdRB.mousePressEvent(event);
      self.mouseDragged(event); # immediately make the RB appear under the mouse cursor


   def mouseReleaseEvent(self, event):
      if(self.createdRB != None):
         if(not self.createdRB_dragged):
            self.createdRB.setParent(None);
         else:
            self.createdRB.mouseReleaseEvent(event);

         self.createdRB_dragged = False;

   def mouseMoveEvent(self, event):
      if(self.createdRB != None):
         self.createdRB.mouseMoveEvent(event);


   def mouseDragged(self, event):
      if(self.createdRB != None):
         self.createdRB.mouseDragged(event);
         self.createdRB_dragged = True;
