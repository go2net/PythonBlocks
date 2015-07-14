#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      A21059
#
# Created:     04/03/2015
# Copyright:   (c) A21059 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

class BlockConnector():
   TRIANGLE_1 = 1
   TRIANGLE_2 = 2
   TRIANGLE_3 = 3

   CIRCLE_1 = 4
   CIRCLE_2 = 5
   CIRCLE_3 = 6

   SQUARE_1 = 7
   SQUARE_2 = 8
   SQUARE_3 = 9

   POLYMORPHIC_1 = 10
   POLYMORPHIC_2 = 11
   POLYMORPHIC_3 = 12

   PROC_PARAM = 13

   COMMAND = 14

   PositionType = enum("SINGLE", "MIRROR", "BOTTOM", "TOP")

   def __init__(self, kind, type, positionType, label, isLabelEditable, isExpandable, connBlockID, expandGroup = None):
      if(positionType == ""):
         yieldy = 0
      self.kind = kind
      self.type = type
      self.positionType = positionType
      self.label = label
      self.isLabelEditable = isLabelEditable
      self.connBlockID = connBlockID
      self.isExpandable = isExpandable
      self.initKind = kind
      self.expandGroup = "" if expandGroup == None else expandGroup
      self.hasDefArg = False
   '''
   * Sets this connector's default argument to the specified genus and initial label.
   * @param genusName the desired BLockGenus name of the default agrument
   * @param label the initial label of the default argument
   '''
   def setDefaultArgument(self,genusName, label):
      self.hasDefArg = True
      #elf.arg = DefArgument(genusName, label)

   '''
   * Returns the PositionType of this
   * @return the PositionType of this
   '''
   def getPositionType(self):
     return self.positionType

   def getKind_(self):
     return self._kind;
     
   def getType(self):
     return self.type;     

   def hasBlock(self):
      return self.connBlockID != -1

   def getBlockID(self):
      return self.connBlockID;

   def getLabel(self):
      return self.label;

   def linkDefArgument(self):
      from Block import Block
      # checks if connector has a def arg or if connector already has a block
      if(self.hasDefArg and self.connBlockID == -1):
         block = Block(arg.getGenusName(), arg.label);
         connBlockID = block.getBlockID();
         return connBlockID;

      return -1

   def setConnectorBlockID(self, id):
      self.connBlockID = id;

   def loadBlockConnector(node):
     pattern = "(.*)"

     con = None;

     initKind = None;
     kind = None;
     idConnected = -1
     label = "";
     isExpandable = False;
     isLabelEditable = False;
     expandGroup = "";
     positionType = "single";

     if (node.tag == ("BlockConnector")):
         # load attributes
         if("init-type" in node.attrib):
             initKind = node.attrib["init-type"]
         if("connector-type" in node.attrib):
             kind = node.attrib["connector-type"]
         if("label" in node.attrib):
             label = node.attrib["label"]
         if("con-block-id" in node.attrib):
             idConnected = int(node.attrib["con-block-id"])

         if("label-editable" in node.attrib):
             isLabelEditable = node.attrib["label-editable"] == ("true");
         if("is-expandable" in node.attrib):
             isExpandable = node.attrib["is-expandable"] == ("true");

         if("expand-group" in node.attrib):
             expandGroup = node.attrib["expand-group"]
         if("position-type" in node.attrib):
             positionType = node.attrib["position-type"]


         #assert initKind != None : "BlockConnector was not specified a initial connection kind";

         if (positionType == ("single")):
            con = BlockConnector('', initKind, BlockConnector.PositionType.SINGLE, label, isLabelEditable, isExpandable, idConnected);
         elif (positionType == ("bottom")):
             con = BlockConnector('',initKind, BlockConnector.PositionType.BOTTOM, label, isLabelEditable, isExpandable, idConnected);
         elif (positionType == ("mirror")):
             con = BlockConnector('',initKind, BlockConnector.PositionType.MIRROR, label, isLabelEditable, isExpandable, idConnected);
         elif (positionType == ("top")):
             con = BlockConnector('',initKind, BlockConnector.PositionType.TOP, label, isLabelEditable, isExpandable, idConnected);

         con.expandGroup = expandGroup;
         if (initKind != kind):
            con.setKind(kind);

     #assert con != None : "BlockConnector was not loaded " + node;

     return con;


   def getSaveNode(self, document, conKind):
      from blocks.Block import Block
      connectorElement = document.createElement("BlockConnector");
      connectorElement.setAttribute("connector-kind", conKind);
      connectorElement.setAttribute("connector-type", self.kind);
      connectorElement.setAttribute("init-type", self.initKind);
      connectorElement.setAttribute("label", self.label);
      if (len(self.expandGroup) > 0) :
         connectorElement.setAttribute("expand-group", expandGroup);

      if (self.isExpandable):
         connectorElement.setAttribute("is-expandable", "yes");
      if (self.positionType == BlockConnector.PositionType.SINGLE):
         connectorElement.setAttribute("position-type", "single");
      elif (self.positionType == BlockConnector.PositionType.MIRROR):
         connectorElement.setAttribute("position-type", "mirror");
      elif (self.positionType == (BlockConnector.PositionType.BOTTOM)):
         connectorElement.setAttribute("position-type", "bottom");
      elif (self.positionType == (BlockConnector.PositionType.TOP)):
         connectorElement.setAttribute("position-type", "top");


      if (self.isLabelEditable):
         connectorElement.setAttribute("label-editable", "true");


      if (self.connBlockID != -1):
         connectorElement.setAttribute("con-block-id", str(self.connBlockID));


      return connectorElement;
