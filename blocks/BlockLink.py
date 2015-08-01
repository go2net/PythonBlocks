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
from blocks.Block import Block
class BlockLink():

   lastLink = None
   lastPlugID = None
   lastSocketID = None
   lastPlug = None
   lastSocket = None
   lastPlugBlockID = None

   def __init__(self,block1, block2, socket1, socket2):
      self.clickSound = None
      self.peer_socket = socket2
      self.peer_block = block2
      self.socket = socket1
      self.block = block1

      isPlug1 = (block1.hasPlug() and block1.getPlug() == socket1) or (block1.hasBeforeConnector() and block1.getBeforeConnector() == socket1);
      isPlug2 = (block2.hasPlug() and block2.getPlug() == socket2) or (block2.hasBeforeConnector() and block2.getBeforeConnector() == socket2);
      if (not (isPlug1 ^ isPlug2)):
         # bad news... there should be only one plug
         assert(False);
      elif (isPlug1):
         self.plug = socket1;
         self.socket = socket2;
         self.plugBlockID = block1.blockID;
         self.socketBlockID = block2.blockID;
      else:
      	self.plug = socket2;
      	self.socket = socket1;
      	self.plugBlockID = block2.blockID;
      	self.socketBlockID = block1.blockID;

      BlockLink.lastPlugID = self.plugBlockID;
      BlockLink.lastSocketID = self.socketBlockID;
      BlockLink.lastPlug = self.plug;
      BlockLink.lastSocket = self.socket;
      BlockLink.lastPlugBlockID = Block.NULL;

   def equal(self,link):
      if(link == None): return False

      return (self.socket == link.socket and
             self.block == link.block and
             self.peer_socket == link.peer_socket and
             self.peer_block == link.peer_block)


   def getPlug(self):
   	return self.plug;

   def getSocket(self):
   	return self.socket;

   def getPlugBlockID(self):
      return self.plugBlockID;

   def getSocketBlockID(self):
      return self.socketBlockID;

   def getLastBlockID(self):
      return self.lastPlugBlockID;

   def connect(self):
      from blocks.RenderableBlock import RenderableBlock
      from blocks.BlockLinkChecker import BlockLinkChecker
      from blocks.BlockConnectorShape import BlockConnectorShape
      # Make sure to disconnect any connections that are going to be overwritten
      # by this new connection.  For example, if inserting a block between two
      # others, make sure to break that original link.*/
      if (self.socket.hasBlock()):
         # save the ID of the block previously attached to (in) this
      	# socket.  This is used by insertion rules to re-link the replaced
      	# block to the newly-inserted block.
         self.lastPlugBlockID = self.socket.blockID;

         # break the link between the socket block and the block in that socket
         plugBlock = Block.getBlock(self.lastPlugBlockID);
         plugBlockPlug = BlockLinkChecker.getPlugEquivalent(plugBlock);
         if (plugBlockPlug != None and plugBlockPlug.hasBlock()):
            socketBlock = Block.getBlock(plugBlockPlug.blockID);
            link = BlockLink.getBlockLink(plugBlock, socketBlock, plugBlockPlug, self.socket);
            link.disconnect();
      		# don't tell the block about the disconnect like we would normally do, because
      		# we don't actually want it to have a chance to remove any expandable sockets
      		# since the inserted block will be filling whatever socket was vacated by this
      		# broken link.
      		#NOTIFY WORKSPACE LISTENERS OF DISCONNECTION (not sure if this is great because the connection is immediately replaced)
      		#Workspace.getInstance().notifyListeners(new WorkspaceEvent(RenderableBlock.getRenderableBlock(socketBlock.blockID).getParentWidget(), link, WorkspaceEvent.BLOCKS_DISCONNECTED));

      if (self.plug.hasBlock()):
      	# in the case of insertion, breaking the link above will mean that
      	# the plug shouldn't be connected by the time we reach here.  This
      	# exception will only be thrown if the plug is connected even
      	# after any insertion-esq links were broken above
         #throw new RuntimeException("trying to link a plug that's already connected somewhere.");
         return


      # actually form the connection

      self.plug.setConnectorBlockID(self.socketBlockID);
      self.socket.setConnectorBlockID(self.plugBlockID);

      # notify renderable block of connection so it can redraw with stretching
      socketRB = RenderableBlock.getRenderableBlock(self.socketBlockID);
      socketRB.blockConnected(self.socket, self.plugBlockID);

      if (self.getLastBlockID() != None and
			self.getLastBlockID() != Block.NULL and
			BlockConnectorShape.isCommandConnector(self.getPlug()) and
			BlockConnectorShape.isCommandConnector(self.getSocket())):
         top = Block.getBlock(self.getPlugBlockID());
         while (top.hasAfterConnector() and top.getAfterConnector().hasBlock()):
            top = Block.getBlock(top.getAfterBlockID());
         bottom = Block.getBlock(self.getLastBlockID());

         # For safety: if either the top stack is terminated, or
         # the bottom stack is not a starter, don't try to force a link
         if (not top.hasAfterConnector() or not bottom.hasBeforeConnector()):
            return;

         link = BlockLink.getBlockLink(top, bottom, top.getAfterConnector(), bottom.getBeforeConnector());
         link.connect();

      if(self.clickSound != None):
         # System.out.println("playing click sound");
         clickSound.play();



   def disconnect(self):
      self.plug.setConnectorBlockID(Block.NULL);
      self.socket.setConnectorBlockID(Block.NULL);



   def getBlockLink(block1, block2, socket1, socket2):
      # If these arguments are the same as the last call to getBlockLink, return the old object instead of creating a new one
      #if not(
      #   (block1.blockID == (BlockLink.lastPlugID) and block2.blockID == (BlockLink.lastSocketID) and socket1 == (BlockLink.lastPlug) and socket2 == (BlockLink.lastSocket)) or
      #   (block2.blockID == (BlockLink.lastPlugID) and block1.blockID == (BlockLink.lastSocketID) and socket2 == (BlockLink.lastPlug) and socket1 == (BlockLink.lastSocket))):
      BlockLink.lastLink = BlockLink(block1, block2, socket1, socket2);

      return BlockLink.lastLink;
