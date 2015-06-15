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

from PyQt4 import QtGui
class BlockControlLabel(QtGui.QLabel):

   def __init__(self,blockID):
      QtGui.QLabel.__init__(self)
      self.blockID = blockID;
      self.active = False
      #self.setFont(Font("Courier", Font.BOLD, (int)(14)));
      #self.setForeground(Color(255,255,255));
      #self.setBorder(BorderFactory.createLineBorder(Color.gray));#show white border
      #self.setOpaque(false);
      #self.setHorizontalAlignment(SwingConstants.CENTER );
      #self.setVerticalAlignment(SwingConstants.CENTER );
      #self.addMouseListener(this);
      #self.setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR));

   def isActive(self):
      return self.active;

   def getBlockID(self):
      return self.blockID;


   def update(self):
      from blocks.RenderableBlock import RenderableBlock
      rb = RenderableBlock.getRenderableBlock(self.getBlockID());

      if (rb != None):
         x = 0;
         y = 0;

         y += (rb.getBlockHeight()/rb.getZoom() - 22 + (BlockConnectorShape.CONTROL_PLUG_HEIGHT if self.isActive() else 0));
         x += 12;
         x=rb.rescale(x);
         y=rb.rescale(y);

         self.move(x, y);
         self.resize(rb.rescale(14), rb.rescale(14));

         if (self.isActive()):
            self.setText("+");
         else:
            self.setText("-");

if __name__ == '__main__':
    main()
