#-------------------------------------------------------------------------------
# Name:        BlockConnectorShape.py
# Purpose:
#
# Author:      Jack.Shi
#
# Created:     02/03/2015
# Copyright:   (c) 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re

from PyQt4 import QtCore,QtGui
from blocks.BlockConnector import BlockConnector
from blocks.BlockShapeUtil import BlockShapeUtil

class BlockConnectorShape():

   # left alignment buffer for command ports
   COMMAND_PORT_OFFSET = 15;

   # height of horizontal-plug/socket
   DATA_PLUG_HEIGHT = 24.0;

   # Width of most plug shapes
   NORMAL_DATA_PLUG_WIDTH = 8.0;

   # Width of polymorphic plug shape
   POLYMORPHIC_DATA_PLUG_WIDTH = 8.0;

   # width of vertical control connection
   CONTROL_PLUG_WIDTH = 14.0;

   # height of vertical control connection
   CONTROL_PLUG_HEIGHT = 4.0;

   # width of command input bar
   COMMAND_INPUT_BAR_WIDTH = COMMAND_PORT_OFFSET + 2.0;

   # height of command input bar
   COMMAND_INPUT_BAR_HEIGHT = 5.0;

   # default height of command input
   DEFAULT_COMMAND_INPUT_HEIGHT = DATA_PLUG_HEIGHT

   COMMAND_SHAPE_NAME="";

   '''
   Different styles of SocketShapes:
   1 is the normal shape
   2 is the double stacked shape
   3 is the double inversion
   '''

   TRIANGLE_1 = 1;
   TRIANGLE_2 = 2;
   TRIANGLE_3 = 3;

   CIRCLE_1 = 4;
   CIRCLE_2 = 5;
   CIRCLE_3 = 6;

   SQUARE_1 = 7;
   SQUARE_2 = 8;
   SQUARE_3 = 9;

   POLYMORPHIC_1 = 10;
   POLYMORPHIC_2 = 11;
   POLYMORPHIC_3 = 12;

   PROC_PARAM = 13;

   COMMAND = 14;
   DEBUG_MODE = False;

   SHAPE_MAPPINGS = {}

   def __init__(self):
      pass

   def getConnenctionShapeMapping(shapeName):

      if (shapeName not in BlockConnectorShape.SHAPE_MAPPINGS):
         assert False, ("Unknown Connection Type: " + shapeName)
         return -1;
      else:
         return BlockConnectorShape.SHAPE_MAPPINGS[shapeName]



   def getConnectorDimensions(blockConnector):
      '''
      Gets the dimension of a given BlockConnector.  Mapping for the connector to a shape must already exist.
      '''
      mappedValue = BlockConnectorShape.getConnenctionShapeMapping(blockConnector.getKind())

      # if shaped not yet mapped
      # assert (mappedValue != -1) : "Block Connector is not mapped: "+blockConnector;

      # TODO: add proc param dimensions
      if((mappedValue == BlockConnector.POLYMORPHIC_1) or
         (mappedValue == BlockConnector.POLYMORPHIC_2) or
         (mappedValue == BlockConnector.POLYMORPHIC_3)):
         return QtCore.QSizeF(BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT)
      else:
         return QtCore.QSizeF(BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT)

   def addConnenctionShapeMapping(shapeName,  integer):
      #print("adding con shape map: "+shapeName+", "+ str(integer));
      BlockConnectorShape.SHAPE_MAPPINGS[shapeName] = integer

      if(integer == BlockConnectorShape.COMMAND):
         BlockConnectorShape.COMMAND_SHAPE_NAME = shapeName;

   def getConnenctionShapeMapping(shapeName):
      if (BlockConnectorShape.SHAPE_MAPPINGS.get(shapeName) == None):
         #assert false : ("Unknown Connection Type: " + shapeName);
         return -1;
      else:
         return BlockConnectorShape.SHAPE_MAPPINGS.get(shapeName);


   def isCommandConnector(connector):
      return (BlockConnectorShape.getConnenctionShapeMapping(connector.getKind()) == BlockConnectorShape.COMMAND);


   def getCommandShapeName():
      return BlockConnectorShape.COMMAND_SHAPE_NAME;

   def addDataSocket(self,blockPath, connectionShape,  onRightSide):
      # if onRightSide, socket is convex-left
      return self.addDataConnection(blockPath, connectionShape, True, not onRightSide);


   # assosiated method to draw starting from the bottom of the socket
   def addDataSocketUp(self, blockPath, connectionShape,  onRightSide):
      # if onRightSide, socket is convex-left
      return self.addDataConnection(blockPath, connectionShape, False, not onRightSide);

   def addControlConnectorShape(self,blockPath, distanceToCenter, appendRight):

      # get the initial point info and set the currentConnectorPath to use the self._lineTo self._curveTo methods
      self.startPoint = blockPath.currentPosition();
      self.socketPoint = QtCore.QPointF(self.startPoint.x() + (distanceToCenter if appendRight else -distanceToCenter), self.startPoint.y());

      self.currentConnectorPath = blockPath;

      if (appendRight):
         #then the centerPoint is to the right of the current location on the generalPath
         self._lineTo(distanceToCenter - BlockConnectorShape.CONTROL_PLUG_WIDTH / 2, 0);
         # update starting point for self._curveTo
         self.startPoint = blockPath.currentPosition();

         self._curveTo( BlockConnectorShape.CONTROL_PLUG_WIDTH / 2, BlockConnectorShape.CONTROL_PLUG_HEIGHT * 4/3,
   			  BlockConnectorShape.CONTROL_PLUG_WIDTH / 2, BlockConnectorShape.CONTROL_PLUG_HEIGHT * 4/3,
   			  BlockConnectorShape.CONTROL_PLUG_WIDTH, 0);
      else:
         # then the centerPoint is to the left of the current location on the generalPath
         self._lineTo(- distanceToCenter + BlockConnectorShape.CONTROL_PLUG_WIDTH / 2, 0);
         #update starting point for self._curveTo
         self.startPoint = blockPath.currentPosition();

         self._curveTo( - BlockConnectorShape.CONTROL_PLUG_WIDTH / 2, BlockConnectorShape.CONTROL_PLUG_HEIGHT * 4/3,
   			 - BlockConnectorShape.CONTROL_PLUG_WIDTH / 2, BlockConnectorShape.CONTROL_PLUG_HEIGHT * 4/3,
   			 - BlockConnectorShape.CONTROL_PLUG_WIDTH, 0);

      # to catch bugs
      self.currentConnectorPath = None;

      return self.socketPoint;

   def _lineTo(self,x, y):
      BlockShapeUtil.lineTo(self.currentConnectorPath, x + self.startPoint.x(), y + self.startPoint.y());


   def _curveTo(self, x1, y1,  x2,  y2, x3,  y3):
      BlockShapeUtil.cubicTo (
         self.currentConnectorPath,
         x1 + self.startPoint.x(), y1 + self.startPoint.y(),
         x2 + self.startPoint.x(), y2 + self.startPoint.y(),
   	   x3 + self.startPoint.x(), y3 + self.startPoint.y());


   def addDataConnection(self,blockPath,  connectionShape,  startFromTop, convexRight):
      # get the associated connection shape value
      connectionShapeInt = BlockConnectorShape.getConnenctionShapeMapping(connectionShape);

      # get the initial point info and set the currentConnectorPath to use the self._lineTo self._curveTo methods
      self.startPoint = blockPath.currentPosition();
      xStart = self.startPoint.x();
      yStart = self.startPoint.y();
      self.currentConnectorPath = QtGui.QPainterPath();
      self.currentConnectorPath.moveTo(xStart, yStart);

      socketPoint = QtCore.QPoint(self.startPoint.x(), (self.startPoint.y() + ( BlockConnectorShape.DATA_PLUG_HEIGHT / 2)) if startFromTop else (self.startPoint.y() - ( BlockConnectorShape.DATA_PLUG_HEIGHT / 2)));

      if (connectionShapeInt == BlockConnectorShape.TRIANGLE_1):
         # Starlogo Number
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT / 2);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT);
      elif (connectionShapeInt == BlockConnectorShape.TRIANGLE_2):
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT / 4);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT / 2);
         # shifted duplicate
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 3.0/4);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT);
      elif (connectionShapeInt == BlockConnectorShape.TRIANGLE_3):
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT / 4);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT / 2);
         # inversion
         self._lineTo( -BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 3.0/4);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT);
         #Starlogo Boolean
      elif (connectionShapeInt == BlockConnectorShape.CIRCLE_1):
         self._curveTo(
         		(BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH) * 4.0 / 3, 0,
         		(BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH) * 4.0 / 3, BlockConnectorShape.DATA_PLUG_HEIGHT,
         		0, BlockConnectorShape.DATA_PLUG_HEIGHT);
      elif (connectionShapeInt == BlockConnectorShape.CIRCLE_2):
         self._curveTo(
         		BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, 0,
         		BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 1/4,
         		BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH * 1/2, BlockConnectorShape.DATA_PLUG_HEIGHT * 1.0/2);
         self._curveTo(BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 3.0/4,
         		BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT,
         		0, BlockConnectorShape.DATA_PLUG_HEIGHT);
      elif (connectionShapeInt == BlockConnectorShape.CIRCLE_3):
         self._curveTo(
         		BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, 0,
         		BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 1/4,
         		BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH * 1/2, BlockConnectorShape.DATA_PLUG_HEIGHT * 1.0/2);
         # inversion
         self._curveTo(-BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 3.0/4,
         		-BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT,
         		0, BlockConnectorShape.DATA_PLUG_HEIGHT);
   	     #Starlogo String
      elif (connectionShapeInt == BlockConnectorShape.SQUARE_1):
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.15);
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.15);
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.85);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.85);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT);
      elif (connectionShapeInt == BlockConnectorShape.SQUARE_2):
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.15);
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.15);
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.45);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.45);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.55);
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.55);
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.85);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.85);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT);
      elif (connectionShapeInt == BlockConnectorShape.SQUARE_3):
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.15);
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.15);
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.50);
         self._lineTo( -BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.50);
         self._lineTo( -BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.85);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.85);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT);
      elif (connectionShapeInt == BlockConnectorShape.POLYMORPHIC_1):
         self._curveTo(0, BlockConnectorShape.DATA_PLUG_HEIGHT/3,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/3, BlockConnectorShape.DATA_PLUG_HEIGHT*1.0/3,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/2, BlockConnectorShape.DATA_PLUG_HEIGHT*1.0/4);
         self._curveTo(BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH *2/3, BlockConnectorShape.DATA_PLUG_HEIGHT*1.0/6,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT*1.0/6,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT*1.0/2);
         self._curveTo(BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT *5.0/6,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH *2/3, BlockConnectorShape.DATA_PLUG_HEIGHT *5.0/6,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/2, BlockConnectorShape.DATA_PLUG_HEIGHT *3.0/4);
         self._curveTo(BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/3, BlockConnectorShape.DATA_PLUG_HEIGHT *2/3,
         		0, BlockConnectorShape.DATA_PLUG_HEIGHT *2/3,
         		0, BlockConnectorShape.DATA_PLUG_HEIGHT);
      elif (connectionShapeInt == BlockConnectorShape.POLYMORPHIC_2):
         self._curveTo(0, BlockConnectorShape.DATA_PLUG_HEIGHT/6,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/3, BlockConnectorShape.DATA_PLUG_HEIGHT/6,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/2, BlockConnectorShape.DATA_PLUG_HEIGHT/8);
         self._curveTo(BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH *2/3, BlockConnectorShape.DATA_PLUG_HEIGHT/12,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT/12,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT/4);
         self._curveTo(BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT *5/12,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH *2/3, BlockConnectorShape.DATA_PLUG_HEIGHT *5/12,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/2, BlockConnectorShape.DATA_PLUG_HEIGHT *3/8);
         self._curveTo(BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/3, BlockConnectorShape.DATA_PLUG_HEIGHT *2/6,
         		0, BlockConnectorShape.DATA_PLUG_HEIGHT *2/6,
         		0, BlockConnectorShape.DATA_PLUG_HEIGHT/2);
         # shifted duplicate
         self._curveTo(0, BlockConnectorShape.DATA_PLUG_HEIGHT *4/6,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/3, BlockConnectorShape.DATA_PLUG_HEIGHT *4/6,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/2, BlockConnectorShape.DATA_PLUG_HEIGHT *5/8);
         self._curveTo(BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH *2/3, BlockConnectorShape.DATA_PLUG_HEIGHT *7/12,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT *7/12,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT *3/4);
         self._curveTo(BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT *11/12,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH *2/3, BlockConnectorShape.DATA_PLUG_HEIGHT *11/12,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/2, BlockConnectorShape.DATA_PLUG_HEIGHT *7/8);
         self._curveTo(BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/3, BlockConnectorShape.DATA_PLUG_HEIGHT *5/6,
         		0, BlockConnectorShape.DATA_PLUG_HEIGHT *5/6,
         		0, BlockConnectorShape.DATA_PLUG_HEIGHT);

      elif (connectionShapeInt == BlockConnectorShape.POLYMORPHIC_3):
         self._lineTo( BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/3, BlockConnectorShape.DATA_PLUG_HEIGHT / 8);
         self._lineTo( BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/2, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.025);
         self._lineTo( BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH * 3/4, BlockConnectorShape.DATA_PLUG_HEIGHT/8);
         self._curveTo(BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH * 10 / 9, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.15,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH * 10 / 9, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.35,
         		BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH * 3 / 4, BlockConnectorShape.DATA_PLUG_HEIGHT * 3 / 8);
         self._lineTo( BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH / 2, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.475);
         self._lineTo( BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH / 3, BlockConnectorShape.DATA_PLUG_HEIGHT * 3 / 8);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT / 2);
         # inversion
         self._lineTo( -BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/3, BlockConnectorShape.DATA_PLUG_HEIGHT / 8 + BlockConnectorShape.DATA_PLUG_HEIGHT / 2);
         self._lineTo( -BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH/2, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.025 + BlockConnectorShape.DATA_PLUG_HEIGHT / 2);
         self._lineTo( -BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH * 3/4, BlockConnectorShape.DATA_PLUG_HEIGHT/8 + BlockConnectorShape.DATA_PLUG_HEIGHT / 2);
         self._curveTo(-BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH * 10 / 9, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.15 + BlockConnectorShape.DATA_PLUG_HEIGHT / 2,
         		-BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH * 10 / 9, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.35 + BlockConnectorShape.DATA_PLUG_HEIGHT / 2,
         		-BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH * 3 / 4, BlockConnectorShape.DATA_PLUG_HEIGHT * 3 / 8 + BlockConnectorShape.DATA_PLUG_HEIGHT / 2);
         self._lineTo( -BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH / 2, BlockConnectorShape.DATA_PLUG_HEIGHT * 0.475 + BlockConnectorShape.DATA_PLUG_HEIGHT / 2);
         self._lineTo( -BlockConnectorShape.POLYMORPHIC_DATA_PLUG_WIDTH / 3, BlockConnectorShape.DATA_PLUG_HEIGHT * 3 / 8 + BlockConnectorShape.DATA_PLUG_HEIGHT / 2);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT);


      # formally BlockGenus.PROC_PARAM
      elif (connectionShapeInt == BlockConnectorShape.PROC_PARAM):
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT * 1 / 4);
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 1 / 4);
         self._lineTo( BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH, BlockConnectorShape.DATA_PLUG_HEIGHT * 3 / 4);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT * 3 / 4);
         self._lineTo( 0, BlockConnectorShape.DATA_PLUG_HEIGHT);

      # look for additional 3rd party shapes here...

      else:
         # System.out.println("Connection Type Not Identified: " + connectionShape);
         pass



      # flip the path if starting from the bottom or changing convex direction
      if (not startFromTop or not convexRight):
         self.currentConnectorPath = self.transformGeneralPath(self.currentConnectorPath, not convexRight, not startFromTop);

      #pos1 = blockPath.currentPosition()
      # finally append the correctly oriented currentConnectorPath to the blockPath
      blockPath.connectPath(self.currentConnectorPath);
      #pos2 = blockPath.currentPosition()
      # to catch bugs
      self.currentConnectorPath = None;

      return socketPoint;

   def addCommandSocket(self, blockPath, commandSocketHeight):
      from blocks.BlockShape import BlockShape

      # draw bar
      BlockShapeUtil.lineToRelative(blockPath, BlockConnectorShape.COMMAND_INPUT_BAR_WIDTH, 0);
      BlockShapeUtil.lineToRelative(blockPath, 0, BlockConnectorShape.COMMAND_INPUT_BAR_HEIGHT);
      socketPoint = self.addControlConnectorShape(blockPath, BlockConnectorShape.CONTROL_PLUG_WIDTH / 2,False);

      # first corner inside command input
      BlockShapeUtil.cornerTo(blockPath,
      QtCore.QPointF(
          blockPath.currentPosition().x() - BlockConnectorShape.COMMAND_INPUT_BAR_WIDTH +  BlockShape.CORNER_RADIUS,
          blockPath.currentPosition().y()),
      QtCore.QPointF(
          blockPath.currentPosition().x() - BlockConnectorShape.COMMAND_INPUT_BAR_WIDTH +  BlockShape.CORNER_RADIUS,
          blockPath.currentPosition().y() + BlockShape.CORNER_RADIUS),
      BlockShape.CORNER_RADIUS);



      # insert dynamic command input height between these two methods
      BlockShapeUtil.lineToRelative(blockPath, 0, commandSocketHeight);

      # second corner at bottom of command input
      BlockShapeUtil.cornerTo(blockPath,
      QtCore.QPointF(
          blockPath.currentPosition().x(),
          blockPath.currentPosition().y() + BlockShape.CORNER_RADIUS),
      QtCore.QPointF(
          blockPath.currentPosition().x() + BlockShape.CORNER_RADIUS,
          blockPath.currentPosition().y() + BlockShape.CORNER_RADIUS),
      BlockShape.CORNER_RADIUS);


      # extend left to match y coordinate of initial point
      BlockShapeUtil.lineToRelative(blockPath, BlockConnectorShape.CONTROL_PLUG_WIDTH/2, 0);

      return socketPoint;

   '''
   * Flips a GeneralPath and translates it so the starting point is in the correct place.
   *
   * @param gp the GeneralPath to be transformed
   * @param horzFlip true if flipped horizontally
   * @param vertFlip true if flipped vertically
   '''
   def transformGeneralPath(self,gp, horzFlip, vertFlip):
      xScale = 0
      yScale = 0
      xTranslate = 0
      yTranslate = 0

      if (horzFlip):
         xScale = -1;
         xTranslate = 2*self.startPoint.x();
      else:
         xScale = 1;
         xTranslate = 0;

      if (vertFlip):
         yScale = -1;
         yTranslate = 2*self.startPoint.y();
      else:
         yScale = 1;
         yTranslate = 0;


      # scale (flip)
      scale_transform = QtGui.QTransform()
      scale_transform.scale(xScale, yScale);
      # translate across the origin
      translate_transform = QtGui.QTransform()
      translate_transform.translate (xTranslate, yTranslate);
      # apply the transforms
      gp = scale_transform.map(gp)
      gp = translate_transform.map(gp)

      return gp



   def addDataPlug(self,blockPath, connectionShape, startFromTop, onRightSide):
      # if onRightSide, plug is convex-right
      return self.addDataConnection(blockPath, connectionShape, startFromTop, onRightSide);

   def loadBlockConnectorShapes(root):

      attrExtractor="(.*)"
      drawerNodes=root.findall("BlockConnectorShapes/BlockConnectorShape");
      for drawerNode in drawerNodes:
         shapeType = None;
         shapeNumber = None;
         if 'shape-type' in drawerNode.attrib:
            shapeType = drawerNode.attrib['shape-type']

         if 'shape-number' in drawerNode.attrib:
            shapeNumber = drawerNode.attrib['shape-number']

         if(shapeType != None and shapeNumber != None):
            # create shape to number mapping here
            BlockConnectorShape.addConnenctionShapeMapping(shapeType, int(shapeNumber));
