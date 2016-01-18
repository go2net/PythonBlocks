#-------------------------------------------------------------------------------
# Name:                module1
# Purpose:
#
# Author:            shijq
#
# Created:         08/03/2015
# Copyright:     (c) shijq 2015
# Licence:         <your licence>
#-------------------------------------------------------------------------------
import math

from blocks.BlockConnectorShape import BlockConnectorShape
from blocks.Block import Block
from PyQt4 import QtGui,QtCore
from blocks.BlockShapeUtil import BlockShapeUtil
from blocks.BlockConnector import BlockConnector

class BlockShape():

    # radius of rounded corners
    CORNER_RADIUS = 3.0;
    # variable declaration spacer
    VARIABLE_DECLARATION_SPACER = 10;
    # spacer for bottom sockets to block sides and other bottom sockets
    BOTTOM_SOCKET_SIDE_SPACER = 10;
    # spacer for in between bottom sockets
    BOTTOM_SOCKET_MIDDLE_SPACER = 16;
    # spacer on top of bottom sockets to give continuous top
    BOTTOM_SOCKET_UPPER_SPACER = 4;

    customBlockShapeSets= []
    BCS = BlockConnectorShape()

    def __init__(self,rb):

        if (rb != None):
             self.rb = rb
             self.blockID = rb.blockID
             self.block = Block.getBlock(self.blockID)
        else:
             print("Cannot create shape of null RenderableBlock.");

            #initialize gernal path segements around the block shape
        #self.painterPath = None

        self.setupProperties();


    def setupProperties(self):
        '''
        Determine charactoristics of the block shape depending on properties of the block
        '''
        # if isCommandBlock than it has curved corners, else sharp corners
        # note: it won't actually waste time drawing sharp corners,
        # but cornering method will know to draw a line instead

        self.hasCurvedCorners = self.block.hasBeforeConnector() or self.block.hasAfterConnector() or self.block.isCommandBlock()
        self.blockCornerRadius = BlockShape.CORNER_RADIUS if self.hasCurvedCorners else 0.0


    def setupDimensions(self):
        '''
        Determine the dimensions of the block shape so there is enough space to
        draw all of the shape's features.
        '''
            # if it has a plug, then offset the start of drawing the block
        initX = 0
        initY = 0;

        if self.block.hasPlug():
             initX = BlockConnectorShape.getConnectorDimensions(self.block.getPlug()).width()

            ###CHECK FOR CUSTOM SHAPES###
            # for every customBlockShapes
        cornerPoints =    [None,None,None,None];

        # System.out.println(block.getGenusName() + " custom size: " + customBlockShapeSets.size());
        for customBlockShapeSet    in self.customBlockShapeSets:
             # returns if custom shape is within this set, break for first one found
             if (customBlockShapeSet.checkCustomShapes(block, cornerPoints, rb.accomodateLabelsWidth(), getTotalHeightOfSockets())):
                    self.topLeftCorner = QPointF (cornerPoints[0].getX() + initX, cornerPoints[0].getY() + initY)
                    self.topRightCorner = QPointF (cornerPoints[1].getX() + initX, cornerPoints[1].getY() + initY)
                    self.botLeftCorner = QPointF (cornerPoints[2].getX() + initX, cornerPoints[2].getY() + initY)
                    self.botRightCorner = QPointF (cornerPoints[3].getX() + initX, cornerPoints[3].getY() + initY)
                    return


            # if custom shape not found, then continue to derive it
            # as determined by the renderable block
            # POSITIONING FACTORS:
            # initial x: plug on left side
            # initial y: should always be 0 so top is at highest point
            # SIZE FACTORS:
            # width: default size of block, size of text
            # height: how many sockets

        width = self.determineBlockWidth()
        height = self.determineBlockHeight()

        self.blockBody = QtCore.QRect( initX, initY, width, height)

            # derived fields
        self.topLeftCorner    = QtCore.QPoint(self.blockBody.x(),    self.blockBody.y());
        self.topRightCorner = QtCore.QPoint(self.blockBody.x() + self.blockBody.width(), self.blockBody.y());
        self.botLeftCorner    = QtCore.QPoint(self.blockBody.x(),    self.blockBody.y() +        self.blockBody.height());
        self.botRightCorner = QtCore.QPoint(self.blockBody.x() + self.blockBody.width(), self.blockBody.y() + self.blockBody.height());

        pass


    def determineBlockWidth(self):
        '''
        Determines the width of the block by checking for numerous block characteristics
        TODO: this contains a lot of starlogo specific checks - should be refactored into slcodeblocks?
        '''
        width = 0;

        # add width for labels
        width += self.rb.accomodateLabelsWidth();
        #print(self.rb.accomodateLabelsWidth())
        # add width for sockets
        width += self.rb.getMaxSocketShapeWidth();

        if (self.block.isCommandBlock()) :
             width +=    10;
        elif (self.block.isDataBlock() or self.block.isFunctionBlock()):
             width += 8;
        #elif (self.block.isDeclaration()):
        #     width += 20;
        else:
             #assert false : "Block type not found." + block;
             # treat like a command block
             width += 10;


        # add some width for the drop down triangle if it has siblings
        if(self.block.hasSiblings()):
             width +=5;


        # add image width if the width calculated so far is less than the image width
        if(width < self.rb.accomodateImagesWidth()):
             width += (self.rb.accomodateImagesWidth() - width) + 10 ;

        # This forces the block to be an even number of pixels wide
        # Doing so ensures that command ports don't occur at half-pixel locations
        if (width % 2 == 1): width+=1;

        width = max(width, self.rb.getBlockWidgetDimension().width());

        return width;

    def determineBlockHeight(self):
        heightSum = 0;

        # has cornered edges?
        heightSum += 2 * BlockShape.CORNER_RADIUS if self.hasCurvedCorners else 0

        # determine and add socket heights
        heightSum += self.getTotalHeightOfSockets();

        # System.out.println("height sum after getting total height of sockets: "+heightSum);

        # ensure at least height of one data plug
        if(heightSum < BlockConnectorShape.DATA_PLUG_HEIGHT):
             heightSum = BlockConnectorShape.DATA_PLUG_HEIGHT;


        # get any height of labels other than sockets
        # page label height
        heightSum += self.rb.accomodatePageLabelHeight();

        # total image height if height so far is less than the total height of images
        if(heightSum < self.rb.accomodateImagesHeight()):
             heightSum += (self.rb.accomodateImagesHeight() - heightSum) + 10;

        # System.out.println("returned heightSum: "+heightSum);

        if(self.block.isInfix()):
            heightSum += BlockShape.BOTTOM_SOCKET_UPPER_SPACER;

        heightSum = max(heightSum, self.rb.getBlockWidgetDimension().height());

        return heightSum;

    def getBottomSide(self):
        return self.gpBottomClockwise;

    def getLeftSide(self):
        return self.gpLeftClockwise;

    def getTopSide(self):
        return self.gpTop;

    def getRightSide(self):
        return self.gpRight;

    def reformArea(self):
        # hopefully reseting is less costly than creating new ones

        self.gpTop = QtGui.QPainterPath()
        self.gpRight = QtGui.QPainterPath()
        self.gpBottom = QtGui.QPainterPath()
        self.gpLeft = QtGui.QPainterPath()

        self.setupDimensions();

        # make all of the sides
        self.makeTopSide();
        self.makeRightSide();
        self.makeBottomSide();
        self.makeLeftSide();

        # corrected (clockwise) left and bottom
        self.gpBottomClockwise = QtGui.QPainterPath ()
        self.gpLeftClockwise = QtGui.QPainterPath ()
        #self.gpBottomClockwise.moveTo(self.gpBottom.currentPosition().x(),
        #                                                     self.gpBottom.currentPosition().y());
        #self.gpLeftClockwise.moveTo(self.gpLeft.currentPosition().x(),
        #                                                     self.gpLeft.currentPosition().y());.2
        BlockShapeUtil.appendPath(self.gpBottomClockwise, self.gpBottom, True);
        BlockShapeUtil.appendPath(self.gpLeftClockwise, self.gpLeft, True);


        # create direction specific paths
        gpClockwise = QtGui.QPainterPath()
        gpCounterClockwise = QtGui.QPainterPath()

        # add to the direction specific paths
        gpCounterClockwise.connectPath(self.gpLeft);
        gpCounterClockwise.connectPath(self.gpBottom);
        gpClockwise.connectPath(self.gpTop);
        gpClockwise.connectPath(self.gpRight);

        # connect so gpCounterClockwise is the full path
        # it must be counter-clockwise for the bevel to be able to use it
        BlockShapeUtil.appendPath(gpCounterClockwise, gpClockwise, True);

        # convert it to an area
        self.blockArea = gpCounterClockwise

        return self.blockArea;


    def setEndPoint(self, gp, currentCorner, otherCorner, firstPointOnSide):

        # save calculation time if cornerRadius is zero
        if(self.blockCornerRadius == 0):
             if(firstPointOnSide):
                    BlockShapeUtil.moveTo(gp,currentCorner.x(), currentCorner.y());
             else:
                    BlockShapeUtil.lineTo(gp,currentCorner.x(), currentCorner.y());

        else:
             # corner radius > 0

             # find theta from line from current corner to other corner
             theta = math.atan2(otherCorner.x() - currentCorner.x(),
                                                            #negate since (0,0) at upper left
                                                            -(otherCorner.y() - currentCorner.y()));

             dx = self.blockCornerRadius * math.cos(math.pi/2 - theta);
             dy = self.blockCornerRadius * math.sin(math.pi/2 - theta);

             # System.out.println("theta: " + theta + "    xdiff: " + Xdiff + "    Ydiff: " + Ydiff);

             if(firstPointOnSide):
                    BlockShapeUtil.moveTo(gp, (currentCorner.x() + dx), (currentCorner.y() - dy));
             else:
                    BlockShapeUtil.lineTo(gp, (currentCorner.x() + dx), (currentCorner.y() - dy));


    def makeTopSide(self):

        # starting point of the block
        # gpTop.moveTo((float) topLeftCorner.getX(), (float) topLeftCorner.getY() + blockCornerRadius);
        self.setEndPoint(self.gpTop, self.topLeftCorner, self.botLeftCorner, True);

        # curve up and right
        BlockShapeUtil.cornerTo(self.gpTop, self.topLeftCorner, self.topRightCorner, self.blockCornerRadius);

        # command socket if necessary
        if (self.block.isCommandBlock() and self.block.hasBeforeConnector()):
             # params: path, distance to center of block, going right
             # Old center-aligned ports
             # Point2D p = BCS.addControlConnectorShape(gpTop, (float) topLeftCorner.distance(topRightCorner) / 2 - blockCornerRadius, true);
             # Trying left-aligned ports for now
             p = BlockShape.BCS.addControlConnectorShape(self.gpTop, BlockConnectorShape.COMMAND_PORT_OFFSET + self.blockCornerRadius, True);

             self.rb.updateSocketPoint(self.block.getBeforeConnector(), p);

        # curve down
        BlockShapeUtil.cornerTo(self.gpTop, self.topRightCorner, self.botRightCorner, self.blockCornerRadius);
        #BlockShapeUtil.lineTo(self.gpTop, self.topRightCorner.x(),self.topRightCorner.y())
        # end topside
    # gpTop.lineTo(blockBody.x + blockBody.width, blockBody.y + blockCornerRadius);
    # gpTop.lineTo((float) topRightCorner.getX(), (float) topRightCorner.getY() + blockCornerRadius);
        self.setEndPoint(self.gpTop, self.topRightCorner, self.botRightCorner, False);

    def makeRightSide(self):

        # move to the end of the TopSide
        # gpRight.moveTo(blockBody.x + blockBody.width, blockBody.y + blockCornerRadius);
        # gpRight.moveTo((float) topRightCorner.getX(), (float) topRightCorner.getY() + blockCornerRadius);
        self.setEndPoint(self.gpRight, self.topRightCorner, self.botRightCorner, True);
        #BlockShapeUtil.moveTo(self.gpRight,self.topRightCorner.x(), self.topRightCorner.y());
        # if page label enabled, extra height
        if(self.block.hasPageLabel()):
             BlockShapeUtil.lineToRelative(self.gpRight, 0, self.rb.accomodatePageLabelHeight()/2);

        # ADD MIRRORED PLUG ////
        # if it has a mirrored plug, then add it
        if((self.block.getPlug() != None) and
            (self.block.getPlug().getPositionType() == (BlockConnector.PositionType.MIRROR))):
             # add the plug to the gpRight
             BlockShape.BCS.addDataPlug(self.gpRight, self.block.getPlug().type, True, True);


        # ADD SOCKETS ////
        # for each socket in the iterator
        for curSocket in self.block.getSockets() :

             # if it is a single socket (there are no mirrored sockets)
             if (curSocket.getPositionType() == (BlockConnector.PositionType.SINGLE)):
                    # add the socket shape to the gpRight

                    # if it's a command socket
                    if (BlockConnectorShape.isCommandConnector(curSocket)):
                         spacerHeight = self.getSocketSpacerHeight(curSocket, BlockConnectorShape.DEFAULT_COMMAND_INPUT_HEIGHT);
                         # draw the command socket bar and such
                         p = BlockShape.BCS.addCommandSocket(self.gpRight, spacerHeight);
                         self.rb.updateSocketPoint(curSocket, p);

                    else:
                         self.appendConnectorOffset(self.gpRight, self.topRightCorner, self.botRightCorner, curSocket, True);
                         # it's a data socket
                         p = BlockShape.BCS.addDataSocket(self.gpRight, curSocket.type, True);
                         self.rb.updateSocketPoint(curSocket, p);

                         spacerHeight = self.getSocketSpacerHeight(curSocket, BlockConnectorShape.DATA_PLUG_HEIGHT);
                         socketHeight = BlockConnectorShape.getConnectorDimensions(curSocket).height();
                         BlockShapeUtil.lineToRelative(self.gpRight, 0, spacerHeight - socketHeight);

                         self.appendConnectorOffset(self.gpRight, self.topRightCorner, self.botRightCorner, curSocket, False);


        # if (block.getPlug() != null) System.out.println(block.getPlug().getPositionType());

        # line to the bottom right
        # gpRight.lineTo(blockBody.x + blockBody.width, blockBody.y + blockBody.height - blockCornerRadius);
        # gpRight.lineTo((float) botRightCorner.getX(), (float) botRightCorner.getY() - blockCornerRadius);
        self.setEndPoint(self.gpRight, self.botRightCorner, self.topRightCorner, False);


    def makeBottomSide(self):

        # start bottom-right
        # gpBottom.moveTo(blockBody.x, blockBody.y + blockBody.height - blockCornerRadius);
        #gpBottom.moveTo((float) botLeftCorner.getX(), (float) botLeftCorner.getY() - blockCornerRadius);
        self.setEndPoint(self.gpBottom, self.botLeftCorner, self.topLeftCorner, True);

        # BlockShapeUtil.lineToRelative(gpLeft, 0, 10);

        # curve down and right
        BlockShapeUtil.cornerTo(self.gpBottom, self.botLeftCorner, self.botRightCorner, self.blockCornerRadius);

        # CONTROL CONNECTOR
        # Removing the isCommandBlock requirement for now because procedure block has an after connector
        # if (block.isCommandBlock() && block.hasAfterConnector()) {
        if (self.block.hasAfterConnector() and (not self.rb.isCollapsed())):

             # control connector if necessary
             # Old center-aligned port
             # Point2D p = BCS.addControlConnectorShape(gpBottom, (float) botLeftCorner.distance(botRightCorner) / 2 - blockCornerRadius, true);
             # Trying left-aligned ports
             p = BlockShape.BCS.addControlConnectorShape(self.gpBottom, BlockConnectorShape.COMMAND_PORT_OFFSET + self.blockCornerRadius, True);
             self.rb.updateSocketPoint(self.block.getAfterConnector(), p);

        # curve right and up
        BlockShapeUtil.cornerTo(self.gpBottom, self.botRightCorner, self.topRightCorner, self.blockCornerRadius);

        # end bottom
        # gpBottom.lineTo(blockBody.x + blockBody.width, blockBody.y + blockBody.height - blockCornerRadius);
        # gpBottom.lineTo((float) botRightCorner.getX(), (float) botRightCorner.getY() - blockCornerRadius);
        self.setEndPoint(self.gpBottom, self.botRightCorner, self.topRightCorner, False);

    def makeLeftSide(self):

        # starting point of the block
        # gpLeft.moveTo(blockBody.x, blockBody.y + blockCornerRadius);
        # gpLeft.moveTo((float) topLeftCorner.getX(), (float) topLeftCorner.getY() + blockCornerRadius);
        self.setEndPoint(self.gpLeft, self.topLeftCorner, self.botLeftCorner, True);

        #//// ADD PLUG ////
        if (self.block.getPlug() != None):

             self.appendConnectorOffset(self.gpLeft, self.botLeftCorner, self.topLeftCorner, self.block.getPlug(), False);

             # add the plug shape to the gpLeft
             p = BlockShape.BCS.addDataPlug(self.gpLeft, self.block.getPlug().type, True,False);
             self.rb.updateSocketPoint(self.block.getPlug(), p);

             self.appendConnectorOffset(self.gpLeft, self.botLeftCorner, self.topLeftCorner, self.block.getPlug(), True);

        # end left side
        # gpLeft.lineTo(blockBody.x, blockBody.y + blockBody.height - blockCornerRadius);

        self.setEndPoint(self.gpLeft, self.botLeftCorner, self.topLeftCorner, False);

    def getTotalHeightOfSockets(self):
        heightSum = 0;

        # note if we find a bottom socket
        hasBottomSocket = False;
        maxBottomSocketHeight = 0;

        for socket in self.block.getSockets():

             socketDimension = self.rb.getSocketSpaceDimension(socket);
             # bottom connector stuff
             if (socket.getPositionType() == BlockConnector.PositionType.BOTTOM ):
                    if(socketDimension != None and socketDimension.height() > maxBottomSocketHeight):
                         maxBottomSocketHeight = socketDimension.height();

                    hasBottomSocket = True;
                    continue;

             #if the socket has been assigned a dimension...
             if(socketDimension != None):

                    heightSum += socketDimension.height();
                    # if command, then add other command parts
                    if(BlockConnectorShape.isCommandConnector(socket)):
                        heightSum += BlockConnectorShape.COMMAND_INPUT_BAR_HEIGHT + 2 * BlockShape.CORNER_RADIUS;
                    continue;


             # else use default dimension
             if(BlockConnectorShape.isCommandConnector(socket)):
                    heightSum += BlockConnectorShape.DEFAULT_COMMAND_INPUT_HEIGHT + BlockConnectorShape.COMMAND_INPUT_BAR_HEIGHT + 2 * BlockShape.CORNER_RADIUS;
                    #print("3：  heightSum {0}", heightSum)
             #else normal data connector, so add height
             else:
                    heightSum += BlockConnectorShape.DATA_PLUG_HEIGHT;


        # if it has bottom sockets, add extra height
        if(hasBottomSocket):
            heightSum += maxBottomSocketHeight;
        return heightSum;


    def appendConnectorOffset(self,gp, topPoint, botPoint,
        blockConnector, aboveConnector):

        # if top and bottom are equal, then no offset necessary
        if(topPoint.x() == botPoint.x()): return;

        # if top further right than bottom, then Xdiff is positive
        Xdiff = topPoint.x() - botPoint.x();
        # absolute distance
        Ydiff = math.abs(topPoint.y() - botPoint.y());


        # check to only offset correctly above or below the connector:
        # offset only above connectors on right slanting sides
        if(Xdiff > 0 and not aboveConnector) : return;
        # offset only below connectors on left slanting sides
        if(Xdiff < 0 and    aboveConnector): return;

        # get fraction by dividing connector height by total height of the side
        fraction = BlockConnectorShape.getConnectorDimensions(blockConnector).getHeight()/Ydiff;
        insetDist = Xdiff * fraction;

        # if top further out, then inset left - else move right
        BlockShapeUtil.lineToRelative(gp, -insetDist, 0);

    def getSocketSpacerHeight(self,socket, defaultHeight):
        # spacer for block connected to socket
        # default spacer height if no block connected
        spacerHeight = defaultHeight;
        # check for socket space from a connected block
        socketSpaceDimension = self.rb.getSocketSpaceDimension(socket);
        # if the socket has been assigned a dimension
        if(socketSpaceDimension != None):
             spacerHeight = socketSpaceDimension.height();

        return spacerHeight;
