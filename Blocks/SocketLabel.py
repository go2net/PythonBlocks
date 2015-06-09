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
from Blocks.BlockLabel import BlockLabel
from Blocks.BlockConnector import BlockConnector
from PyQt4 import QtGui
from Blocks.BlockConnectorShape import BlockConnectorShape

class SocketLabel(BlockLabel):


   def __init__(self, socket, initLabelText, labelType, isEditable, blockID):
      BlockLabel.__init__(self, initLabelText, '', '', labelType, isEditable, blockID, False, QtGui.QColor(190, 250, 125));
      self.socket = socket;

   '''
   * Returns true if the socket label should not be added to this.  Conditions for ignoring socket labels are:
   * 1.  the specified socket is a bottom socket
   * 2.  the specified socket has an empty label
   * @param socket the BlockConnector to test
   * @return true if the specified socket should have a corresponding Blocklabel instance added to this.
    '''
   def ignoreSocket(socket):
      return (socket.getPositionType() == BlockConnector.PositionType.BOTTOM) or socket.getLabel() == ("");

   def update(self,socketPoint):
      if(SocketLabel.ignoreSocket(self.socket)):return;
      #abstarct location so we need to tranform it
      x = 0;
      y = 0;
      if (BlockConnectorShape.isCommandConnector(self.socket)):
         #command socket
         x = -8  - BlockConnectorShape.COMMAND_INPUT_BAR_WIDTH + socketPoint.x();
         y = -4 + socketPoint.y();
      else:
         # data socket
         x = -4  - BlockConnectorShape.getConnectorDimensions(self.socket).width() + socketPoint.x();
         y = -8 + socketPoint.y();

      x = - self.getAbstractWidth() + x;
      self.setPixelLocation(self.rescale(x), self.rescale(y));


	#@Override
   def textChanged(self,text):
      # Prevents running this when sockets are null.
      # Sockets can be null during loading.
      return
      if (self.socket != None):
         socket.setLabel(text);
         BlockLabel.textChanged(self,text);


