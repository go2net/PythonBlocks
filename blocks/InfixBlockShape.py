
from PyQt4 import QtCore

from blocks.BlockShape import BlockShape
from blocks.BlockConnector import BlockConnector
from blocks.BlockShapeUtil import BlockShapeUtil
from blocks.BlockConnectorShape import BlockConnectorShape
from blocks.Block import Block

class InfixBlockShape(BlockShape):

   def __init__(self,rb):
      BlockShape.__init__(self,rb)
      self.maxX=0

   def makeBottomSide(self):
      '''
      * Overrided from BlockShape.
      * Takes into account the need to resize the dimensions of an infix block for various cases.
      '''
      from blocks.RenderableBlock import RenderableBlock
      from blocks.BlockShapeUtil import BlockShapeUtil
      # Reset the maximum X-coordinate so the infix block can resize if you remove blocks within it
      self.maxX = 0;

      # start bottom-right
      self.setEndPoint(self.gpBottom, self.botLeftCorner, self.topLeftCorner, True);

      #curve down and right
      BlockShapeUtil.cornerTo(self.gpBottom, self.botLeftCorner, self.botRightCorner, self.blockCornerRadius);



      # BOTTOM SOCKETS
      # for each socket in the iterator
      socketCounter = 0; #need to use this to determine which socket we're on
      for curSocket in self.block.getSockets():
         #if bottom socket
         if (curSocket.getPositionType() == BlockConnector.PositionType.BOTTOM):

            # move away from bottom left corner
            if(socketCounter > 0):
               self.gpBottom.lineTo(
                         self.gpBottom.currentPosition().x() + BlockShape.BOTTOM_SOCKET_MIDDLE_SPACER,
                         self.gpBottom.currentPosition().y());
            else:
                 self.gpBottom.lineTo(
                         self.gpBottom.currentPosition().x() + BlockShape.BOTTOM_SOCKET_SIDE_SPACER,
                         self.gpBottom.currentPosition().y());


            # move down so bevel doesn't screw up from connecting infinitely sharp corner
            # as occurs from a curved port
            BlockShapeUtil.lineToRelative(self.gpBottom, 0, -0.1);

            #//////////////////////
            #//begin drawing socket
            #//////////////////////

            if(curSocket.blockID == Block.NULL):
               # draw first socket - up left side
               leftSocket = BlockShape.BCS.addDataSocketUp(self.gpBottom, curSocket.type, True);
               self.rb.updateSocketPoint(curSocket, leftSocket);
               # System.out.println("socket poitn: "+rb.getSocketPoint(curSocket));

               # System.out.println("socket poitn leftsocket: "+leftSocket);

               # draw left standard empty socket space - top side
               self.gpBottom.lineTo(
                         self.gpBottom.currentPosition().x() + BlockShape.BOTTOM_SOCKET_SIDE_SPACER,
                         self.gpBottom.currentPosition().y());


               #draw first socket - down right side
               BlockShape.BCS.addDataSocket(self.gpBottom, curSocket.type, False);
               #rb.updateSocketPoint(curSocket, rightSocket);
            else: # there is a connected block

               connectedBlock = Block.getBlock(curSocket.blockID);
               connectedRBlock = RenderableBlock.getRenderableBlock(curSocket.blockID);
               if(connectedBlock == None or connectedRBlock== None) : continue

               # calculate and update the new socket point
               # update the socket point of this cursocket which should now adopt the plug socket point of its
               # connected block since we're also adopting the left side of its shape

               # Use coordinates when the zoom level is 1.0 to calculate socket point
               unzoomX = connectedRBlock.getSocketPixelPoint(connectedBlock.getPlug()).x()/connectedRBlock.getZoom();
               unzoomY = connectedRBlock.getSocketPixelPoint(connectedBlock.getPlug()).y()/connectedRBlock.getZoom();
               connectedBlockSocketPoint = QtCore.QPoint(unzoomX, unzoomY);
               currentPoint = self.gpBottom.currentPosition();
               newX = connectedBlockSocketPoint.x() + abs(connectedBlockSocketPoint.x() - currentPoint.x());
               newY = connectedBlockSocketPoint.y() + abs(connectedRBlock.getBlockHeight()/connectedRBlock.getZoom() - currentPoint.y());
               self.rb.updateSocketPoint(curSocket, QtCore.QPoint(newX, newY));

               self.gpBottom.currentPosition().x()

               connectedBlockShape = RenderableBlock.getRenderableBlock(curSocket.blockID).getBlockShape();
               #append left side of connected block
               
               connectedBlockShape.reformArea()
               BlockShapeUtil.appendPath(self.gpBottom, connectedBlockShape.getLeftSide(), False);
               connectedBlockShape.getLeftSide().currentPosition()
               self.gpBottom.currentPosition().x()
               # append right side of connected block (more complicated)
               if(connectedBlock.getNumSockets() == 0 or connectedBlock.isInfix()):
                  #  append top side of connected block
                  BlockShapeUtil.appendPath(self.gpBottom, connectedBlockShape.getTopSide(), False);
                  BlockShapeUtil.appendPath(self.gpBottom, connectedBlockShape.getRightSide(), False);
               else:
                  # iterate through the sockets of the connected block, checking if
                  # it has blocks connected to them
                  self.appendRightSidePath(self.gpBottom, connectedBlock, connectedBlockShape);


               # Updates the maximum X-coordinate and sets the current point to self.maxX
               if(self.maxX < self.gpBottom.currentPosition().x()):
                  self.maxX = self.gpBottom.currentPosition().x();

               self.gpBottom.lineTo(self.maxX, self.gpBottom.currentPosition().y());


            # bump down so bevel doesn't screw up
            BlockShapeUtil.lineToRelative(self.gpBottom, 0, 0.1);

            # System.out.println("gpbottom starting point: "+gpBottom.currentPosition());

            # draw RIGHT to create divider ////
            if(socketCounter < self.block.getNumSockets()-1):
               self.gpBottom.lineTo( #need to add the width of the block label.  warning: this assumes that there is only one block label
                      self.gpBottom.currentPosition().x() + BlockShape.BOTTOM_SOCKET_MIDDLE_SPACER + self.rb.accomodateLabelsWidth(),
                      self.gpBottom.currentPosition().y());
            else:
               self.gpBottom.lineTo(
                      self.gpBottom.currentPosition().x() + BlockShape.BOTTOM_SOCKET_SIDE_SPACER,
                      self.gpBottom.currentPosition().y());

            socketCounter+=1;

      #curve right and up
      BlockShapeUtil.cornerTo(self.gpBottom, self.botRightCorner, self.topRightCorner, self.blockCornerRadius);

      #end bottom
      self.setEndPoint(self.gpBottom, self.botRightCorner, self.topRightCorner, False);

   def appendRightSidePath(self,painterPath, connectedBlock, connectedBlockShape):
      '''
        * Appends the right side path of the stack of blocks connected to the specified connectedBlock.  If there are
        * some empty sockets, this method will append empty placeholders.
        * @param painterPath the GeneralPath to append the new path to
        * @param connectedBlock the Block instance whose right side of its stack of connected blocks will be appened to the
        * specified painterPath
        * @param connectedBlockShape the BlockShape of the specified connectedBlock
       '''
      from blocks.RenderableBlock import RenderableBlock
      # int lastBottomPathWidth;


      # append top side of connected block
      BlockShapeUtil.appendPath(painterPath, connectedBlockShape.getTopSide(), False);

      startX = painterPath.currentPosition().x();
      for socket in connectedBlock.getSockets():
         # Sets the current x-coordinate to the start x-coordinate
         # Makes it so path movements created by previous blocks don't affect
         # the subsequent blocks.
         painterPath.lineTo(startX, painterPath.currentPosition().y());
         if(socket.blockID == Block.NULL):
            # just draw an empty socket placeholder
            # if its the first socket, draw a top side
            painterPath.lineTo(
                        painterPath.currentPosition().x() + BlockShape.BOTTOM_SOCKET_SIDE_SPACER,
                        painterPath.currentPosition().y());

            # now draw the empty right socket side
            # draw first socket - down right side
            BlockShape.BCS.addDataSocket(painterPath, socket.getKind(), False);
            # TODO:lastBottomPathWidth = (int)BOTTOM_SOCKET_SIDE_SPACER;
         else:
            # a block is connected to this socket, check if that block has sockets
            # OR if the block is an infix block - if it is infix, then just wrap around the infix block
            block = Block.getBlock(socket.blockID);
            shape = RenderableBlock.getRenderableBlock(socket.blockID).getBlockShape();
            if(block.getNumSockets() == 0 or block.isInfix()):
               # append this block's top and right side
               # TODO instead of just appending the right side...draw line to
               BlockShapeUtil.appendPath(painterPath, shape.getTopSide(), False);
               BlockShapeUtil.appendPath(painterPath, shape.getRightSide(), False);
            else:
               self.appendRightSidePath(painterPath, block, shape);


         # Updates the maximum X-coordinate and sets the current point to self.maxX
         if(self.maxX < painterPath.currentPosition().x()):
            self.maxX =  painterPath.currentPosition().x();

         painterPath.lineTo(self.maxX, painterPath.currentPosition().y());

   def determineBlockWidth(self):
      '''
        * Overrided from BlockShape.
        * Determines the width of the sum of the bottom sockets and uses it if it is
        * greater than the width determined by the determineBlockWidth in BlockShape.
        * Else, it returns the sum of these two values.
      '''
      # System.out.println("determining block width");

      width = BlockShape.determineBlockWidth(self);

      # if the sum of bottom sockets is greater than the calculated width, then use it
      bottomSocketWidth = 0;
      for socket in self.block.getSockets():
         if (socket.getPositionType() == BlockConnector.PositionType.BOTTOM):
            if(socket.blockID == Block.NULL):
               # 3 socket spacers = left of socket, between connectors, right of socket
               bottomSocketWidth += BlockShape.BOTTOM_SOCKET_SIDE_SPACER ;
            else: # a block is connected to socket
               # TODO get their assigned width from rb
               if (self.rb.getSocketSpaceDimension(socket) != None):
                  bottomSocketWidth += self.rb.getSocketSpaceDimension(socket).width();
                  bottomSocketWidth -= BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH;
                  # if it's a mirror plug, subtract for the other side, too.
                  if (Block.getBlock(socket.blockID).getPlug().getPositionType() == BlockConnector.PositionType.MIRROR):
                     bottomSocketWidth -= BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH;



      bottomSocketWidth += 2 * BlockShape.BOTTOM_SOCKET_MIDDLE_SPACER;  # TODO need to decide for a size of the middle spacer and how to place them
      bottomSocketWidth += 2 * BlockShape.BOTTOM_SOCKET_SIDE_SPACER;

      if(bottomSocketWidth > width): return (bottomSocketWidth + self.rb.accomodateLabelsWidth());

      width += bottomSocketWidth;

      # make sure its even
      if(width % 2 == 1): width+=1;

      return width;
