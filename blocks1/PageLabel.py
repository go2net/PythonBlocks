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
from blocks.BlockLabel import BlockLabel
from PyQt4 import QtGui

class PageLabel(BlockLabel):
   def __init__(self,initLabelText, labelType, isEditable, blockID):
      BlockLabel.__init__(self,initLabelText, '', '', labelType, isEditable, blockID, False, QtGui.QColor(255,255,0));

   def update(self):
      x = 5;
      y = 5;

      rb = RenderableBlock.getRenderableBlock(getBlockID());
      if (rb != None): x += descale(rb.getControlLabelsWidth());

      self.setPixelLocation( rescale(x), rescale(y));


if __name__ == '__main__':
    main()
