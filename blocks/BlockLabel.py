#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      A21059
#
# Created:     06/03/2015
# Copyright:   (c) A21059 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PyQt4 import QtGui
from blocks.LabelWidget import LabelWidget
from blocks.Block import Block


class BlockLabel():
  def enum(*sequential, **named):
       enums = dict(zip(sequential, range(len(sequential))), **named)
       return type('Enum', (), enums)

  Type = enum("NAME_LABEL", "PAGE_LABEL", "PORT_LABEL", "DATA_LABEL")

  blockFontSmall_Bold   = QtGui.QFont("Arial",  6, QtGui.QFont.Bold);
  blockFontMedium_Bold  = QtGui.QFont("Arial",  8, QtGui.QFont.Bold);
  blockFontLarge_Bold   = QtGui.QFont("Arial", 10, QtGui.QFont.Bold);
  blockFontSmall_Plain  = QtGui.QFont("Arial",  6, QtGui.QFont.Normal);
  blockFontMedium_Plain = QtGui.QFont("Arial",  8, QtGui.QFont.Normal);
  blockFontLarge_Plain  = QtGui.QFont("Arial", 10, QtGui.QFont.Normal);

  def __init__(self,parent, initLabelText, prefix, suffix, labelType, isEditable, blockID, hasComboPopup, tooltipBackground):
      from blocks.RenderableBlock import RenderableBlock
      from blocks.FactoryRenderableBlock import FactoryRenderableBlock
      
      self.widget= LabelWidget(parent, blockID, initLabelText, prefix, suffix, Block.getBlock(blockID).getColor().darker(), tooltipBackground)
      self.parent = parent
      self.zoom = 1.0
      self.initLabelText = initLabelText
      self.labelType = labelType
      self.blockID = blockID
      self.hasComboPopup = hasComboPopup
      # Only editable if the isEditable parameter was true, the label is either a Block's name or
      # socket label, the block can edit labels, and the block is not in the factory.
      self.widget.setEditable(
            isEditable and
            (labelType == BlockLabel.Type.NAME_LABEL or labelType == BlockLabel.Type.PORT_LABEL) and
            Block.getBlock(blockID).isLabelEditable() and
            not isinstance(RenderableBlock.getRenderableBlock(blockID),FactoryRenderableBlock));
      if(labelType == None or labelType == (BlockLabel.Type.NAME_LABEL)):
         self.widget.setFont(BlockLabel.blockFontLarge_Bold);
      elif(labelType == (BlockLabel.Type.PAGE_LABEL)):
         self.widget.setFont(BlockLabel.blockFontMedium_Bold);
      elif(labelType ==(BlockLabel.Type.PORT_LABEL)):
        self.widget.setFont(BlockLabel.blockFontMedium_Bold);
      elif(labelType == (BlockLabel.Type.DATA_LABEL)):
        self.widget.setFont(BlockLabel.blockFontMedium_Bold);
      
      # set initial text
      self.widget.updateLabelText(initLabelText);
      # add and show the textLabel initially
      self.widget.setEditingState(False);
      
      #famList = {}
      #if (Block.getBlock(blockID).hasSiblings()) :
      #  famList = Block.getBlock(blockID).getSiblingsList();      

      #self.widget.setMenu();
      
      self.widget.fireTextChanged = self.textChanged
      self.widget.fireGenusChanged = self.labelChanged
      #self.widget.fireMenuChanged = self.menuChanged
  
  def menuEnabled(self):
      return self.hasComboPopup and Block.getBlock(self.blockID).hasSiblings()

  def labelChanged(self, label):
    from blocks.RenderableBlock import RenderableBlock

    if(self.widget.hasMenu):
      oldBlock = Block.getBlock(self.blockID);
      oldBlock.changeLabelTo(label);
      rb = RenderableBlock.getRenderableBlock(self.blockID);
      rb.repaintBlock();
      #Workspace.getInstance().notifyListeners(new WorkspaceEvent(rb.getParentWidget(), blockID, WorkspaceEvent.BLOCK_GENUS_CHANGED));

  def textChanged(self, text):
    from blocks.RenderableBlock import RenderableBlock
    from blocks.BlockStub import BlockStub
    
    if (self.labelType == BlockLabel.Type.NAME_LABEL or 
        self.labelType == BlockLabel.Type.PORT_LABEL) and  (Block.getBlock(self.blockID).isLabelEditable()):
      if (self.labelType == (BlockLabel.Type.NAME_LABEL)):
        Block.getBlock(self.blockID).setBlockLabel(text);

      plug = Block.getBlock(self.blockID).getPlug();
      # Check if we're connected to a block. If we are and the the block we're connected to
      # has stubs, update them.
      if (plug != None and plug.blockID != Block.NULL):
        if (Block.getBlock(plug.blockID) != None):
          if(Block.getBlock(plug.blockID).isProcedureDeclBlock() and
            Block.getBlock(plug.blockID).hasStubs()):
            # Blocks already store their socket names when saved so it is not necessary
            # nor desired to call the connectors changed event again.
            if (Block.getRenderableBlock(plug.blockID).isLoading()):
              BlockStub.parentConnectorsChanged(self.workspace, plug.blockID);

      rb = RenderableBlock.getRenderableBlock(self.blockID);

      if(rb != None and not rb.isLoading):
        rb.reformBlockShape()
        rb.updateBuffImg()
        #rb.repaint()
        pass
          #workspace.notifyListeners(new WorkspaceEvent(workspace, rb.getParentWidget(), blockID, WorkspaceEvent.BLOCK_RENAMED));

  def onRenameVariable(self, old_name, new_name):
    from blocks.FactoryRenderableBlock import FactoryRenderableBlock
    from blocks.BlockGenus import BlockGenus
    
    block = Block.getBlock(self.blockID)
    familyMap = block.getCustomerFamily();
    
    findVar = False
    for key in familyMap:
      if(familyMap[key] == old_name):
        familyMap[key] = new_name
        findVar = True 
        
    if(not findVar):
        familyMap[new_name] = new_name
    

    factoryBlock = FactoryRenderableBlock.factoryRBs[block.getGenusName()]
    for rb in factoryBlock.child_list:
      blockLabel = rb.blockLabel
      #blockLabel.widget.setMenu();
      if(blockLabel.getText() == old_name):            
            blockLabel.labelChanged(new_name)
    
    #factoryBlock.blockLabel.widget.setMenu()
    if(factoryBlock.blockLabel.getText() == old_name):
      factoryBlock.blockLabel.labelChanged(new_name)
    
    if(block.getGenus().familyName in BlockGenus.familyBlocks):
      for genus in  BlockGenus.familyBlocks[block.getGenus().familyName]:
          genusName = genus.genusName
          if genusName not in FactoryRenderableBlock.factoryRBs: continue
          factoryBlock = FactoryRenderableBlock.factoryRBs[genusName]
          for rb in factoryBlock.child_list:
            blockLabel = rb.blockLabel
            #blockLabel.widget.setMenu();
            if(blockLabel.getText() == old_name):
              blockLabel.labelChanged(new_name)
          
          #factoryBlock.blockLabel.widget.setMenu();
          if(factoryBlock.blockLabel.getText() == old_name):
            #print(factoryBlock)
            factoryBlock.blockLabel.labelChanged(new_name)
    
  def getAbstractWidth(self):
    if(self.widget.hasMenu):
      return (self.widget.width()/self.zoom)-9;
    else:
      return (self.widget.width()/self.zoom);

  def getAbstractHeight(self):
      return (self.widget.height()/self.zoom);

  def rescale(self,x):return x*self.zoom
  def descale(self,x):return x/self.zoom
  def setPixelLocation(self,x, y): self.widget.move(x, y)

  def getText(self):
      return self.widget.getText();

  def setZoomLevel(self, newZoom):
      self.zoom = newZoom;
      #self.widget.setZoomLevel(newZoom);

  def setText(self,text):
      #pass
      self.widget.setText(text);

  def setParent(self,parent):
      self.parent = parent
      self.widget.setParent(parent);

  def getParent(self):
      return self.parent

  def raise_(self):
      self.widget.raise_()

