#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      A21059
#
# Created:     03/03/2015
# Copyright:   (c) A21059 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PyQt4 import QtCore,QtGui
from Blocks.Block import Block
from Blocks.FactoryRenderableBlock import FactoryRenderableBlock

import re

class PageDrawerLoadingUtils():

   def __init__(self):
      passss

   def loadBlockDrawerSets(root, manager):

      pattern = "(.*)"
      drawerSetNodes = root.findall("BlockDrawerSets/BlockDrawerSet")

      for drawerSetNode in drawerSetNodes:
         drawerNodes=drawerSetNode.getchildren()

         # retreive drawer information of this bar
         for drawerNode in drawerNodes:
            if(drawerNode.tag == "BlockDrawer"):
               drawerName = None
               buttonColor =  QtCore.Qt.blue
               #StringTokenizer col;
               if("name" in drawerNode.attrib):
               	drawerName = drawerNode.attrib["name"]

               # get drawer's color:
               if("button-color" in drawerNode.attrib):
                  col = drawerNode.attrib["button-color"].split();
                  if(len(col) == 3):
                     buttonColor = QtGui.QColor(int(col[0]), int(col[1]), int(col[2]));
                  else:
                     buttonColor = QtCore.Qt.BLACK;


               canvas = manager.addStaticDrawerNoPos(drawerName, QtGui.QColor(100,100,100,0));

               #if(True): continue;
               # get block genuses in drawer and create blocks
               drawerBlocks = drawerNode.getchildren()
               blockNode = None
               drawerRBs = []
               for blockNode in drawerBlocks:
                  if(blockNode.tag == "BlockGenusMember"):
                     genusName = blockNode.text
                     #assert BlockGenus.getGenusWithName(genusName) != null : "Unknown BlockGenus: "+genusName;

                     # don't link factory blocks to their stubs because they will
                     # forever remain inside the drawer and never be active
                     newBlock = Block(genusName, False)
                     drawerRBs.append(FactoryRenderableBlock(manager, newBlock.getBlockID(),QtGui.QColor(225,225,225,100)));

               manager.addStaticBlocks(drawerRBs, drawerName);


   def getNodeValue(node, nodeKey):
      pattern = "(.*)"
      opt_item = node.getAttribute(nodeKey);
      if(opt_item != ""):
         nameMatcher = re.match(pattern,opt_item)
         if (nameMatcher != None):
            return nameMatcher.group(1);
      return "";


   def getColorValue(node, nodeKey):
      color = PageDrawerLoadingUtils.getNodeValue(node, nodeKey);
      if(color != ""):
         col = StringTokenizer(color);
         if(col.countTokens() == 3):
            return QtGui.QColor(Integer.parseInt(col.nextToken()), Integer.parseInt(col.nextToken()), Integer.parseInt(col.nextToken()));

      return None;



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


   def loadPagesAndDrawers( root, manager):
      from Workspace import Workspace
      from WorkspaceController import WorkspaceController











