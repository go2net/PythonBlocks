#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      A21059
#
# Created:     25/03/2015
# Copyright:   (c) A21059 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PyQt4 import QtGui,QtCore
from blocks.RenderableBlock import RenderableBlock
from blocks.WorkspaceWidget import WorkspaceWidget

class Canvas(QtGui.QWidget,WorkspaceWidget):
   def __init__(self):
      QtGui.QWidget.__init__(self)
      pass


class BlockCanvas(QtGui.QScrollArea):

   def __init__(self):
      from blocks.WorkspaceController import WorkspaceController
      QtGui.QScrollArea.__init__(self)

      self.hValue = 0
      self.vValue = 0
      self.canvas = Canvas();
      #self.canvas.setStyleSheet("background-color: rgba(225, 225, 0,255);")
      #self.setStyleSheet("background-color: rgba(225, 0, 225,255);")
      self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
      self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
      self.setWidgetResizable(False)
      self.setWidget(self.canvas)

      #Scroll Area Layer add
      self.layout = QtGui.QHBoxLayout(self)
      self.canvas.setLayout(self.layout)

      self.setStyleSheet("background-color: rgba(225, 225, 225,0);")
      self.pages = []
      self.dividers = []
      self.block_list = {}

      #self.blocks = []

      screen = QtGui.QDesktopWidget().availableGeometry()
      self.canvas.resize(screen.width(),screen.height());

   def getBlocksByName(self,genusName):
      if(genusName in self.block_list):
         return self.block_list[genusName]
      else:
         return []

   def getPages(self):
      return self.pages

   def getBlocks(self):
      blocks = []
      for component in self.findChildren(RenderableBlock) :
         blocks.append(component)

      return blocks

      allPageBlocks = []
      for p in self.pages:
         allPageBlocks += p.getBlocks();

      #print(allPageBlocks)
      return allPageBlocks;

   def reset(self):
 
      for block in self.getBlocks():
         block.setParent(None)

      pass
      #this.pageJComponent.removeAll();
      #Page.zoom = 1.0;


   #def getBlocks(self):
   #   blocks = self.findChildren(RenderableBlock)
   #   return blocks;

   def blockDropped(self,block):
      #print("blockcanvas blockDropped")
      # add to view at the correct location
      oldParent = block.parentWidget();
      old_pos = oldParent.mapToGlobal(block.pos())

      block.setParent(self.canvas)
      #self.blocks.append(block)

      new_pos  = self.mapFromGlobal(old_pos)

      #print(self.horizontalScrollBar().value())
      block.move(new_pos.x()+self.horizontalScrollBar().value(),new_pos.y()+self.verticalScrollBar().value());
      block.show()
      w = self.width()

      width = max(new_pos.x()+self.horizontalScrollBar().value()+50,self.canvas.width())
      height = max(new_pos.y()+self.verticalScrollBar().value()+50,self.canvas.height())

      self.canvas.resize(width,height)
      #self.parent().resizeEvent(None)
      #print("width:" + str(width) + " height:"+str(height))

      #self.resize(,
      #           )

      #block.setLocation(SwingUtilities.convertPoint(oldParent,
      #       block.getLocation(), this.pageJComponent));
      #self.addBlock(block);
      #this.pageJComponent.setComponentZOrder(block, 0);
      #this.pageJComponent.revalidate();

   '''
   def blockDropped(self, block):
      # add to view at the correct location
      oldParent = block.parent();
      #block.setLocation(SwingUtilities.convertPoint(oldParent,
      #		block.getLocation(), this.pageJComponent));
      self.addBlock(block);
      #this.pageJComponent.setComponentZOrder(block, 0);
      #this.pageJComponent.revalidate();
   '''
   def addBlock(self,block):
      # update parent widget if dropped block
      oldParent = block.parent();
      if(oldParent != self):
         if (oldParent != None):
            oldParent.removeBlock(block);
            if (block.hasComment()):
               block.getComment().getParent().remove(block.getComment());

         block.setParent(self);
         #if (block.hasComment()):
         #   block.getComment().setParent(block.parent().getJComponent());


      #self.getRBParent().addToBlockLayer(block);
      #block.setHighlightParent(this.getRBParent());

      # if block has page labels enabled, in other words, if it can, then set page label to this
      #if(Block.getBlock(block.getBlockID()).isPageLabelSetByPage()):
      #   Block.getBlock(block.getBlockID()).setPageLabel(this.getPageName());

      # notify block to link default args if it has any
      block.linkDefArgs();

      # fire to workspace that block was added to canvas if oldParent != this
      if(oldParent != self):
         pass
         #Workspace.getInstance().notifyListeners(WorkspaceEvent(oldParent, block.getBlockID(), WorkspaceEvent.BLOCK_MOVED));
         #Workspace.getInstance().notifyListeners(WorkspaceEvent(this, block.getBlockID(), WorkspaceEvent.BLOCK_ADDED, true));


      # if the block is off the edge, shift everything or grow as needed to fully show it
      #self.reformBlockPosition(block);

   	#self.pageJComponent.setComponentZOrder(block, 0);
   	# this.pageJComponent.revalidate();

   def hasPageAt(self, position):
      return (position >= 0 and position < len(self.pages));

   def numOfPages(self):
     return len(self.pages);

   def appendPage(self, page):
      self.insertPage(page,len(self.pages));
      self.pages.append(page);

   def setWidth(self, width):
      self.canvasWidth = width;

   def setHeight(self, height):
      self.canvasHeight = height;

   def getSaveNode(self, document):

      blocks = self.getBlocks();
      if (len(blocks) > 0):
         blocksElement = document.createElement("Blocks");
         for rb in blocks:
            blocksElement.appendChild(rb.getSaveNode(document));
         print(blocksElement)
         return blocksElement;
      else:
         return None

   def reformBlockCanvas(self):
      self.canvas.resize(self.canvasWidth,self.canvasHeight);
   	#scrollPane.revalidate();
      self.repaint();


      from Page import Page
      widthCounter = 0;
      for i in range(0, len(self.pages)):
         p = self.pages[i];
         if(p.getDefaultPageColor() == None):
            if (i % 2 == 1):
               p.setPageColor(QtGui.QColor(200,200,200,150));
            else:
               p.setPageColor(QtGui.QColor(180,180,180,150));

         else:
            p.setPageColor(p.getDefaultPageColor());
         p.repaint()
         widthCounter = widthCounter + p.reformBounds(widthCounter);

      for d in self.dividers:
         d.resize(
   				5,
   				d.getLeftPage().height());
         d.move(   				d.getLeftPage().x()+d.getLeftPage().width()-3,
   				0,)

      self.canvas.resize(widthCounter,(Page.DEFAULT_ABSTRACT_HEIGHT*Page.getZoomLevel()));
   	#scrollPane.revalidate();
      self.repaint();

   def mouseMoveEvent(self, event):
      #print(str(self)+":mouseMoveEvent")
      pass

   def insertPage(self,page, position):
      from PageDivider import PageDivider
      if(page == None):
         raise Exception("Invariant Violated: May not add null Pages");

      elif(position<0 or position > len(self.pages)):
         print(position+", "+pages.size());
         raise Exception("Invariant Violated: Specified position out of bounds");

      self.pages.insert(position, page);
      self.layout.addWidget(page)
      #page.parent = self.canvas
      #self.canvas.add(page, 0);
      pd = PageDivider(page);
      self.dividers.append(pd);
      self.layout.addWidget(pd)
      #canvas.add(pd,0);
      #PageChangeEventManager.notifyListeners();

   def loadBlocksFrom(self,blocksNode):
      blocks = blocksNode.getchildren();
      loadedBlocks = []

      for blockNode in blocks:
         rb = RenderableBlock.loadBlockNode(blockNode, self);
         rb.setParent(self.canvas)
         #rb.show()
         # save the loaded blocks to add later
         loadedBlocks.append(rb)
         
      #return loadedBlocks;
      for rb in loadedBlocks:  
         rb.redrawFromTop()
         rb.show()
      #loadedBlocks[0].redrawFromTop()

      return loadedBlocks;

   def loadSaveString(self,root):

      '''
      * Loads all the RenderableBlocks and their associated Blocks that
      * reside within the block canvas.  All blocks will have their nessary
      * data populated including connection information, stubs, etc.
      * Note: This method should only be called if this language only uses the
      * BlockCanvas to work with blocks and no pages. Otherwise, workspace live blocks
      * are loaded from Pages.
      * @param root the Document Element containing the desired information
      '''
      #from PageDrawerManager import PageDrawerManager
      # Extract canvas blocks and load

      blocksRoot = root.findall("Blocks");
      if(blocksRoot != None and len(blocksRoot) == 1):
         blocks = self.loadBlocksFrom(blocksRoot[0]);
      # load pages, page drawers, and their blocks from save file
      #PageDrawerManager.loadPagesAndDrawers(root);
      # PageDrawerLoadingUtils.loadPagesAndDrawers(root, WorkspaceController.workspace, WorkspaceController.workspace.factory);
      screen = QtGui.QDesktopWidget().availableGeometry()
      screenWidth = screen.width()
      canvasWidth = self.width();
      #if(canvasWidth<screenWidth):
      #   p = self.pages[len(self.pages)-1];
      #   p.addPixelWidth(screenWidth-canvasWidth);
      #   #PageChangeEventManager.notifyListeners();


   def blockEntered(self,block):
      pass
      #if (mouseIsInPage == false):
      #   mouseIsInPage = true;
      #   this.pageJComponent.repaint();
   def blockExited(self,block):
      pass

   def contains(self,point):
      return self.rect().contains(point)
     
