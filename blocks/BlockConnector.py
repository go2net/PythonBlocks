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
        if(connBlockID == -1):
            raise Exception("connBlockID == -1")
            connBlockID = ""
        self.connBlockID = connBlockID
        self.isExpandable = isExpandable

        self.initKind = kind
        self.initType = type

        self.expandGroup = "" if expandGroup == None else expandGroup
        self.hasDefArg = False
  
        #print(connBlockID)
        
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

    '''
    def __ne__(self, other):
        return not self .__eq__(other)
  
    def __eq__(self, other):
        if(other == None): return False
        if self.type != other.type: return False
        if self.label != other.label: return False
        return True
    '''
    
    def sameAs(self,  other):
        if(other == None): return False
        if self.type != other.type: return False
        if self.label != other.label: return False
        return True        

    def getConnectorInfo(self):
        conn_info = {}
        conn_info['position'] = self.positionType
        conn_info['kind'] = self.kind
        conn_info['type'] = self.type
        conn_info['expandable'] = self.isExpandable
        conn_info['editable'] = self.isLabelEditable
        conn_info['label'] = self.label
        conn_info['expand-group'] = self.expandGroup
        conn_info["con-block-id"] = self.blockID
        return conn_info

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
        return self.connBlockID != "" and self.connBlockID != -1

    def getLabel(self):
        return self.label;

    def linkDefArgument(self):
        from Block import Block
        # checks if connector has a def arg or if connector already has a block
        if(self.hasDefArg and self.connBlockID == ""):
            block = Block(self.arg.getGenusName(), self.arg.label);
            connBlockID = block.blockID;
            return connBlockID;

        return -1

    def setConnectorBlockID(self, id):
        self.connBlockID = id;

    def loadBlockConnector(conn_info):
        con = None;
        initKind = None;
        kind = None;
        idConnected = ""
        label = "";
        isExpandable = False;
        isLabelEditable = False;
        expandGroup = "";
        position = 0
        # load attributes
        if("type" in conn_info):
            initType = conn_info["type"]

        if("kind"  in conn_info):
            kind = conn_info["kind"]
         
        if("connector-type" in conn_info):
            kind = conn_info["connector-type"]
         
        if("label" in conn_info):
            label = conn_info["label"]
         
        if("con-block-id" in conn_info):
            idConnected = conn_info["con-block-id"] # + Block.MAX_RESERVED_ID

        if("editable" in conn_info):
            isLabelEditable = conn_info["editable"] 
         
        if("expandable" in conn_info):
            isExpandable = conn_info["expandable"] 

        if("expand-group" in conn_info):         
            expandGroup = conn_info["expand-group"]
        if("position" in conn_info):
            position = conn_info["position"]

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
