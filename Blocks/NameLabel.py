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
from Blocks.BlockLabel import BlockLabel
from Blocks.BlockConnectorShape import BlockConnectorShape
from PyQt4 import QtGui

class NameLabel(BlockLabel):

   def __init__(self, initLabelText, labelType, isEditable, blockID):
      BlockLabel.__init__(self,initLabelText, labelType, isEditable, blockID, True, QtGui.QColor(255,255,225))
      self.blockID = blockID;


   def update(self):
      from Blocks.RenderableBlock import RenderableBlock
      rb = RenderableBlock.getRenderableBlock(self.blockID);
      if (rb != None):
         x = 0;
         y = 0;
         if(rb.getBlock().isCommandBlock()): x+=5;
         if(rb.getBlock().isDeclaration()): x+=12;
         if(rb.getBlock().hasPlug()):
            x+=4+BlockConnectorShape.getConnectorDimensions(rb.getBlock().getPlug()).width();
         if(rb.getBlock().isInfix()):
            if(not rb.getBlock().getSocketAt(0).hasBlock()):
                x+=30;
            else:
               if(rb.getSocketSpaceDimension(rb.getBlock().getSocketAt(0)) != None):
                  x+= rb.getSocketSpaceDimension(rb.getBlock().getSocketAt(0)).width();

         if(rb.getBlockWidget()==None):
            y+=rb.getAbstractBlockArea().controlPointRect().height()/2;
         else:
            y+=8;

         if(rb.getBlock().isCommandBlock()):
            y-=2;

         if(rb.getBlock().hasPageLabel() and rb.getBlock().hasAfterConnector()):
            y-=BlockConnectorShape.CONTROL_PLUG_HEIGHT;

         if(not rb.getBlock().hasPageLabel()):
            y-=self.getAbstractHeight()/2;

         # Comment Label and Collapse Label take up some additional amount of space
         x += rb.getControlLabelsWidth();

         # if block is collapsed keep the name label from moving
         y += BlockConnectorShape.CONTROL_PLUG_HEIGHT/2 if rb.isCollapsed() else 0;
         #y+=3
         x=self.rescale(x);
         y=self.rescale(y);

         self.setPixelLocation(x, y);


if __name__ == '__main__':
    main()
