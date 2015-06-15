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
from blocks.BlockConnectorShape import BlockConnectorShape

class CommandRule(LinkRule):
   def __init__e(self):
      pass


   def canLink(self,block1, block2, socket1, socket2):
      if (not BlockConnectorShape.isCommandConnector(socket1) or not BlockConnectorShape.isCommandConnector(socket2)):
         return False;
      # We want exactly one before connector
      if (socket1 == block1.getBeforeConnector()):
         return not socket1.hasBlock();
      elif (socket2 == block2.getBeforeConnector()):
         return not socket2.hasBlock();
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


