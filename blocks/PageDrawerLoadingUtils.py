
from PyQt4 import QtGui
from blocks.Block import Block
from blocks.FactoryRenderableBlock import FactoryRenderableBlock

import re

class PageDrawerLoadingUtils():

   def __init__(self):
      pass

   def loadBlockDrawerSets(root, manager):

      drawerSetNodes = root.findall("BlockDrawerSets/BlockDrawerSet")

      for drawerSetNode in drawerSetNodes:
         drawerNodes=drawerSetNode.getchildren()

         # retreive drawer information of this bar
         for drawerNode in drawerNodes:
            if(drawerNode.tag == "BlockDrawer"):
               drawerName = None
               if("name" in drawerNode.attrib):
               	drawerName = drawerNode.attrib["name"]

               manager.addStaticDrawerNoPos(drawerName, QtGui.QColor(100,100,100,0));

               drawerBlocks = drawerNode.getchildren()
               blockNode = None
               drawerRBs = []
               for blockNode in drawerBlocks:
                  if(blockNode.tag == "BlockGenusMember"):
                     genusName = blockNode.text
                     newBlock = Block.createBlock(genusName, False)
                     drawerRBs.append(FactoryRenderableBlock.from_blockID(manager, newBlock.blockID,False, QtGui.QColor(225,225,225,100)));

               manager.addStaticBlocks(drawerRBs, drawerName);


   def getNodeValue(node, nodeKey):
      pattern = "(.*)"
      opt_item = node.getAttribute(nodeKey);
      if(opt_item != ""):
         nameMatcher = re.match(pattern,opt_item)
         if (nameMatcher != None):
            return nameMatcher.group(1);
      return "";


   def getBooleanValue(node, nodeKey):
      bool = PageDrawerLoadingUtils.getNodeValue(node, nodeKey);
      if(bool != ""):
         if (bool == ("no")): return False;
         else: return True;

      return True;

   def getIntValue(node, nodeKey):
      num = PageDrawerLoadingUtils.getNodeValue(node, nodeKey);
      if(num!= ""):
         return int(num)
      return 0;








