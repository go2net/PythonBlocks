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
        self._kind = kind
        self._type = type

        self.positionType = positionType
        self.label = label
        self.isLabelEditable = isLabelEditable
        self.connBlockID = connBlockID
        self.isExpandable = isExpandable

        self.initKind = kind
        self.initType = type

        self.expandGroup = "" if expandGroup == None else expandGroup
        self.hasDefArg = False
  
    
    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, value):
        self._kind = value

    @kind.deleter
    def kind(self):
        del self._kind 

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
      
    @type.deleter
    def type(self):
        del self._kind 

    @property
    def blockID(self):
        return self.connBlockID

    @blockID.setter
    def blockID(self, value):
        self.connBlockID = value

    def getConnectorInfo(self):
        ConnectorInfo = {}
        ConnectorInfo['position-type'] = self.positionType
        ConnectorInfo['connector-kind'] = self.kind
        ConnectorInfo['connector-type'] = self.type
        ConnectorInfo['is-expandable'] = self.isExpandable
        ConnectorInfo['label-editable'] = self.isLabelEditable
        ConnectorInfo['label'] = self.label
        ConnectorInfo['expand-group'] = self.expandGroup
        
        return ConnectorInfo

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

    def hasBlock(self):
        return self.connBlockID != -1

    def getLabel(self):
        return self.label;

    def linkDefArgument(self):
        from Block import Block
        # checks if connector has a def arg or if connector already has a block
        if(self.hasDefArg and self.connBlockID == -1):
            block = Block(self.arg.getGenusName(), self.arg.label);
            connBlockID = block.blockID;
            return connBlockID;

        return -1

    def setConnectorBlockID(self, id):
        self.connBlockID = id;

    def loadBlockConnector(node):
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
             initType = node.attrib["init-type"]
         
         if("init-kind" in node.attrib):
             initKind = node.attrib["init-kind"]
             
         if("connector-type" in node.attrib):
             kind = node.attrib["connector-type"]
             
         if("label" in node.attrib):
             label = node.attrib["label"]
             
         if("con-block-id" in node.attrib):
             idConnected = node.attrib["con-block-id"] # + Block.MAX_RESERVED_ID

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
            position = BlockConnector.PositionType.SINGLE
         elif (positionType == ("bottom")):
             position = BlockConnector.PositionType.BOTTOM
         elif (positionType == ("mirror")):
             position = BlockConnector.PositionType.MIRROR
         elif (positionType == ("top")):
             position = BlockConnector.PositionType.TOP

         con = BlockConnector(initKind, initType,position, label, isLabelEditable, isExpandable, idConnected);
         
         con.expandGroup = expandGroup;
         if (initKind != kind):
            con.kind = kind;

     #assert con != None : "BlockConnector was not loaded " + node;

     return con;


    def getSaveNode(self, document, conKind):
      connectorElement = document.createElement("BlockConnector");
      connectorElement.setAttribute("connector-kind", conKind);
      connectorElement.setAttribute("connector-type", self.type);
      
      #connectorElement.setAttribute("init-kind", self.initKind);
      connectorElement.setAttribute("init-type", self.initType);
      
      connectorElement.setAttribute("label", self.label);
      if (len(self.expandGroup) > 0) :
         connectorElement.setAttribute("expand-group", self.expandGroup);

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
