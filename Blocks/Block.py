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
import re
from Blocks.BlockGenus import BlockGenus
from Blocks.BlockConnector import BlockConnector

class Block():

   # The ID that is to be assigned to the next new block
   NEXT_ID = 1

   # Defines a NULL id for a Block
   NULL = -1

   # A universal hashmap of all the Block instances
   ALL_BLOCKS= {}

   def __init__(self, genusName, linkToStubs=True, id=-1,label=None):
      if(id == -1):
         id = Block.NEXT_ID
         Block.NEXT_ID+=1

      if(id >= Block.NEXT_ID):
         Block.NEXT_ID = id+1

      #print ("id=%d,NEXT_ID=%d"%(id,Block.NEXT_ID))
      if (label == None):
         label = BlockGenus.getGenusWithName(genusName).getInitialLabel()

      if (id in Block.ALL_BLOCKS):
        dup = Block.ALL_BLOCKS.get(id);
        print("pre-existing block is: {0} with genus {1} and label {2}".format(id,dup.getGenusName(),dup.getBlockLabel()));
        raise Exception("Block id: {0} already exists!  BlockGenus {1}, label: {2}".format(id,genusName,label))
        #assert !ALL_BLOCKS.containsKey(id) : "Block id: "+id+" already exists!  BlockGenus "+genusName+" label: "+label;
      self.linkToStubs = linkToStubs
      self.blockID = id;
      self.pageLabel = ""
      self.hasFocus = False;
      self.isBad = False;
      self.disabled = False
      self.sockets = []
      self.argumentDescriptions = []
      self.outputConnection = None
      
      # copy connectors from BlockGenus
      #try:
      genus = BlockGenus.getGenusWithName(genusName)
      if(genus == None):
          raise Exception("genusName: "+genusName+" does not exist.")

      # copy the block connectors from block genus
      iter = genus.getInitSockets();
      for con in iter:
         self.sockets.append(BlockConnector(
            con.kind,
            con.positionType,
            con.label,
            con.isLabelEditable,
            con.isExpandable,
            con.connBlockID,
            con.expandGroup))


      if(genus.getInitPlug() != None):
         self.plug = BlockConnector(
            genus.getInitPlug().kind,
            genus.getInitPlug().positionType,
            genus.getInitPlug().label,
            genus.getInitPlug().isLabelEditable,
            genus.getInitPlug().isExpandable,
            genus.getInitPlug().connBlockID,
            genus.getInitPlug().expandGroup);
      else:
         self.plug = None

      if(genus.getInitBefore() != None):
         self.before = BlockConnector(
            genus.getInitBefore().kind,
            genus.getInitBefore().positionType,
            genus.getInitBefore().label,
            genus.getInitBefore().isLabelEditable,
            genus.getInitBefore().isExpandable,
            genus.getInitBefore().connBlockID,
            genus.getInitBefore().expandGroup);
      else:
         self.before = None

      if(genus.getInitAfter() != None):
         self.after = BlockConnector(
            genus.getInitAfter().kind,
            genus.getInitAfter().positionType,
            genus.getInitAfter().label,
            genus.getInitAfter().isLabelEditable,
            genus.getInitAfter().isExpandable,
            genus.getInitAfter().connBlockID,
            genus.getInitAfter().expandGroup);
      else:
         self.after = None

      self.genusName = genusName;

      self.label = label;

      #arguumentIter = genus.getInitialArgumentDescriptions()
      #for arg in arguumentIter:
      #	argumentDescriptions.add(arg.trim())


      self.expandGroups = []

      # add to ALL_BLOCKS
      # warning: publishing this block before constructor finishes has the
      # potential to cause some problems such as data races
      # other threads could access this block from getBlock()
      #print(self.blockID)
      Block.ALL_BLOCKS[self.blockID] = self

      # add itself to stubs hashmap
      # however factory blocks will have entries in hashmap...
      #if(linkToStubs and self.hasStubs()):
      #    BlockStub.putNewParentInStubMap(this.blockID)


      #except:
      #  exc_type, exc_obj, exc_tb = sys.exc_info()
      #  fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      #  print(exc_type, fname, exc_tb.tb_lineno,exc_obj)

   def __del__(self):
      pass

   def getBlockID(self):
      '''
      * Returns the block ID of this
      * @return the block ID of this
      '''
      return self.blockID

   def getInputTargetBlock(self, name):
    socket = self.getSocketByName(name.lower())
    if(socket == None):
      return None
      
    blockID = socket.getBlockID()
    if(blockID == -1):
      return None
    else:
      return Block.getBlock(blockID)
      
   def getBlock(blockID):
      if(blockID in Block.ALL_BLOCKS):
         return Block.ALL_BLOCKS[blockID]
      else:
         #print( Block.ALL_BLOCKS )
         #print("Not found")
         return None

   def isInfix(self):
      genus = self.getGenus()
      return genus.isInfix()

   def getGenus(self):
     return BlockGenus.getGenusWithName(self.genusName)

   def changeLabelTo(self,  label):
      #self.genusName = genusName;
      self.label = label #BlockGenus.getGenusWithName(genusName).getInitialLabel();

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

   def getBlockLabel(self):
      return self.getGenus().getLabelPrefix()+self.label+self.getGenus().getLabelSuffix();

   def setBlockLabel(self, newLabel):
      from Blocks.BlockStub import BlockStub
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
      #assert index < sockets.size() : "Index "+index+" is greater than the num of sockets: "+sockets.size()+" of "+this;
      return self.sockets[index];

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
      from Blocks.BlockStub import BlockStub
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
      return self.before.getBlockID();

   def getAfterBlockID(self):
      if (self.after == None):
         return Block.NULL;
      return self.after.getBlockID();

   def getPlugBlockID(self):
      if(self.plug == None):
         return Block.NULL;
      return self.plug.getBlockID();


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
      expandSockets = self.getExpandGroup(expandGroups, group);
      #assert expandSockets != null;

      # Search for the socket to insert after.
      index = len(sockets) - 1;
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
      expandSockets = getExpandGroup(expandGroups, group);
      #assert expandSockets != null;

      # Search for the first socket in the group, if not the expandable
      # one.
      label = expandSockets.get(0).getLabel();
      index = getSocketIndex(socket);
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
         con = sockets[index];
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
         conn = sockets.get(i);
         if (conn == self.socket):
             if (first == -1):first = i;
             else: return true;
         elif (conn.getPositionType().equals(socket.getPositionType()) and
                  conn.isExpandable() == socket.isExpandable() and
                  conn.initKind().equals(socket.initKind()) and
                  conn.getExpandGroup().equals(socket.getExpandGroup())):
             if (first == -1): first = i;
             else: return true;


      # If the socket is the first and last of its kind, then we can NOT
      # remove it. (We also can't remove it if they're both -1, obviously.)
      return False;

   def blockDisconnected(self,disconnectedSocket):
      '''
      * Informs this Block that a block has disconnected from the specified disconnectedSocket
      * @param disconnectedSocket
      '''
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
         if (socket.getBlockID() == otherBlockID):
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
         labelElement.appendChild(document.createTextNode(label));
         blockElement.appendChild(labelElement);


      if (self.pageLabel != None and self.pageLabel != ""):
         pageLabelElement = document.createElement("PageLabel");
         pageLabelElement.appendChild(document.createTextNode(self.pageLabel));
         blockElement.appendChild(pageLabelElement);


      if (self.isBad):
         msgElement = document.createElement("CompilerErrorMsg");
         msgElement.appendChild(document.createTextNode(badMsg));
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
         blockIdElement.appendChild(document.createTextNode(str(self.getBeforeBlockID())));
         blockElement.appendChild(blockIdElement);


      if (self.hasAfterConnector() and self.getAfterBlockID() != Block.NULL):
         blockIdElement = document.createElement("AfterBlockId");
         blockIdElement.appendChild(document.createTextNode(str(self.getAfterBlockID())));
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



   def loadBlockFrom(node):
      '''
      * Loads Block information from the specified node and return a Block
      * instance with the loaded information
      * @param workspace The workspace in use
      * @param node Node cantaining desired information
      * @return Block instance containing loaded information
      '''

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
            id = int(node.attrib["id"]) #translateLong(workspace, long(nameMatcher.group(1)), idMapping);
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
                 label = child.getTextContent();
            elif (child.tag == ("PageLabel")):
                 pagelabel = child.getTextContent();
            elif (child.tag == ("CompilerErrorMsg")):
                 badMsg = child.getTextContent();
            elif  (child.tag == ("BeforeBlockId")):
                 beforeID = int(child.text)
            elif  (child.tag == ("AfterBlockId")):
                 afterID = int(child.text)
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
               key = null;
               value = null;
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
               block = Block( genusName, True, id);
            else:
               block = Block( genusName,True, id,label);

         else:
            #assert label != null : "Loading a block stub, but has a null label!";
            block = BlockStub(workspace, id, genusName, label, stubParentName, stubParentGenus);


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
