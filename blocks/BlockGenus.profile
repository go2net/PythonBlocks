�}q (X'   C:\Python34\lib\importlib\_bootstrap.pyqK�X   __init__q�q(KKG        G        }qX'   C:\Python34\lib\importlib\_bootstrap.pyqMX   _get_module_lockq�qKstqX'   C:\Python34\lib\importlib\_bootstrap.pyq	MWX   _validate_bytecode_headerq
�q(KKG        G        }qX'   C:\Python34\lib\importlib\_bootstrap.pyqM�X   get_codeq�qKstqX    qK X   statq�q(KKG        G        }qX'   C:\Python34\lib\importlib\_bootstrap.pyqKDX
   _path_statq�qKstqhK X
   is_builtinq�q(KKG        G        }qX'   C:\Python34\lib\importlib\_bootstrap.pyqM�X	   find_specq�qKstqX   profileq K XP�  import os,sys
from PyQt4 import QtCore,QtGui
from blocks.BlockConnector import BlockConnector
from blocks.BlockConnectorShape import BlockConnectorShape

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class BlockGenus():
    EMPTY_STRING = ""

    # mapping of genus names to BlockGenus objects
    # only BlockGenus may add to this map
    nameToGenus = {}
    familyBlocks = {}
    families = {}
    def __init__(self,genusName = None, newGenusName=None):

        self.properties = {}
        
        # make sure key module and function exist
        self.properties['module_name'] = ''
        self.properties['function_name'] = ''
        
        self.blockImageMap = {}        

        self.family = {}
        self.sockets = []
        self.stubList = []
        self.argumentDescriptions = []
        self.expandGroups = []

        self.areSocketsExpandable = False
        self.hasDefArgs = False

        self._isLabelEditable = False
        self.isLabelValue = False
        self._isVarLabel = False
        self.isPageLabelEnabled = False
        
        self._isStarter = False
        self._isTerminator = False

        self._isStarterInConfig = False
        self._isTerminatorInConfig = False
        
        self.__isInfix = False
        self.labelMustBeUnique = True

        self.color = 0
        self.isDirty = False
        
        self.initLabel = ""
        self.kind = ""
        self.labelPrefix = ""
        self.labelSuffix = ""
        self._genusName = ""
        self.familyName = ''

        self.plug = None
        self.before = None
        self.after = None

        if(genusName == None and newGenusName == None): return
        #assert !genusName.equals(newGenusName)  : "BlockGenuses must have unique names: "+genusName;

        genusToCopy = BlockGenus.getGenusWithName(genusName)
        
        self.familyName = genusToCopy.familyName
        
        self.expandGroups = genusToCopy.expandGroups    # doesn't change
        self.areSocketsExpandable = genusToCopy.areSocketsExpandable
        self.color = QtGui.QColor(genusToCopy.color.red(), genusToCopy.color.green(), genusToCopy.color.blue())        
        self.hasDefArgs = genusToCopy.hasDefArgs
        
        
        self.initLabel = genusToCopy.initLabel
        
        self._isLabelEditable = genusToCopy._isLabelEditable;
        #self._isVarLabel = genusToCopy._isVarLabel;
        self.isLabelValue = genusToCopy.isLabelValue;
        self.isStarter = genusToCopy.isStarter;
        self.isTerminator = genusToCopy.isTerminator;
        self.__isInfix = genusToCopy.__isInfix;
        self.kind = genusToCopy.kind;
        self.labelPrefix = genusToCopy.labelPrefix;
        self.labelSuffix = genusToCopy.labelSuffix;

        if(genusToCopy.plug != None):
            self.plug = BlockConnector(
                genusToCopy.plug.kind,
                genusToCopy.plug.type,
                genusToCopy.plug.positionType,
                genusToCopy.plug.label,
                genusToCopy.plug.isLabelEditable,
                genusToCopy.plug.isExpandable,
                genusToCopy.plug.connBlockID,
                genusToCopy.plug.expandGroup)

        if(genusToCopy.before != None):
            self.before = BlockConnector(
                genusToCopy.before.kind,
                genusToCopy.before.type,
                genusToCopy.before.positionType,
                genusToCopy.before.label,
                genusToCopy.before.isLabelEditable,
                genusToCopy.before.isExpandable,
                genusToCopy.before.connBlockID,
                genusToCopy.before.expandGroup)

        if(genusToCopy.after != None):
            self.after = BlockConnector(
                genusToCopy.after.kind,
                genusToCopy.after.type,
                genusToCopy.after.positionType,
                genusToCopy.after.label,
                genusToCopy.after.isLabelEditable,
                genusToCopy.after.isExpandable,
                genusToCopy.after.connBlockID,
                genusToCopy.after.expandGroup)
                
        
        for socketToCopy in genusToCopy.sockets:
            socket = BlockConnector(
                socketToCopy.kind,
                socketToCopy.type,
                socketToCopy.positionType,
                socketToCopy.label,
                socketToCopy.isLabelEditable,
                socketToCopy.isExpandable,
                socketToCopy.connBlockID,
                socketToCopy.expandGroup) 
            self.sockets.append(socket)
            
        for key in genusToCopy.properties:
            self.properties[key] = genusToCopy.properties[key]

        self._genusName = newGenusName
        
        BlockGenus.nameToGenus[newGenusName] = self

    @property
    def isStarter(self):
        """I'm the 'x' property."""
        return self._isStarter

    @isStarter.setter
    def isStarter(self, value):
        if (self._kind == 'data' or
            self._kind == 'variable' or
            self._kind == 'function'):
            self._isStarter = True
        else:
            self._isStarter = value
            self._isStarterInConfig = value
          
        if (not self._isStarter):
            self.before = BlockConnector('' ,BlockConnectorShape.getCommandShapeName(), BlockConnector.PositionType.TOP, "", False, False, -1);      
        else:
            self.before = None
          
    @isStarter.deleter
    def isStarter(self):
        del self._isStarter

    @property
    def isTerminator(self):
        """I'm the 'x' property."""
        return self._isTerminator

    @isTerminator.setter
    def isTerminator(self, value):
        if (self._kind == 'data' or
            self._kind == 'variable' or
            self._kind == 'function'):
            self._isTerminator = True
        else:
            self._isTerminator = value
            self._isTerminatorInConfig = value
          
        if (not self._isTerminator):
            self.after = BlockConnector('' ,BlockConnectorShape.getCommandShapeName(),  BlockConnector.PositionType.BOTTOM, "", False, False, -1);
        else:
            self.after = None
          
    @isTerminator.deleter
    def isTerminator(self):
        del self._isTerminator
     
    @property
    def kind(self):
        """I'm the 'x' property."""
        return self._kind

    @kind.setter
    def kind(self, value):
        self._kind = value
        if (self._kind == 'data' or
             self._kind == 'variable' or
             self._kind == 'function'):
          self.isStarter = True
          self.isTerminator = True
        else:
          self.isStarter = self._isStarterInConfig
          self.isTerminator = self._isTerminatorInConfig

    @property
    def genusName(self):
        """I'm the 'x' property."""
        return self._genusName

    @genusName.setter
    def genusName(self, value):
        self._genusName = value
        if(self._genusName not in BlockGenus.nameToGenus):
            BlockGenus.nameToGenus[self._genusName] = self          
  
    def __eq__(self, other):
        if(other == None): return False
        if(self.color != other.color): return False
        if(self._kind != other._kind): return False
        if(self.initLabel != other.initLabel): return False
        if(self.labelPrefix != other.labelPrefix): return False
        if(self.labelSuffix != other.labelSuffix): return False
        if(self.isStarter != other.isStarter): return False
        if(self.isTerminator != other.isTerminator): return False
        
        for key in self.properties:
            if(key in self.properties and key in other.properties):
                if(self.properties[key] != other.properties[key]):
                    return False
            else:
                return False   
    
        return True
    
    def copyDataFrom(self,  other):
        if(other == None): return
        self.color = other.color
        self._kind = other._kind
        self.initLabel = other.initLabel
        self.labelPrefix = other.labelPrefix
        self.labelSuffix = other.labelSuffix
        self.isStarter = other.isStarter
        self.isTerminator = other.isTerminator
        
        if('module_name' in other.properties):
            self.properties['module_name'] = other.properties['module_name']
        else:
            self.properties['module_name'] = ''
        if('function_name' in other.properties):    
            self.properties['function_name'] = other.properties['function_name']    
    
    def getGenusWithName(name):
        if(name in BlockGenus.nameToGenus):
            return BlockGenus.nameToGenus[name]
        else:
            return None

    def getInitPlug(self):
          return self.plug;

    def loadGenusDescription(descriptions, genus):
        for description in descriptions:
            if(description.tag == "text"):
                genus.blockDescription = description.text
            elif(description.tag == "arg-description"):
                #    int argumentIndex = 0;
                argumentDescription = ""

                if("n" in description.attrib):
                    genus.argumentIndex = int(description.attrib["n"]);

                if("doc-name" in description.attrib):
                    argumentDescription = description.attrib["doc-name"];

                argumentDescription = description.text
                if(argumentDescription != ""):
                    genus.argumentDescriptions.append(argumentDescription)
        
    
    def getConnectorInfoList(self):
        connector_list = []
        if(self.plug != None):
            connector_list.append(self.plug.getConnectorInfo())
    
        for socket in self.sockets:
            connector_list.append(socket.getConnectorInfo())
            
        return connector_list  

    def loadBlockConnectorInformation(connectors, genus):
        '''
         * Loads the BlockConnector information of the specified genus
         * @param connectors NodeList of connector information to load from
         * @param genus BlockGenus to load block connector information onto
        '''
        for connector in connectors:
            if(connector.tag == "BlockConnector"):
                label = "";
                connectorType = "none";
                connectorKind = 0  # where 0 is socket, 1 is plug
                positionType = "single"
                isExpandable = False
                isLabelEditable = False
                expandGroup = ""
                defargname = None
                defarglabel = None

                if 'connector-kind' in connector.attrib:
                    connectorKind = connector.attrib['connector-kind'];
                if 'connector-type' in connector.attrib:
                    connectorType = connector.attrib['connector-type']
                if 'position-type' in connector.attrib:
                    positionType = connector.attrib['position-type']
                if 'is-expandable' in connector.attrib:
                    isExpandable = True if connector.attrib['is-expandable'] == "yes" else False
                if 'label-editable' in connector.attrib:
                    isLabelEditable = True if connector.attrib['label-editable'] == "yes" else False

                # load optional items
                if 'label' in connector.attrib:
                    label = connector.attrib['label']

                if 'expand-group' in connector.attrib:
                    expandGroup = connector.attrib['expand-group']


                for defarg in connector.getchildren():
                    if(defarg.tag == "DefaultArg"):

                        if 'genus-name' in defarg.attrib:
                            defargname = defarg.attrib['genus-name']

                         # assert BlockGenus.nameToGenus.get(defargname) != null : "Unknown BlockGenus: "+defargname;
                        # warning: if this block genus does not have an editable label, the label being loaded does not
                        # have an affect
                        if 'label' in defarg.attrib:
                            defarglabel = defarg.attrib['label']

                        genus.hasDefArgs = True;


                # set the position type for this new connector, by default its set to single
                if(positionType == "mirror"):
                    position_type = BlockConnector.PositionType.MIRROR
                elif(positionType == ("bottom")):
                    position_type = BlockConnector.PositionType.BOTTOM
                else:
                    position_type = BlockConnector.PositionType.SINGLE

                socket = BlockConnector(
                    connectorKind, 
                    connectorType,
                    position_type,
                    label,
                    isLabelEditable,
                    isExpandable,
                    -1,
                    expandGroup);

                # add def args if any
                if(defargname != None):
                    socket.setDefaultArgument(defargname, defarglabel);


                #set the connector kind
                if(connectorKind == 'socket'):
                    genus.sockets.append(socket);
                else:
                    genus.plug= socket;
                    #assert (!socket.isExpandable()) : genus.genusName + " can not have an expandable plug.  Every block has at most one plug.";


                if(socket.isExpandable):
                    genus.areSocketsExpandable = True;

                if (len(expandGroup) > 0):
                    genus.addToExpandGroup(genus.expandGroups, socket);

    def loadBlockImages(images, genus):
        from blocks.BlockImageIcon import ImageLocation
        from blocks.BlockImageIcon import BlockImageIcon
        '''
        * Loads the images to be drawn on the visible block instances of this
        * @param images NodeList of image information to load from
        * @param genus BlockGenus instance to load images onto
        '''
        #the current working directory of this
    
        location = None;
        isEditable = False
        textWrap = False
        for i in range(0,len(images)):
            imageNode = images[i]
            if(imageNode.tag == ("Image")):
                #load image properties
                if("block-location" in imageNode.attrib):
                    location = imageNode.attrib["block-location"];

                if("image-editable" in imageNode.attrib):
                    isEditable = True if imageNode.attrib["image-editable"] == "yes" else False;

                if("wrap-text" in imageNode.attrib):
                    textWrap = True if imageNode.attrib["wrap-text"] == "yes" else False;

                width = -1;
                height = -1;

                if("width" in imageNode.attrib):
                    width = int(imageNode.attrib["width"]);

                if("height" in imageNode.attrib):
                    height = int(imageNode.attrib["height"]);

                # load actual image

                for imageLocationNode in imageNode.getchildren():
                    if(imageLocationNode.tag == ("FileLocation")):
                        fileLocation = imageLocationNode.text
                        try:
                            if(fileLocation != '' and location != None):
                                # translate location String to ImageLocation representation
                                imgLoc= ImageLocation.getImageLocation(location)
                                #assert imgLoc != null : "Invalid location string loaded: "+imgLoc;

                                #store in blockImageMap
                                icon = QPixmap(os.getcwd() +fileLocation)
                                if(width > 0 and height > 0):                                
                                    icon = icon.scaled(width, height)
                                    print('Genus ICON width=%d,height=%d'%(width, height))

                                genus.blockImageMap[imgLoc] =  BlockImageIcon(icon, imgLoc, isEditable, textWrap)

                        except:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(exc_type, fname, exc_tb.tb_lineno,exc_obj)
                            
    def getLangSpecProperties(self):
        properities = []
        for key in self.properties:
            properity = {}
            properity['key'] = key
            properity['value'] = self.properties[key]
            properities.append(properity)
        return properities

    def loadLangDefProperties(properties, genus):
        '''
         * Loads the language definition properties of the specified genus
         * @param properties NodeList of properties to load from file
         * @param genus BlockGenus to load the properties onto
        '''
        key = None
        value = None

        for l in range(0,len(properties)):
            prop = properties[l]
            if(prop.tag == ("LangSpecProperty")):

                if("key" in prop.attrib):
                    key = prop.attrib["key"]
                if("value" in prop.attrib):
                    value = prop.attrib["value"]
                else:
                    value = prop.text

                if(key != None and value != None):
                    genus.properties[key] = value

    def getProperty(self, property) :
        if(property in self.properties):
          return self.properties[property]
        else:
          return ''


    def loadStubs(stubs, genus):
        '''
        * Loads the stub information of the specified genus
        * @param stubs NodeList of stub information to load
        * @param genus BlockGenus to load stub information onto
        '''
        stubGenus = "";
        for m in range(0,len(stubs)):
            stub = stubs[m];
            if(stub.tag == ("Stub")):
                if("stub-genus" in stub.attrib):
                    stubGenus = stub.attrib["stub-genus"]

                if(len(stub.getchildren()) > 0):
                    # this stub for this genus deviates from generic stub
                    # generate genus by copying one of generic ones

                    newStubGenus = BlockGenus(stubGenus, stubGenus + genus.genusName);
                    # load unique stub genus properties
                    for stubChild in stub.getchildren():
                        if(stubChild.tag == ("LangSpecProperties")):
                            BlockGenus.loadLangDefProperties(stubChild.getchildren(), newStubGenus);

                    BlockGenus.nameToGenus[newStubGenus.genusName] = newStubGenus
                    genus.stubList.append(newStubGenus.genusName);
                else:
                    # not a unique stub, add generic stub
                    genus.stubList.append(stubGenus);
            


    def loadBlockGenera(root):
        '''
        * Loads the all the initial BlockGenuses and BlockGenus families of this language
        * @param root the Element carrying the specifications of the BlockGenuses
        '''      
        
        # # # # # # # # # # # # # # # # # # /
        # / LOAD BLOCK FAMILY INFORMATION # /
        # # # # # # # # # # # # # # # # # # /
        families = root.findall("BlockFamilies/BlockFamily")

        #BlockGenus.famMap = {}
        for i in range(0,len(families)):
          familyNode=families[i]
          familyName = ''
          if("name" in familyNode.attrib):
              familyName = familyNode.attrib["name"]
                    
          children = familyNode.getchildren()
          
          family = {}                  
          for j in range(0, len(children)):
             member = children[j]
             if (member.tag == ("FamilyMember")): # a family member entry
                name = member.text
                label = name
                if("label" in member.attrib):
                  label = member.attrib["label"] 
                family[name] = label
          
          if(familyName != ''):
             if(familyName not in BlockGenus.families):
                BlockGenus.families[familyName] = family
             else:
                print('Duplicated BlockFamily')
        
        genusNodes=root.findall("BlockGenuses/BlockGenus"); # look for genus
     
        for genusNode in genusNodes: # find them
          BlockGenus.loadGenus(genusNode)

    def getColorInfo(color):
        color_info = {}
        color_info['r'] = color.red()
        color_info['g'] = color.green()
        color_info['b'] = color.blue()
        return color_info     

    def getGenusInfo(self):
        genusInfo = {}
        genusInfo['name'] = self.genusName
        genusInfo['color'] = BlockGenus.getColorInfo(self.color)
        genusInfo['kind'] = self.kind
        genusInfo['family_name'] = self.familyName
        genusInfo['initlabel'] = self.initLabel
        genusInfo['editable-label'] = self._isLabelEditable
        genusInfo['var-label'] = self._isVarLabel
        genusInfo['label-unique'] = self.labelMustBeUnique
        genusInfo['is-starter'] = self.isStarter
        genusInfo['is-terminator'] = self.isTerminator        
        genusInfo['is-label-value'] = self.isLabelValue
        genusInfo['label-prefix'] = self.labelPrefix
        genusInfo['label-suffix'] = self.labelSuffix
        genusInfo['page-label-enabled'] = self.isPageLabelEnabled
        
        genusInfo['LangSpecProperties'] = self.getLangSpecProperties()
        genusInfo['BlockConnectors'] = self.getConnectorInfoList()
        
        return genusInfo
    
    def loadGenus(genusNode):
        '''
        # # # # # # # # # # # # # # # # # /
        # / LOAD BLOCK GENUS PROPERTIES # /
        # # # # # # # # # # # # # # # # # /
        '''
        newGenus = BlockGenus();
        # first, parse out the attributes
        if 'name' in genusNode.attrib:
            newGenus.genusName = genusNode.attrib["name"]
            BlockGenus.nameToGenus[newGenus.genusName] = newGenus
            
        # assert that no other genus has this name
        # assert nameToGenus.get(newGenus.genusName) == null : "Block genus names must be unique.  A block genus already exists with this name: "+newGenus.genusName;
        if 'color' in genusNode.attrib:
            col = genusNode.attrib["color"].split();
            if(len(col) == 3):
                newGenus.color = QtGui.QColor(int(col[0]), int(col[1]), int(col[2]));
            else:
                newGenus.color = QtCore.Qt.BLACK;

        if 'kind' in genusNode.attrib:
            newGenus.kind = genusNode.attrib["kind"]

        if 'family_name' in genusNode.attrib:
            newGenus.familyName = genusNode.attrib["family_name"]
         
            newGenus.family = BlockGenus.families[newGenus.familyName]
          
            if(newGenus.familyName not in BlockGenus.familyBlocks):
                BlockGenus.familyBlocks[newGenus.familyName] = []
              
            BlockGenus.familyBlocks[newGenus.familyName].append(newGenus)

        if 'initlabel' in genusNode.attrib:
            newGenus.initLabel = genusNode.attrib["initlabel"]
        else:
            newGenus.initLabel = ''            

        if 'editable-label' in genusNode.attrib:
            newGenus._isLabelEditable = True if genusNode.attrib["editable-label"] == ("yes") else False

        if 'var-label' in genusNode.attrib:
            newGenus._isVarLabel = True if genusNode.attrib["var-label"] == ("yes") else False
        else:
            newGenus._isVarLabel = False

        if 'label-unique' in genusNode.attrib:
            newGenus.labelMustBeUnique = True if genusNode.attrib["label-unique"] == ("yes") else False
        else:
            newGenus.labelMustBeUnique = False
        
        if 'is-starter' in genusNode.attrib:
            newGenus.isStarter= True if genusNode.attrib["is-starter"] == ("yes") else False
        else:
            newGenus.isStarter = False          
          
        if 'is-terminator' in genusNode.attrib:
            newGenus.isTerminator= True if genusNode.attrib["is-terminator"] == ("yes") else False
        else:
            newGenus.isTerminator = False
          
        if 'is-label-value' in genusNode.attrib:
            newGenus.isLabelValue= True if genusNode.attrib["is-label-value"] == ("yes") else False
        else:
            newGenus.isLabelValue = False

        if 'label-prefix' in genusNode.attrib:
            newGenus.labelPrefix= genusNode.attrib["label-prefix"]
        else:
            newGenus.labelPrefix = ''
            
        if 'label-suffix' in genusNode.attrib:
            newGenus.labelSuffix= genusNode.attrib["label-suffix"]
        else:
            newGenus.labelSuffix = ''
            
        if 'page-label-enabled' in genusNode.attrib:
            newGenus.isPageLabelEnabled= True if genusNode.attrib["page-label-enabled"] == ("yes") else False
        else:
            newGenus.isPageLabelEnabled = ''
            
        # if genus is a data genus (kind=data) or a variable block (and soon a declaration block)
        # it is both a starter and terminator
        # in other words, it should not have before and after connectors
        #if(newGenus.isDataBlock() or newGenus.isVariableDeclBlock() or newGenus.isFunctionBlock()):
        #  newGenus.isStarter = True;
        #  newGenus.isTerminator = True;

        # next, parse out the elements
        genusChildren=genusNode.getchildren()

        for genusChild in genusChildren:

            if (genusChild.tag == ("description")):
                  # # # # # # # # # # # # # # # # # #
                  # / LOAD BLOCK GENUS DESCRIPTION # /
                  # # # # # # # # # # # # # # # # # #
                  BlockGenus.loadGenusDescription(genusChild.getchildren(), newGenus);
            elif (genusChild.tag == ("BlockConnectors")):
                # # # # # # # # # # # # # # # # # # # #
                # / LOAD BLOCK CONNECTOR INFORMATION # /
                # # # # # # # # # # # # # # # # # # # #
                BlockGenus.loadBlockConnectorInformation(genusChild.getchildren(), newGenus);

                # if genus has two connectors both of bottom position type than this block is an infix
                # operator
                if( newGenus.sockets != None and len(newGenus.sockets) == 2 and
                    newGenus.sockets[0].getPositionType() == BlockConnector.PositionType.BOTTOM and
                    newGenus.sockets[1].getPositionType() == BlockConnector.PositionType.BOTTOM):
                    newGenus.__isInfix = True
            elif(genusChild.tag == ("Images")):
                # # # # # # # # # # # # /
                # / LOAD BLOCK IMAGES # /
                # # # # # # # # # # # # /
                BlockGenus.loadBlockImages(genusChild.getchildren(), newGenus);
            elif(genusChild.tag == ("LangSpecProperties")):
                # # # # # # # # # # # # # # # # # # # # /
                # / LOAD LANGUAGE SPECIFIC PROPERTIES # /
                # # # # # # # # # # # # # # # # # # # # /
                BlockGenus.loadLangDefProperties(genusChild.getchildren(), newGenus);

            elif (genusChild.tag == ("Stubs")):
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # / LOAD STUBS INFO AND GENERATE GENUSES FOR EACH STUB # /
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                BlockGenus.loadStubs(genusChild.getchildren(), newGenus);


        #  John's code to add command sockets... probably in the wrong place
        #if (not newGenus.isStarter):
        #  newGenus.before = BlockConnector(BlockConnectorShape.getCommandShapeName(),'' , BlockConnector.PositionType.TOP, "", False, False, -1);

        #if (not newGenus.isTerminator):
        #  newGenus.after = BlockConnector(BlockConnectorShape.getCommandShapeName(), '' , BlockConnector.PositionType.BOTTOM, "", False, False, -1);


        return newGenus

    def hasSiblings(self):
        '''
        * Returns true if this genus has siblings; False otherwise.
        * Note: For a genus to have siblings, its label must be uneditable.  An editable label
        * interferes with the drop down menu widget that blocks with siblings have.
        * @return true if this genus has siblings; False otherwise.
        '''
        return (len(self.family) > 0)

    def getSiblingsList(self):
        return self.family

    def getInitSockets(self):
        '''
        * Returns the initial set of sockets of this
        * @return the initial set of sockets of this
        '''
        return self.sockets

    def getStubList(self):
        '''
         * Returns a list of the stub kinds (or stub genus names) of this; if this genus does not have any stubs,
         * returns an empty list
         * @return a list of the stub kinds (or stub genus names) of this; if this genus does not have any stubs,
         * returns an empty list
        '''
        return self.stubList

    def hasStubs(self):
        '''
         * Returns true is this genus has stubs (references such as getters, setters, etc.); False otherwise
         * @return true is this genus has stubs (references such as getters, setters, etc.); False otherwise
        '''
        return (len(self.stubList) > 0)

    def hasDefaultArgs(self):
        '''
         * Returns true iff any one of the connectors for this genus has default arguments; False otherwise
         * @return true iff any one of the connectors for this genus has default arguments; False otherwise
        '''
        return self.hasDefArgs

    def isCommandBlock(self):
        '''
         * Returns true if this block is a command block (i.e. forward, say, etc.); False otherwise
         * @return true if this block is a command block (i.e. forward, say, etc.); False otherwise
        '''
        return self.kind == "command"

    def isDataBlock(self):
        '''
         * Returns true if this block is a data block a.k.a. a primitive (i.e. number, string, boolean);
         * False otherwise
         * @return Returns true if this block is a data block a.k.a. a primitive (i.e. number, string, boolean);
         * False otherwise
        '''
        return self.kind == "data"

    def isFunctionBlock(self):
        '''
         * Returns true iff this block is a function block, which takes in an input and produces an
         * output. (i.e. math blocks, arctan, add to list); False otherwise.
         * @return true iff this block is a function block, which takes in an input and produces an
         * output. (i.e. math blocks, arctan, add to list); False otherwise.
        '''
        return self.kind == "function"

    def isVariableDeclBlock(self):
        '''
         * Returns true if this block is a variable declaration block; False otherwise
         * @return true if this block is a variable declaration block; False otherwise
        '''
        return self.kind == "variable"

    def isProcedureDeclBlock(self):
        '''
         * Returns true if this block is a procedure declaration block; False otherwise
         * @return true if this block is a procedure declaration block; False otherwise
        '''
        return self.kind == "procedure"

    def isProcedureParamBlock(self) :
        '''
         * Returns true if this block is a procedure parameter block; False otherwise
        '''
        return self.kind == "param"

    def isDeclaration(self):
        '''
         * Returns true if this genus is a declaration block.  Declaration blocks define variables and procedures.
        '''
        return self.isVariableDeclBlock() or self.isProcedureDeclBlock()

    def isListRelated(self) :
        '''
         * Returns true if this block is a list or a list operator (determined by whether it has at
         * least one list connector of any type); False otherwise.
         * @return is determined by whether it has at least one list connector of any type.
        '''
        hasListConn = False;
        if (self.plug != None):
            hasListConn = self.plug.getKind().contains("list");
        for socket in self.sockets:
            hasListConn |= socket.getKind().contains("list");
        return hasListConn;

    def hasBeforeConnector(self):
        '''
         * Returns true if this genus has a "before" connector; False otherwise.
         * @return true is this genus has a "before" connector; False otherwise.
        '''
        return not self.isStarter;

    def hasAfterConnector(self):
        '''
         * Returns true if this genus has a "after" connector; False otherwise.
         * @return true if this genus has a "after" connector; False otherwise.
        '''
        return not self.isTerminator;

    def isLabelValue(self):
        '''
         * Returns true if the value of this genus is contained within the label of this; False
         * otherwise
         * @return true if the value of this genus is contained within the label of this; False
         * otherwise
        '''
        return self.isLabelValue

#    def isLabelEditable(self):
        '''
         * Returns true if the label of this is editable; False otherwise
         * @return true if the label of this is editable; False otherwise
        '''
#         return self.isLabelEditable

    def isPageLabelSetByPage(self):
        '''
         * Returns true iff this genus can have page label.
         * @return true iff this genus can have page label
        '''
        return self.isPageLabelEnabled

    def areSocketsExpandable(self):
        '''
         * Returns true iff this genus's sockets are expandable
        '''
        return self.areSocketsExpandable

    def isInfix(self):
        '''
         * Returns true iff this genus is an infix operator.  This genus must be supporting two bottom sockets.
         * @return true iff this genus is an infix operator.  This genus must be supporting two bottom sockets.
        '''
        return self.__isInfix

    def getInitialLabel(self):
        '''
         * Returns the initial label of this
         * @return the initial label of this
        '''
        return self.initLabel

    def getInitBefore(self):
        return self.before;

    def getInitAfter(self):
        return self.after;

    def getLabelPrefix(self):
        '''
         * Returns the String block label prefix of this
         * @return the String block label prefix of this
        '''
        return self.labelPrefix

    def getLabelSuffix(self):
        '''
         * Returns the String block label prefix of this
         * @return the String block label prefix of this
        '''
        return self.labelSuffix

    def getInitBlockImageMap(self):
        return self.blockImageMap;

    def getBlockDescription(self):
        '''
         * Returns the String block text description of this.
         * Also known as the block tool tip, or block description.
         * If no descriptions exists, return null.
         * @returns the String block text description of this or NULL.
        '''
        return self.blockDescription

    def getColor(self):
        return self.color;
q!�q"(KKG        G?�      }q#h K X   profilerq$�q%Kstq&X'   C:\Python34\lib\importlib\_bootstrap.pyq'K2X
   _path_joinq(�q)(KTKTG        G        }q*(X'   C:\Python34\lib\importlib\_bootstrap.pyq+M�X   cache_from_sourceq,�q-KX'   C:\Python34\lib\importlib\_bootstrap.pyq.M�h�q/KRutq0X'   C:\Python34\lib\importlib\_bootstrap.pyq1MKX   createq2�q3(KKG        G        }q4X'   C:\Python34\lib\importlib\_bootstrap.pyq5M�X   _load_unlockedq6�q7Kstq8hK X   allocate_lockq9�q:(KKG        G        }q;hKstq<h(KKG        G        }q=X'   C:\Python34\lib\importlib\_bootstrap.pyq>McX
   _find_specq?�q@KstqAX'   C:\Python34\lib\importlib\_bootstrap.pyqBM�h�qC(KKG        G        }qDX'   C:\Python34\lib\importlib\_bootstrap.pyqEM6X   path_hook_for_FileFinderqF�qGKstqHX'   C:\Python34\lib\importlib\_bootstrap.pyqIMX	   __enter__qJ�qK(KKG        G        }qLX'   C:\Python34\lib\importlib\_bootstrap.pyqMM�X   _find_and_loadqN�qOKstqPhK X
   rpartitionqQ�qR(K$K$G        G        }qS(X'   C:\Python34\lib\importlib\_bootstrap.pyqTM�X   load_moduleqU�qVKh-KX'   C:\Python34\lib\importlib\_bootstrap.pyqWM�X   _find_and_load_unlockedqX�qYKh/KutqZhK X   rstripq[�q\(K�K�G        G        }q]X'   C:\Python34\lib\importlib\_bootstrap.pyq^K4X
   <listcomp>q_�q`K�stqaX'   C:\Python34\lib\importlib\_bootstrap.pyqbM�X	   <genexpr>qc�qd(KKG        G        }qehK X   extendqf�qgKstqhhK X   execqi�qj(KKG        G?�      }qk(X'   C:\Python34\lib\importlib\_bootstrap.pyqlM9X   _call_with_frames_removedqm�qnKh"KutqoX'   C:\Python34\lib\importlib\_bootstrap.pyqpM8h�qq(KKG        G        }qrh@KstqshK X   getattrqt�qu(KKG        G        }qv(X'   C:\Python34\lib\importlib\_bootstrap.pyqwM�X   init_module_attrsqx�qyKX'   C:\Python34\lib\importlib\_bootstrap.pyqzM�X   _load_backward_compatibleq{�q|K	utq}hK X   lowerq~�q(K�K�G        G        }q�(X'   C:\Python34\lib\importlib\_bootstrap.pyq�MX   _fill_cacheq��q�KkX'   C:\Python34\lib\importlib\_bootstrap.pyq�M*X	   <setcomp>q��q�Kwutq�hK X   _fix_co_filenameq��q�(KKG        G        }q�X'   C:\Python34\lib\importlib\_bootstrap.pyq�M�X   _compile_bytecodeq��q�Kstq�X'   C:\Python34\lib\importlib\_bootstrap.pyq�KX   _relax_caseq��q�(KKG        G        }q�h/Kstq�X'   C:\Python34\lib\importlib\_bootstrap.pyq�M�X   _handle_fromlistq��q�(KKG        G?�      }q�X-   F:\projects\PythonBlocks\blocks\BlockGenus.pyq�KX   <module>q��q�Kstq�X'   C:\Python34\lib\importlib\_bootstrap.pyq�M8X   cachedq��q�(KKG        G        }q�hyKstq�X'   C:\Python34\lib\importlib\_bootstrap.pyq�M=X   _path_hooksq��q�(KKG        G        }q�X'   C:\Python34\lib\importlib\_bootstrap.pyq�MNX   _path_importer_cacheq��q�Kstq�hO(KKG        G?�      }q�(hK X   load_dynamicq��q�Kh�KhK X
   __import__q��q�Kutq�X'   C:\Python34\lib\importlib\_bootstrap.pyq�M	X
   __import__q��q�(KKG        G        }q�hK X   load_dynamicq��q�Kstq�X'   C:\Python34\lib\importlib\_bootstrap.pyq�M_X
   path_statsq��q�(KKG        G        }q�hKstq�X'   C:\Python34\lib\importlib\_bootstrap.pyq�M�h{�q�(KKG        G?�      }q�X'   C:\Python34\lib\importlib\_bootstrap.pyq�M�h6�q�Kstq�X'   C:\Python34\lib\importlib\_bootstrap.pyq�M�hJ�q�(KKG        G        }q�h7Kstq�hK X   loadsqŇq�(KKG        G        }q�h�Kstq�hK X
   isinstanceqɇq�(KKG        G        }q�(X'   C:\Python34\lib\importlib\_bootstrap.pyq�MnX	   _get_specq͇q�KX'   C:\Python34\lib\importlib\_bootstrap.pyq�M�X   _sanity_checkqЇq�Kh�Kutq�h�(KKG?�      G?�      }q�X'   C:\Python34\lib\importlib\_bootstrap.pyq�M9hm�q�Kstq�hK X   hasattrqׇq�(KKG        G        }q�(h�Kh�Kh7Kh3Kutq�X'   C:\Python34\lib\importlib\_bootstrap.pyq�MJX   parentq܇q�(KKG        G        }q�hyKstq�X'   C:\Python34\lib\importlib\_bootstrap.pyq�K-X   _r_longq�q�(KKG        G        }q�hKstq�hK X   acquire_lockq�q�(KKG        G        }q�(X'   C:\Python34\lib\importlib\_bootstrap.pyq�M�X   _gcd_importq�q�KX'   C:\Python34\lib\importlib\_bootstrap.pyq�MHhJ�q�Kutq�X'   C:\Python34\lib\importlib\_bootstrap.pyq�K�X   releaseq�q�(KKG        G        }q�(X'   C:\Python34\lib\importlib\_bootstrap.pyq�MX   __exit__q�q�KX'   C:\Python34\lib\importlib\_bootstrap.pyq�M%X   _lock_unlock_moduleq��q�Kutq�hG(KKG        G        }q�h�Kstq�X'   C:\Python34\lib\importlib\_bootstrap.pyq�MX   _check_name_wrapperq��q�(KKG        G?�      }q�(hKh|Kutq�X'   C:\Python34\lib\importlib\_bootstrap.pyr   MtX   spec_from_file_locationr  �r  (KKG        G        }r  X'   C:\Python34\lib\importlib\_bootstrap.pyr  M�h͇r  Kstr  X'   C:\Python34\lib\importlib\_bootstrap.pyr  M X   cbr  �r	  (KKG        G        }r
  (h�KhOKutr  X'   C:\Python34\lib\importlib\_bootstrap.pyr  K\X   _path_isdirr  �r  (KKG        G        }r  hGKstr  X'   C:\Python34\lib\importlib\_bootstrap.pyr  KNX   _path_is_mode_typer  �r  (KKG        G        }r  (X'   C:\Python34\lib\importlib\_bootstrap.pyr  KWX   _path_isfiler  �r  Kj  Kutr  X'   C:\Python34\lib\importlib\_bootstrap.pyr  Mh�r  (KKG        G        }r  (X'   C:\Python34\lib\importlib\_bootstrap.pyr  Mnh͇r  Kj  Kutr  hK X   lenr  �r   (KKG        G        }r!  (X'   C:\Python34\lib\importlib\_bootstrap.pyr"  K8X   _path_splitr#  �r$  KhKutr%  hK X   joinr&  �r'  (KVKVG        G        }r(  (h)KTh-Kutr)  hK X	   is_frozenr*  �r+  (KKG        G        }r,  hqKstr-  h�(KKG        G        }r.  h�Kstr/  X'   C:\Python34\lib\importlib\_bootstrap.pyr0  M�h�r1  (KKG        G        }r2  h@Kstr3  hK X
   from_bytesr4  �r5  (KKG        G        }r6  h�Kstr7  X'   C:\Python34\lib\importlib\_bootstrap.pyr8  MX   _verbose_messager9  �r:  (KUKUG        G        }r;  (X'   C:\Python34\lib\importlib\_bootstrap.pyr<  M�h�r=  KhVKhKh�Kh/KOutr>  hK X   addr?  �r@  (KwKwG        G        }rA  h�KwstrB  j  (KKG        G        }rC  X'   C:\Python34\lib\importlib\_bootstrap.pyrD  M�h�rE  KstrF  h(KKG        G        }rG  (hKKh�KutrH  h�(KKG        G        }rI  h�KstrJ  X'   C:\Python34\lib\importlib\_bootstrap.pyrK  K�X   acquirerL  �rM  (KKG        G        }rN  (hKKh�KutrO  h�(KKG        G        }rP  h�KstrQ  hK X   anyrR  �rS  (KKG        G        }rT  (j=  KX'   C:\Python34\lib\importlib\_bootstrap.pyrU  K�h�rV  KX'   C:\Python34\lib\importlib\_bootstrap.pyrW  M�X
   is_packagerX  �rY  KutrZ  hK X   readr[  �r\  (KKG        G        }r]  X'   C:\Python34\lib\importlib\_bootstrap.pyr^  MUX   get_datar_  �r`  Kstra  hK X   OpenKeyrb  �rc  (K
K
G        G        }rd  X'   C:\Python34\lib\importlib\_bootstrap.pyre  MyX   _open_registryrf  �rg  K
strh  X'   C:\Python34\lib\importlib\_bootstrap.pyri  Mh�rj  (KKG        G        }rk  hOKstrl  h�(KKG        G        }rm  hOKstrn  hK X   listdirro  �rp  (KKG        G        }rq  h�Kstrr  h�(KKG        G        }rs  hKstrt  h�(KKG        G?�      }ru  X'   C:\Python34\lib\importlib\_bootstrap.pyrv  M9hm�rw  Kstrx  X'   C:\Python34\lib\importlib\_bootstrap.pyry  M�hU�rz  (KKG        G?�      }r{  X'   C:\Python34\lib\importlib\_bootstrap.pyr|  Mh��r}  Kstr~  h�(KKG        G        }r  j1  Kstr�  h/(KKG        G        }r�  h�Kstr�  hK X	   get_identr�  �r�  (KKG        G        }r�  (jM  Kh�Kutr�  h�(KKG        G        }r�  h@Kstr�  h`(KTKTG        G        }r�  h)KTstr�  jg  (KKG        G        }r�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  M�X   _search_registryr�  �r�  Kstr�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  MbX   _execr�  �r�  (KKG        G        }r�  h7Kstr�  j=  (KKG        G        }r�  h7Kstr�  h@(KKG        G        }r�  hYKstr�  hy(KKG        G        }r�  h3Kstr�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  M�h�r�  (KKG        G        }r�  h7Kstr�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  M�h�r�  (KKG        G        }r�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  M�h͇r�  Kstr�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  MRX   has_locationr�  �r�  (KKG        G        }r�  hyKstr�  hK X   rsplitr�  �r�  (KKG        G        }r�  j$  Kstr�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  M�hc�r�  (KKG        G        }r�  jS  Kstr�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  K�hJ�r�  (KKG        G        }r�  jz  Kstr�  hK X   release_lockr�  �r�  (KKG        G        }r�  (X'   C:\Python34\lib\importlib\_bootstrap.pyr�  MLh�r�  KhKKh�Kutr�  hn(KKG        G?�      }r�  (h�KhVKX'   C:\Python34\lib\importlib\_bootstrap.pyr�  M�X   exec_moduler�  �r�  KX'   C:\Python34\lib\importlib\_bootstrap.pyr�  M�hX�r�  Kutr�  hK X   setattrr�  �r�  (KKG        G        }r�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  M�hX�r�  Kstr�  j�  (KKG        G        }r�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  M�h�r�  Kstr�  hK X	   partitionr�  �r�  (KxKxG        G        }r�  (h�Kwh�Kutr�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  M�h�r�  (KKG        G        }r�  hYKstr�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  K�X   _new_moduler�  �r�  (KKG        G        }r�  h3Kstr�  hK X
   startswithr�  �r�  (KKG        G        }r�  h�Kstr�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  M�hc�r�  (KKG        G        }r�  hK X   anyr�  �r�  Kstr�  h(KKG        G        }r�  (j  Kh�Kh/Kutr�  j�  (KKG        G        }r�  h@Kstr�  hK X   getcwdr�  �r�  (KKG        G        }r�  h�Kstr�  jV  (KKG        G        }r�  hVKstr�  h7(KKG        G?�      }r�  hYKstr�  h�(KKG        G        }r�  h/Kstr�  h-(KKG        G        }r�  (h�KhKutr�  j$  (KKG        G        }r�  (h-KjY  Kutr�  j`  (KKG        G        }r�  hKstr�  X'   C:\Python34\lib\importlib\_bootstrap.pyr�  K�h�r�  (KKG        G        }r�  jz  Kstr�  hK X
   setprofiler�  �r�  (KKG        G        }r�  h"Kstr�  j�  (KKG        G        }r   j�  Kstr  hK X   endswithr  �r  (KKG        G        }r  h�Kstr  j  (KKG        G        }r  jE  Kstr  jY  (KKG        G        }r  hVKstr	  X'   C:\Python34\lib\importlib\_bootstrap.pyr
  K�hc�r  (KKG        G        }r  hK X   anyr  �r  Kstr  hK X   formatr  �r  (K�K�G        G        }r  (j�  Kh�Kh�Kkh/KOX'   C:\Python34\lib\importlib\_bootstrap.pyr  M�hX�r  Kutr  h�(KKG        G        }r  h�Kstr  X'   C:\Python34\lib\importlib\_bootstrap.pyr  M7h�r  (KKG        G        }r  j  Kstr  h�(KKG        G        }r  h�Kstr  hg(KKG        G        }r  hCKstr  X'   C:\Python34\lib\importlib\_bootstrap.pyr   MPX   get_filenamer!  �r"  (KKG        G        }r#  h�Kstr$  j�  (KKG        G        }r%  h@Kstr&  h(KKG        G        }r'  j�  Kstr(  hY(KKG        G?�      }r)  hOKstr*  X/   C:\Python34\lib\site-packages\PyQt4\__init__.pyr+  Kh��r,  (KKG        G        }r-  hK X   execr.  �r/  Kstr0  h�(KKG        G?�      }r1  hjKstr2  u.