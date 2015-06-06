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
from Blocks.LabelWidget import LabelWidget
from Blocks.Block import Block


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

  def __init__(self,initLabelText, labelType, isEditable, blockID, hasComboPopup, tooltipBackground):
      from Blocks.RenderableBlock import RenderableBlock
      from Blocks.FactoryRenderableBlock import FactoryRenderableBlock
      from Blocks.BlockGenus import BlockGenus
      
      self.widget= LabelWidget(initLabelText, Block.getBlock(blockID).getColor().darker(), tooltipBackground)
      self.zoom = 1.0
      self.initLabelText = initLabelText
      self.labelType = labelType
      self.blockID = blockID
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
      if (Block.getBlock(blockID).hasSiblings()) :
        #/Map<String, String> siblings = new HashMap<String, String>();
        siblingsNames = Block.getBlock(blockID).getSiblingsList();
        print(siblingsNames)
        siblings = []
        sibling = [Block.getBlock(blockID).getGenusName(), Block.getBlock(blockID).getInitialLabel()]
        siblings.append(sibling)
        for i in range(0,  len(siblingsNames)):
          #print(siblingsNames[i])
          oldBlock = Block.getBlock(self.blockID)
          siblings.append([siblingsNames[i], BlockGenus.getGenusWithName(oldBlock.getGenusName()).getInitialLabel()])
        
        #print(siblings)
        self.widget.setSiblings(hasComboPopup and Block.getBlock(blockID).hasSiblings(), siblingsNames);
      
      self.widget.fireTextChanged = self.textChanged
      self.widget.fireGenusChanged = self.labelChanged

  def labelChanged(self, label):
    from Blocks.RenderableBlock import RenderableBlock
    if(self.widget.hasSiblings):
      oldBlock = Block.getBlock(self.blockID);
      oldBlock.changeLabelTo(label);
      rb = RenderableBlock.getRenderableBlock(self.blockID);
      rb.repaintBlock();
      #Workspace.getInstance().notifyListeners(new WorkspaceEvent(rb.getParentWidget(), blockID, WorkspaceEvent.BLOCK_GENUS_CHANGED));

  def textChanged(self, text):
    from Blocks.RenderableBlock import RenderableBlock
    if (self.labelType == BlockLabel.Type.NAME_LABEL or 
        self.labelType == BlockLabel.Type.PORT_LABEL) and  (Block.getBlock(self.blockID).isLabelEditable()):
      if (self.labelType == (BlockLabel.Type.NAME_LABEL)):
        Block.getBlock(self.blockID).setBlockLabel(text);

      plug = Block.getBlock(self.blockID).getPlug();
      # Check if we're connected to a block. If we are and the the block we're connected to
      # has stubs, update them.
      if (plug != None and plug.getBlockID() != Block.NULL):
        if (Block.getBlock(plug.getBlockID()) != None):
          if(Block.getBlock(plug.getBlockID()).isProcedureDeclBlock() and
            Block.getBlock(plug.getBlockID()).hasStubs()):
            # Blocks already store their socket names when saved so it is not necessary
            # nor desired to call the connectors changed event again.
            if (Block.getRenderableBlock(plug.getBlockID()).isLoading()):
              BlockStub.parentConnectorsChanged(workspace, plug.getBlockID());

      rb = RenderableBlock.getRenderableBlock(self.blockID);

      if(rb != None and not rb.isLoading):
        rb.reformBlockShape()
        rb.updateBuffImg()
        #rb.repaint()
        pass
          #workspace.notifyListeners(new WorkspaceEvent(workspace, rb.getParentWidget(), blockID, WorkspaceEvent.BLOCK_RENAMED));

  def getAbstractWidth(self):
    if(self.widget.hasSiblings):
      return (self.widget.width()/self.zoom)-LabelWidget.DROP_DOWN_MENU_WIDTH;
    else:
      width = self.widget.width()
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

if __name__ == '__main__':
    main()
