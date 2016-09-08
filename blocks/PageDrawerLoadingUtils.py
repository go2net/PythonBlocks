
from PyQt4 import QtGui
from blocks.Block import Block
from blocks.FactoryRenderableBlock import FactoryRenderableBlock

import re

class PageDrawerLoadingUtils():

   def __init__(self):
      pass

   def loadBlockDrawerSets(block_drawersets, manager):
        import json
        if(block_drawersets == ''): return
        f=open(block_drawersets)
        data=json.load(f)

        if 'block_drawer_sets' in data:
            block_drawer_sets = data['block_drawer_sets']
            for drawerElement in block_drawer_sets:
                if 'drawer' in drawerElement and 'genus-list' in drawerElement:
                    drawerName = drawerElement['drawer']
                    canvas = manager.addStaticDrawerNoPos(drawerName, QtGui.QColor(100,100,100,0));  
                    drawerRBs = []
                    member = drawerElement['genus-list']
                    for genusName in member:
                        newBlock = Block.createBlock(canvas, genusName, False)
                        if(newBlock == None): continue
                        
                        rb = FactoryRenderableBlock.from_block(canvas, newBlock,False, QtGui.QColor(225,225,225,100))
                        drawerRBs.append(rb);
                        FactoryRenderableBlock.factoryRBs[genusName] = rb
                    manager.addStaticBlocks(drawerRBs, drawerName) 
        return

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








