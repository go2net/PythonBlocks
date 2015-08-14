#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      A21059
#
# Created:     06/03/2015
# Copyright:   (c) A21059 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PyQt4 import QtGui
from blocks.RenderableBlock import RenderableBlock
from blocks.BlockUtilities import BlockUtilities
from blocks.Block import Block

class FactoryRenderableBlock(RenderableBlock):
   factoryRBs = {}
   def __init__(self,workspaceWidget ):
      RenderableBlock.__init__(self, workspaceWidget)
      pass
      #dragHandler = new JComponentDragHandler(this);

   @classmethod
   def from_block(cls, workspaceWidget, block, isLoading=False,back_color=QtGui.QColor(225,225,225,255)):
     obj = super(FactoryRenderableBlock, cls).from_block(workspaceWidget,block,False, back_color)
     obj.setBlockLabelUneditable()
     obj.createdRB = None
     obj.createdRB_dragged = False
     obj.child_list = []
     FactoryRenderableBlock.factoryRBs[block.getGenusName()] = obj
     return  obj
     
   @classmethod     
   def from_blockID(cls, workspaceWidget, blockID, isLoading=False,back_color=QtGui.QColor(225,225,225,255)):
     return  FactoryRenderableBlock.from_block(workspaceWidget,Block.getBlock(blockID),False, back_color)
     
     
   def createNewInstance(self):
      rb = BlockUtilities.cloneBlock(Block.getBlock(self.blockID), self.workspaceWidget)
      self.child_list.append(rb)
      return rb


   def mousePressEvent(self, event):
      from blocks.Workspace import Workspace
      if(self.workspaceWidget == None): return
      
      Workspace.ws.factory.OnPressed(Workspace.ws.factory.active_button)

      # create new renderable block and associated block
      self.createdRB = self.createNewInstance();
      # add this new rb to parent component of this
      #self.getParent().add(createdRB,0);
      self.createdRB.setParent(self.parent())
      # set the parent widget of createdRB to parent widget of this
      # createdRB not really "added" to widget (not necessary to since it will be removed)
      #self.createdRB.setParentWidget(this.getParentWidget());
      self.createdRB.setParent(self.parentWidget())
      #self.createdRB.setWorkspaceWidget(self.getWorkspaceWidget())
      # set the location of new rb from this
      self.createdRB.move(self.x(), self.y());
      # send the event to the mousedragged() of new block
      #MouseEvent newE = SwingUtilities.convertMouseEvent(this, e, createdRB);
      self.createdRB.mousePressEvent(event);
      self.mouseDragged(event); # immediately make the RB appear under the mouse cursor

     #super(DragButton, self).mousePressEvent(event)

   #def mouseMoveEvent(self, event):
   #   if event.buttons() == QtCore.Qt.LeftButton:
   #      pass
         # adjust offset from clicked point to origin of widget
         #currPos = self.mapToGlobal(self.pos())
         #globalPos = event.globalPos()
         #diff = globalPos - self.__mouseMovePos
         #newPos = self.mapFromGlobal(currPos + diff)
         #self.move(newPos)

         #self.__mouseMovePos = globalPos

      #super(DragButton, self).mouseMoveEvent(event)

   def mouseReleaseEvent(self, event):
      if(self.createdRB != None):
         if(not self.createdRB_dragged):
            self.createdRB.setParent(None);
            #parent.remove(createdRB);
            #parent.validate();
            #parent.repaint();
         else:
            # translate this e to a MouseEvent for createdRB
            #newE = SwingUtilities.convertMouseEvent(this, e, createdRB);
            self.createdRB.mouseReleaseEvent(event);

         self.createdRB_dragged = False;

   def mouseMoveEvent(self, event):
      if(self.createdRB != None):
         self.createdRB.mouseMoveEvent(event);


   def mouseDragged(self, event):
      if(self.createdRB != None):
         # translate this e to a MouseEvent for createdRB
         #newE = SwingUtilities.convertMouseEvent(this, e, createdRB);
         self.createdRB.mouseDragged(event);
         self.createdRB_dragged = True;
