
import re
from blocks.BlockGenus import BlockGenus
from blocks.BlockConnector import BlockConnector
import uuid
       
class Block():

   # The ID that is to be assigned to the next new block
   NEXT_ID = 1
   MAX_RESERVED_ID = -1
   
   # Defines a NULL id for a Block
   NULL = -1

   # A universal hashmap of all the Block instances
   ALL_BLOCKS= {}
   tmpObj = None
   
   def __init__(self, canvas):
      self.canvas = canvas
      self.pageLabel = ""
      self.hasFocus = False;
      self.isBad = False;
      self.disabled = False
      self.sockets = []
      self.argumentDescriptions = []
      self.outputConnection = None
  
   def __del__(self):
      pass

   @classmethod
   def createBlockFromID(cls, canvas, genusName, linkToStubs=True, id=-1,label=None):
      obj = cls(canvas)
      obj.linkToStubs = linkToStubs
      obj._blockID = id

      if (label == None):
         label = BlockGenus.getGenusWithName(genusName).getInitialLabel()

      #if (id in Block.ALL_BLOCKS):
      #  dup = Block.ALL_BLOCKS.get(id);
      #  print("pre-existing block is: {0} with genus {1} and label {2}".format(id,dup.getGenusName(),dup.getBlockLabel()));
      #  raise Exception("Block id: {0} already exists!  BlockGenus {1}, label: {2}".format(id,genusName,label))
      
      # copy connectors from BlockGenus
      genus = BlockGenus.getGenusWithName(genusName)
      if(genus == None):
          raise Exception("genusName: "+genusName+" does not exist.")

      # copy the block connectors from block genus
      iter = genus.getInitSockets();
      for con in iter:
         obj.sockets.append(BlockConnector(         
            con.kind,
            con.type,
            con.positionType,
            con.label,
            con.isLabelEditable,
            con.isExpandable,
            con.connBlockID,
            con.expandGroup))


      if(genus.getInitPlug() != None):
         obj.plug = BlockConnector(
            genus.getInitPlug().kind,
            genus.getInitPlug().type,
            genus.getInitPlug().positionType,
            genus.getInitPlug().label,
            genus.getInitPlug().isLabelEditable,
            genus.getInitPlug().isExpandable,
            genus.getInitPlug().connBlockID,
            genus.getInitPlug().expandGroup);
      else:
         obj.plug = None

      if(genus.getInitBefore() != None):
         obj.before = BlockConnector(
            genus.getInitBefore().kind,
            genus.getInitBefore().type,
            genus.getInitBefore().positionType,
            genus.getInitBefore().label,
            genus.getInitBefore().isLabelEditable,
            genus.getInitBefore().isExpandable,
            genus.getInitBefore().connBlockID,
            genus.getInitBefore().expandGroup);
      else:
         obj.before = None

      if(genus.getInitAfter() != None):
         obj.after = BlockConnector(
            genus.getInitAfter().kind,
            genus.getInitAfter().type,
            genus.getInitAfter().positionType,
            genus.getInitAfter().label,
            genus.getInitAfter().isLabelEditable,
            genus.getInitAfter().isExpandable,
            genus.getInitAfter().connBlockID,
            genus.getInitAfter().expandGroup);
      else:
         obj.after = None

      obj.genusName = genusName;

      obj.label = label;

      obj.expandGroups = []
     
      if(obj.blockID != None and obj.blockID != -1):
        Block.ALL_BLOCKS[obj.blockID] = obj

      Block.tmpObj = obj
      
      return obj
      
   
   @classmethod
   def createBlock(cls, canvas,  genusName, linkToStubs, label=None):
     id = Block.generateId()
     return Block.createBlockFromID(canvas, genusName, linkToStubs, id,label)

   @property
   def blockID(self):
      """I'm the 'x' property."""
      return self._blockID

   @blockID.setter
   def blockID(self, value):
      self._blockID = value

   @blockID.deleter
   def blockID(self):
      del self._blockID       
      
   def generateId():
       return str(uuid.uuid1())
       
   def getInputTargetBlock(self, name):
    socket = self.getSocketByName(name.lower())
    if(socket == None):
      return None
      
    blockID = socket.blockID
    if(blockID == -1):
      return None
    else:
      return Block.getBlock(blockID)
      
   def getBlock(blockID):
     
      if(blockID == -1): return Block.tmpObj 

      if(blockID in Block.ALL_BLOCKS):
         return Block.ALL_BLOCKS[blockID]
      else:
         #print("Not found")
         return None

   def isInfix(self):
      genus = self.getGenus()
      return genus.isInfix()

   def getGenus(self):
     return BlockGenus.getGenusWithName(self.genusName)

   def changeLabelTo(self,  label):
      self.label = label 

   def hasPlug(self):
     return not (self.plug == None);

   def getPlug(self):
     return self.plug;


   def hasPageLabel(self):
      return self.pageLabel != None and self.pageLabel != ""

   def isCommandBlock(self):
      return self.getGenus().isCommandBlock()

   def hasSiblings(self):
     return self.getGenus().hasSiblings();

   def getSiblingsList(self):
      return self.getGenus().getSiblingsList()


   def hasBeforeConnector(self):
      return self.before != None;

   def hasAfterConnector(self):
      return self.after != None;

   def getSockets(self):
      return self.sockets
      
   def getSocketByName(self, name):
      for socket in self.getSockets():
        if(socket.getLabel() == name):
          return socket
      return None

   def isProcedureDeclBlock(self):
      return self.getGenus().isProcedureDeclBlock();

   def getAfterConnector(self):
      return self.after;

   def getBeforeConnector(self):
      return self.before;

   def getBlockFullLabel(self):
      return self.getGenus().getLabelPrefix()+self.label+self.getGenus().getLabelSuffix();
      
   def getBlockLabel(self):
      return self.label

   def getLabelPrefix(self):
      return self.getGenus().getLabelPrefix()
      
   def getLabelSuffix(self):
      return self.getGenus().getLabelSuffix()
      
   def setBlockLabel(self, newLabel):
      from blocks.BlockStub import BlockStub
      if (self.linkToStubs and self.hasStubs()):
          BlockStub.parentNameChanged(self.label, newLabel, self.blockID);

      self.label = newLabel;

   def isLabelEditable(self):
      return self.getGenus()._isLabelEditable;

   def getPageLabel(self):
      return self.pageLabel;

   def getNumSockets(self):
      return len(self.sockets);

   def getSocketAt(self, index):
        if(index<len(self.sockets)):
           return self.sockets[index];
        else:
          return None
        #assert index < sockets.size() : "Index "+index+" is greater than the num of sockets: "+sockets.size()+" of "+this;
      

   def getInitBlockImageMap(self):
      return self.getGenus().getInitBlockImageMap();

   def isDeclaration(self):
      return self.getGenus().isDeclaration();

   def getColor(self):
      return self.getGenus().getColor();

   def isDataBlock(self):
      return self.getGenus().isDataBlock();

   def isFunctionBlock(self):
      return self.getGenus().isFunctionBlock();
      
   def isVariable(self):
      return self.getGenus().isVariableDeclBlock();      

   def getArgumentDescription(self, index):
      if (index < len(self.argumentDescriptions) and index >= 0):
         return self.argumentDescriptions[index];

      return None;

   def getInitialLabel(self):
     return self.getGenus().getInitialLabel();

   def labelMustBeUnique(self):
      return self.getGenus().labelMustBeUnique;

   def hasDefaultArgs(self):
      return self.getGenus().hasDefaultArgs();

   def linkAllDefaultArgs(self):
      if(self.getGenus().hasDefaultArgs()):
         defargIDs = []
         for con in self.sockets:
            id = con.linkDefArgument();
            defargIDs.append(id);
            # if id not null, then connect def arg's plug to this block
            if(id != Block.NULL):
               Block.getBlock(id).getPlug().setConnectorBlockID(self.blockID);

         return defargIDs;

      return None;

   def blockConnected(self,connectedSocket, connectedBlockID):
      from blocks.BlockStub import BlockStub
      if (connectedSocket.isExpandable):
         if (connectedSocket.getExpandGroup().length() > 0):
             # Part of an expand group
            self.expandSocketGroup(connectedSocket.getExpandGroup());

         else:
            #expand into another one
            index = self.getSocketIndex(connectedSocket);
            if(self.isProcedureDeclBlock()):
               self.addSocket(index+1, connectedSocket.initKind(), connectedSocket.getPositionType(), "", connectedSocket.isLabelEditable(), connectedSocket.isExpandable(), Block.NULL);
            else:
               self.addSocket(index+1, connectedSocket.initKind(), connectedSocket.getPositionType(), connectedSocket.getLabel(), connectedSocket.isLabelEditable(), connectedSocket.isExpandable(), Block.NULL);


      # NOTE: must update the sockets of this before updating its stubs as stubs use this as a reference to update its own sockets
      # if block has stubs, update its stubs as well
      if(self.hasStubs()):
         BlockStub.parentConnectorsChanged(self.blockID);

   def hasStubs(self):
      return self.linkToStubs and  self.getGenus().hasStubs();

   def getBeforeBlockID(self):
      if (self.before == None):
         return Block.NULL;
      return self.before.blockID;

   def getAfterBlockID(self):
      if (self.after == None):
         return Block.NULL;
      return self.after.blockID;

   def getPlugBlockID(self):
      if(self.plug == None):
         return Block.NULL;
      return self.plug.blockID;


   def getExpandGroup(groups, group):
      for list in groups:
         # Always at least one element in the group.
         if (list[0].getExpandGroup() == group):
            return list;

      return None;

   def expandSocketGroup(self,group):
      '''
      * Expand a socket group in this block. For now, all new sockets will
      * be added after the last socket in the group.
      '''
      expandSockets = self.getExpandGroup(self.expandGroups, group);
      #assert expandSockets != null;

      # Search for the socket to insert after.
      index = len(self.sockets) - 1;
      label = expandSockets[len(expandSockets) - 1].getLabel();
      while(index  >= 0):
         conn = self.sockets[index]
         if (conn.getLabel()==label and conn.getExpandGroup() ==(group)):
             break;
         index -= 1

     #assert index >= 0;

      # Insert all the new sockets
      for conn in  expandSockets:
         index+=1;
         newConn = BlockConnector(conn);
         self.sockets.add(index, newConn);

   def shrinkSocketGroup(self, socket):
      '''
      * Shrink a socket group (un-expand it).
      '''
      group = socket.getExpandGroup();
      expandSockets = self.getExpandGroup(self.expandGroups, group);
      #assert expandSockets != null;

      # Search for the first socket in the group, if not the expandable
      # one.
      label = expandSockets.get(0).getLabel();
      index = self.getSocketIndex(self.socket);
      while(index  >= 0):
         con = self.sockets[index];
         if (con.getLabel() == label and con.getExpandGroup() == group):
             break;
         index -= 1

      #assert index >= 0;

      # Remove all the sockets.
      self.removeSocket(index);
      total = len(expandSockets);
      for i in range(1,total):
         con = self.sockets[index];
         if (con.getLabel() == expandSockets[i].getLabel() and con.getExpandGroup() == group):
            self.removeSocket(index);
            i+=1;
         else:
             index+=1;

   def canRemoveSocket(self, socket):
      '''
      * Returns true if the given expandable socket can be removed.
      '''
      total = len(self.sockets);
      first = -1;
      for i in range(0,total):
         conn = self.sockets.get(i);
         if (conn == self.socket):
             if (first == -1):first = i;
             else: return True;
         elif (conn.getPositionType().equals(socket.getPositionType()) and
                  conn.isExpandable() == socket.isExpandable() and
                  conn.initKind().equals(socket.initKind()) and
                  conn.getExpandGroup().equals(socket.getExpandGroup())):
             if (first == -1): first = i;
             else: return True;


      # If the socket is the first and last of its kind, then we can NOT
      # remove it. (We also can't remove it if they're both -1, obviously.)
      return False;

   def blockDisconnected(self,disconnectedSocket):
      '''
      * Informs this Block that a block has disconnected from the specified disconnectedSocket
      * @param disconnectedSocket
      '''
      from blocks.BlockStub import BlockStub
      
      if (disconnectedSocket.isExpandable and self.canRemoveSocket(disconnectedSocket)):
         if (disconnectedSocket.getExpandGroup().length() > 0):
            self.shrinkSocketGroup(disconnectedSocket);
         else:
            self.removeSocket(disconnectedSocket);


      # NOTE: must update the sockets of this before updating its stubs as stubs use this as a reference to update its own sockets
      # if block has stubs, update its stubs as well
      if(self.hasStubs()):
         BlockStub.parentConnectorsChanged(self.blockID);

   def getConnectorTo(self,otherBlockID):
      '''
      * Searches for the BlockConnector linking this block to another block
      * @param otherBlockID the Block ID if the other block
      * @return the BlockConnector linking this block to the other block
      '''
      if (otherBlockID == None or otherBlockID == Block.NULL):
         return None;
      if (self.getPlugBlockID() == otherBlockID):
         return self.plug;
      if (self.getBeforeBlockID() == otherBlockID):
         return self.before;
      if (self.getAfterBlockID() == otherBlockID):
         return self.after;
      for socket in self.getSockets():
         if (socket.blockID == otherBlockID):
            return socket;
      return None;

   def getGenusName(self):
      '''
      * Returns the name of this genus
      * FORWARDED FROM BLOCK GENUS
      * @return the name of this genus
      '''
      return self.genusName


   def getSaveNode(self, document, x, y, commentNode, isCollapsed):
      blockElement = document.createElement("Block");

      blockElement.setAttribute("id", str(self.blockID));

      blockElement.setAttribute("genus-name", self.getGenusName());
      if (self.hasFocus):
         blockElement.setAttribute("has-focus", "yes");


      if (not self.label == (self.getInitialLabel())):
         labelElement = document.createElement("Label");
         labelElement.appendChild(document.createTextNode(self.label ));
         blockElement.appendChild(labelElement);


      if (self.pageLabel != None and self.pageLabel != ""):
         pageLabelElement = document.createElement("PageLabel");
         pageLabelElement.appendChild(document.createTextNode(self.pageLabel));
         blockElement.appendChild(pageLabelElement);


      if (self.isBad):
         msgElement = document.createElement("CompilerErrorMsg");
         msgElement.appendChild(document.createTextNode(self.badMsg));
         blockElement.appendChild(msgElement);


      # Location
      locationElement = document.createElement("Location");
      xElement = document.createElement("X");
      xElement.appendChild(document.createTextNode(str(x)));
      locationElement.appendChild(xElement);

      yElement = document.createElement("Y");
      yElement.appendChild(document.createTextNode(str(y)));
      locationElement.appendChild(yElement);
      blockElement.appendChild(locationElement);

      if (isCollapsed):
         collapsedElement = document.createElement("Collapsed");
         blockElement.appendChild(collapsedElement);


      if (commentNode != None):
         blockElement.appendChild(commentNode);


      if (self.hasBeforeConnector() and self.getBeforeBlockID() != Block.NULL):
         blockIdElement = document.createElement("BeforeBlockId");
         blockIdElement.appendChild(document.createTextNode(self.getBeforeBlockID() ));
         blockElement.appendChild(blockIdElement);


      if (self.hasAfterConnector() and self.getAfterBlockID() != Block.NULL):
         blockIdElement = document.createElement("AfterBlockId");
         blockIdElement.appendChild(document.createTextNode(self.getAfterBlockID()));
         blockElement.appendChild(blockIdElement);


      if (self.plug != None):
        	plugElement = document.createElement("Plug");
        	blockConnectorNode = self.plug.getSaveNode(document, "plug");
        	plugElement.appendChild(blockConnectorNode);
        	blockElement.appendChild(plugElement);

      if (len(self.sockets) > 0) :
         socketsElement = document.createElement("Sockets");
         socketsElement.setAttribute("num-sockets", str(len(self.sockets)));
         for con in self.getSockets():
            blockConnectorNode = con.getSaveNode(document, "socket");
            socketsElement.appendChild(blockConnectorNode);

         blockElement.appendChild(socketsElement);
         # sockets tricky... because what if
         # one of the sockets is expanded?  should the socket keep a reference
         # to their genus socket?  and so should the expanded one?


      # save block properties that are not specified within genus
      # i.e. properties that were created/specified during runtime

      '''
      if (not properties.isEmpty()):
         propertiesElement = document.createElement("LangSpecProperties");
         for (Entry<String, String> property : properties.entrySet()):
            propertyElement = document.createElement("LangSpecProperty");
            propertyElement.setAttribute("key", property.getKey());
            propertyElement.setAttribute("value", property.getValue());

            propertiesElement.appendChild(propertyElement);

         blockElement.appendChild(propertiesElement);

      '''
      return blockElement;



   def loadBlockFrom(node, canvas):
      '''
      * Loads Block information from the specified node and return a Block
      * instance with the loaded information
      * @param workspace The workspace in use
      * @param node Node cantaining desired information
      * @return Block instance containing loaded information
      '''
      from blocks.BlockStub import BlockStub
      
      block = None;
      id = None;
      genusName = None;
      label = None;
      pagelabel = None;
      badMsg = None;
      beforeID = None;
      afterID = None;
      plug = None;
      sockets = []
      blockLangProperties = {};
      hasFocus = False;

      # stub information if this node contains a stub
      isStubBlock = False;
      stubParentName = None;
      stubParentGenus = None;
      pattern = "(.*)"
      # Matcher nameMatcher;
      
      if (node.tag == ("BlockStub")):
         isStubBlock = True;
         blockNode = None;
         stubChildren = node.getchildren();
         for infoNode in stubChildren:
            if (infoNode.tag == ("StubParentName")):
               stubParentName = infoNode.getTextContent();
            elif (infoNode.tag ==("StubParentGenus")) :
               stubParentGenus = infoNode.getTextContent();
            elif (infoNode.tag == ("Block")):
               blockNode = infoNode;

         node = blockNode;


      if (node.tag == ("Block")):
         # load attributes
         if("id" in node.attrib):
            id = node.attrib["id"]  #+ canvas.getMaxReservedID() #translateLong(workspace, long(nameMatcher.group(1)), idMapping);
            # BUG: id may conflict with the new Block
            # bug fix: HE Qichen 2012-2-24

         if("genus-name" in node.attrib):
            genusName = node.attrib["genus-name"]


         # load optional items
         if("has-focus" in node.attrib):
            hasFocus = True if node.attrib["has-focus"] == ("yes") else False

         # load elements
         children = node.getchildren()

         for child in children:
            if (child.tag == ("Label")):
                 label = child.text;
            elif (child.tag == ("PageLabel")):
                 pagelabel = child.getTextContent;
            elif (child.tag == ("CompilerErrorMsg")):
                 badMsg = child.text;
            elif  (child.tag == ("BeforeBlockId")):
                 beforeID = child.text
            elif  (child.tag == ("AfterBlockId")):
                 afterID = child.text
            elif  (child.tag == ("Plug")):
               plugs = child.getchildren(); #there should only one child

               for plugNode in plugs:
                  if (plugNode.tag == ("BlockConnector")):
                     plug = BlockConnector.loadBlockConnector(plugNode,);

            elif  (child.tag == ("Sockets")) :
               socketNodes = child.getchildren();
               for  socketNode in socketNodes:
                  if (socketNode.tag == ("BlockConnector")) :
                     sockets.append(BlockConnector.loadBlockConnector(socketNode));

            elif  (child.tag == ("LangSpecProperties")):
               blockLangProperties = {}
               propertyNodes = child.getchildren();
               key = None;
               value = None;
               for  propertyNode in propertyNodes:
                  if (propertyNode.tag == ("LangSpecProperty")):
                     nameMatcher = re.match(pattern,propertyNode.getAttribute("key"))
                     if (nameMatcher): # will be true
                       key = nameMatcher.group(1);

                     opt_item = propertyNode.getAttributes("value");
                     if (opt_item != None):
                        nameMatcher = re.match(pattern,opt_item)
                        if (nameMatcher): # will be true
                           value = nameMatcher.group(1);
                        else:
                           value = propertyNode.getTextContent();

                     if (key != None and value != None):
                        blockLangProperties.put(key, value);
                        key = None;
                        value = None;


         #assert genusName != null && id != null : "Block did not contain required info id: " + id + " genus: " + genusName;
         #create block or block stub instance
         if (not isStubBlock):
            if (label == None):
               block = Block.createBlockFromID(canvas, genusName, True, id);
            else:
               block = Block.createBlockFromID(canvas,  genusName,True, id,label);

         else:
            #assert label != null : "Loading a block stub, but has a null label!";
            block = BlockStub(node.workspace, id, genusName, label, stubParentName, stubParentGenus);


         if (plug != None):
            # Some callers can change before/after/plug types. We have
            # to synchronize so that we never have both.
            # assert beforeID == null && afterID == null;
            block.plug = plug;
            block.removeBeforeAndAfter();

         if (len(sockets) > 0):
             block.sockets = sockets;

         if (beforeID != None):
             block.before.setConnectorBlockID(beforeID);

         if (afterID != None):
             block.after.setConnectorBlockID(afterID);

         if (pagelabel != None):
             block.pageLabel = pagelabel;

         if (badMsg != None):
             block.isBad = True;
             block.badMsg = badMsg;

         block.hasFocus = hasFocus;

         #load language dependent properties
         if (blockLangProperties != None and not len(blockLangProperties) == 0):
             block.properties = blockLangProperties;


         return block;


      return None;

   def removeBeforeAndAfter(self):
      self.before = None;
      self.after = None;
