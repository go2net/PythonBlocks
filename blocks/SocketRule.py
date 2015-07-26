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
from blocks.LinkRule import LinkRule

class SocketRule(LinkRule):
   def __init__e(self):
      pass


   def canLink(self,block1, block2, socket1, socket2):
      # Make sure that none of the sockets are connected,
      # and that exactly one of the sockets is a plug.
      if (socket1.hasBlock() or socket2.hasBlock() or
      	not((block1.hasPlug() and block1.getPlug() == socket1) ^
      	  (block2.hasPlug() and block2.getPlug() == socket2))):
         return False;

      # If they both have the same kind, then they can connect
      if (socket1.type == (socket2.type)):
         return True;

      return False;

   def isMandatory(self):
      return False;


   def workspaceEventOccurred(self, e):
      pass
      '''
		// TODO Auto-generated method stub
		if (e.getEventType() == WorkspaceEvent.BLOCKS_CONNECTED) {
			BlockLink link = e.getSourceLink();
			if (link.getLastBlockID() != null && link.getLastBlockID() != Block.NULL &&
				BlockConnectorShape.isCommandConnector(link.getPlug()) && BlockConnectorShape.isCommandConnector(link.getSocket())) {
				Block top = Block.getBlock(link.getPlugBlockID());
				while (top.hasAfterConnector() && top.getAfterConnector().hasBlock())
					top = Block.getBlock(top.getAfterBlockID());
				Block bottom = Block.getBlock(link.getLastBlockID());

				// For safety: if either the top stack is terminated, or
				// the bottom stack is not a starter, don't try to force a link
				if (!top.hasAfterConnector() || !bottom.hasBeforeConnector())
				    return;

				link = BlockLink.getBlockLink(top, bottom, top.getAfterConnector(), bottom.getBeforeConnector());
				link.connect();
			}
		}
      '''


