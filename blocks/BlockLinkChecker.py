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
from PyQt4 import QtCore

class BlockLinkChecker():

   MAX_LINK_DISTANCE = 20.0;
   rules = []

   def hasPlugEquivalent(b):
      if (b == None):
         return False;
      hasPlug = b.hasPlug();
      hasBefore = b.hasBeforeConnector();
      # Should have at most one plug-type connector
      assert( not (hasPlug & hasBefore));
      return hasPlug | hasBefore;

   def getPlugEquivalent(b):
      if (not BlockLinkChecker.hasPlugEquivalent(b)):
         return None;
      if (b.hasPlug()):
         return b.getPlug(); 
      return b.getBeforeConnector();

   def getSocketEquivalents(b):
      if (b == None):
         return []
      if (not b.hasAfterConnector()):
      	return b.getSockets();
      socketEquivalents = [];
      for socket in b.getSockets():
         socketEquivalents.append(socket);

      socketEquivalents.append(b.getAfterConnector());
      return socketEquivalents


   def addRule(rule):
      BlockLinkChecker.rules.append(rule);
      #if (rule instanceof WorkspaceListener)
     	#	Workspace.getInstance().addWorkspaceListener((WorkspaceListener)rule);

   '''
    * Factory method for creating BlockLink objects
    * @param block1 one of the Block objects in the potential link
    * @param block2 the other Block object
    * @param socket1 the BlockConnector from block1
    * @param socket2 the BlockConnector from block2
    * @return a BlockLink object storing the potential link between block1 and block2
   '''
   def getBlockLink(block1, block2, socket1, socket2):
      # If these arguments are the same as the last call to getBlockLink, return the old object instead of creating a new one
      if (not
         ((block1.blockID == lastPlugID  and block2.blockID == lastSocketID and socket1 == lastPlug and socket2 == lastSocket) or
   		 (block2.blockID == lastPlugID  and block1.blockID == lastSocketID and socket2 == lastPlug and socket1 == lastSocket))):
         lastLink = BlockLink(block1, block2, socket1, socket2);

      return lastLink;

   '''
   * Gets the screen coordinate of the center of a socket.
   * @param block the RenderableBlock containting the socket
   * @param socket the desired socket
   * @return a Point2D that represents the center of the socket on the screen.
   '''
   def getAbsoluteSocketPoint(block, socket):
      relativePoint = block.getSocketPixelPoint(socket);
      blockPosition = block.getLocationOnScreen();
      return QtCore.QPointF(relativePoint.x() + blockPosition.x(), relativePoint.y() + blockPosition.y());


   def distance(p, q):
      import math
      dx   = p.x() - q.x();         #horizontal difference
      dy   = p.y() - q.y();         #vertical difference
      dist = math.sqrt( dx*dx + dy*dy ); #distance using Pythagoras theorem
      return dist;


   '''
   * Checks if a potential link satisfies ANY of the rules loaded into the link checker
   * @param block1 one Block in the potential link
   * @param block2 the other Block
   * @param socket1 the BlockConnector from block1 in the potential link
   * @param socket2 the BlockConnector from block2
   * @return true if the pairing of block1 and block2 at socket1 and socket2 passes any rules, false otherwise
   '''
   def checkRules(block1, block2, socket1, socket2):
      rulesList = BlockLinkChecker.rules
      currentRule = None;
      foundRule = False;
      for currentRule in rulesList:
         canLink = currentRule.canLink(block1, block2, socket1, socket2);
         if (not currentRule.isMandatory()):
            foundRule |= canLink;
         elif (not canLink):
            return False;

      return foundRule;


   '''
   * Checks to see if a <code>RenderableBlock</code>s can connect to other <code>RenderableBlock</code>s.
   * This would mean that they have <code>BlockConnector</code>s that satisfy at least one of the <code>LinkRule</code>s,
   * and that these sockets are in close proximity.
   * @param rblock1 one of the blocks to check
   * @param otherBlocks the other blocks to check against
   * @return a <code>BlockLink</code> object that gives the two closest matching <code>BlockConnector</code>s in these blocks,
   * or null if no such matching exists.
   '''
   def getLink(rblock1, otherBlocks):
      from blocks.BlockLink import BlockLink

      block1 = Block.getBlock(rblock1.blockID);
      closestSocket1 = None;
      closestSocket2 = None;
      closestBlock2 = None;
      closestDistance = BlockLinkChecker.MAX_LINK_DISTANCE;
      #currentDistance;

      for rblock2 in otherBlocks:
         currentPlug = BlockLinkChecker.getPlugEquivalent(block1);

         block2 = Block.getBlock(rblock2.blockID);
         if (block1 == block2 or not rblock1.isVisible() or not rblock2.isVisible() or rblock1.isCollapsed() or rblock2.isCollapsed()):
            continue;

         currentPlugPoint = None;
         currentSocketPoint = None;
         if (currentPlug != None):
            currentPlugPoint = BlockLinkChecker.getAbsoluteSocketPoint(rblock1, currentPlug);

            for currentSocket in BlockLinkChecker.getSocketEquivalents(block2):
               currentSocketPoint = BlockLinkChecker.getAbsoluteSocketPoint(rblock2, currentSocket);
               currentDistance = BlockLinkChecker.distance(currentPlugPoint,currentSocketPoint);

               if ((currentDistance < closestDistance) and BlockLinkChecker.checkRules(block1, block2, currentPlug, currentSocket)):
                  closestBlock2 = block2;
                  closestSocket1 = currentPlug;
                  closestSocket2 = currentSocket;
                  closestDistance = currentDistance;


         currentPlug = BlockLinkChecker.getPlugEquivalent(block2);
         if (currentPlug != None) :
            currentPlugPoint = BlockLinkChecker.getAbsoluteSocketPoint(rblock2, currentPlug);
            for currentSocket in BlockLinkChecker.getSocketEquivalents(block1):
               currentSocketPoint = BlockLinkChecker.getAbsoluteSocketPoint(rblock1, currentSocket);
               currentDistance = BlockLinkChecker.distance(currentPlugPoint,currentSocketPoint);
               if ((currentDistance < closestDistance) and BlockLinkChecker.checkRules(block1, block2, currentSocket, currentPlug)):
                  closestBlock2 = block2;
                  closestSocket1 = currentSocket;
                  closestSocket2 = currentPlug;
                  closestDistance = currentDistance;

      if (closestSocket1 == None):
         return None;


      return BlockLink.getBlockLink(block1, closestBlock2, closestSocket1, closestSocket2);
