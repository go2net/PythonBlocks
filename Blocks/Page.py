#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      shijq
#
# Created:     22/04/2015
# Copyright:   (c) shijq 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PyQt4 import QtGui, uic,QtCore
from WorkspaceWidget import WorkspaceWidget

'''
 * This class serves as the zoomable JComponent and RBParent of the page
 * that wraps it.
'''
class PageWidget(QtGui.QWidget):
   def __init__(self):
      QtGui.QWidget.__init__(self)
      self.setAutoFillBackground(True)
      self.BLOCK_LAYER = 1;
      self.HIGHLIGHT_LAYER = 0;
      self.IMAGE_WIDTH = 60;
      self.image = None;
      self.fullview = True;
      self.backcolor = QtGui.QColor(255,255,255)

   def setFullView(self,isFullView):
      self.fullview = isFullView;

   def setImage(self, image):
      self.image=image;

   def getImage(self):
      return image;

   def setBackground(self,newColor):
      self.backcolor = newColor

   def getBackground(self):
      return self.backcolor

   '''
    * renders this JComponent
   '''
   def paintEvent(self,event):
      QtGui.QWidget.paintEvent(self,event);
      painter = QtGui.QPainter(self);
      w = self.width()
		# paint page
      #self.setStyleSheet("background-color: rgba(225, 168, 0,255);")
		# set label color
      palette = self.palette ()
      palette.setColor(self.backgroundRole(), self.backcolor);
      #backcolor = palette.color(QtGui.QPalette.Background)
      if (self.backcolor.blue() + self.backcolor.green() + self.backcolor.red() > 400):
         palette.setColor(self.foregroundRole(), QtGui.QColor(0,0,0));
      else:
         palette.setColor(self.foregroundRole(), QtGui.QColor(0,0,0));

      self.setPalette(palette);
      self.setAutoFillBackground(True)
		# paint label at correct position
      if(self.fullview):
         xpos = self.width()*0.5 #-g.getFontMetrics().getStringBounds(this.getName(), g).getCenterX());
         painter.drawText(xpos, self.height()/2,self.objectName());
         painter.drawText(xpos, self.height()/2,self.objectName())
         painter.drawText(xpos, self.height()*3/4,self.objectName())

         '''
         g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER,0.33F));
         int imageX = (int)(this.getWidth()/2-IMAGE_WIDTH/2*Page.zoom);
         int imageWidth = (int)(IMAGE_WIDTH*Page.zoom);
         g.drawImage(this.getImage(), imageX, getHeight()/2+5,imageWidth,imageWidth,null);
         g.drawImage(this.getImage(), imageX, getHeight()/4+5,imageWidth,imageWidth,null);
         g.drawImage(this.getImage(), imageX, getHeight()*3/4+5,imageWidth,imageWidth,null);
         g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER,1));

         '''



class Page(PageWidget,WorkspaceWidget):
   #  Width while in collapsed mode
   COLLAPSED_WIDTH = 20;
   #  The smallest value that this.minimumPixelWidth/zoom can be
   DEFAULT_MINUMUM_WIDTH = 100;
   #  The default abstract width
   DEFAULT_ABSTRACT_WIDTH = 700;
   #  The default abstract height
   DEFAULT_ABSTRACT_HEIGHT = 1600;
   #  an equals sign followed by a double quote character
   EQ_OPEN_QUOTE = "=\"";
   #  a double quote character
   CLOSE_QUOTE ="\" ";
   #  An empty string
   emptyString = "";

   zoom = 1.0

   def __init__(self,name, pageWidth, pageHeight, pageDrawer, inFullview, defaultColor):
      PageWidget.__init__(self)
      #self.setStyleSheet("background-color: rgba(225, 168, 0,255);")
      #  this.zoomLevel: zoom level state */
      #self.zoom = 1.0;
      #  The JComponent of this page */
      # self.pageJComponent = QtGui.QFrame();
      #  The abstract width of this page */
      # self.abstractWidth;
      #  The abstract height of this page */
      # self.abstractHeight;
      #  The name of the drawer that this page refers to */
      # self.pageDrawer;
      #  The default page color.  OVERRIDED BY BLOCK CANVAS */
      # self.defaultColor;
      #  MouseIn Flag: true if and only if the mouse is in this page */
      self.mouseIsInPage = False;
      #  The minimum width of the page in pixels */
      self.minimumPixelWidth = 0;
      #  Fullview */
      # self.fullview;
      #  The GUI component for interfacing with the user
      #  to help the user collapse or restore the page */
      # self.collapse;
      #  The user-time unique id of this page. Once set, cannot be changed. */
      self.pageId = None;
      #  Toggles to show/hide minimize page button. */
      self.hideMinimize = False;


      self.defaultColor = defaultColor;
      #self.pageJComponent.setLayout(None);
      self.setObjectName(name);
      self.abstractWidth = pageWidth if pageWidth > 0 else Page.DEFAULT_ABSTRACT_WIDTH;
      self.abstractHeight = Page.DEFAULT_ABSTRACT_HEIGHT;
      if(pageDrawer != None):
         self.pageDrawer = pageDrawer;
      elif(Workspace.everyPageHasDrawer):
         self.pageDrawer = name;

      #self.pageJComponent.setOpaque(True);

      self.fullview = inFullview;
      #self.collapse = CollapseButton(inFullview, name);
      #self.pageJComponent.add(collapse);
      #self.setFullView(inFullview);
      #self.resize(400,self.height())

   def loadPageFrom(self, pageNode, importingPage):
      return
      # note: this code is duplicated in BlockCanvas.loadSaveString().
      pageChildren = pageNode.childNodes;
      loadedBlocks = []
      idMapping = {} if importingPage else None;
      if (importingPage):
         reset();
      for i in range(0, len(pageChildren)):
         pageChild = pageChildren.item(i);
         if(pageChild.NodeName() == ("PageBlocks")):
            blocks = pageChild.getChildNodes();
            for j in range(0, len(blocks)):
               blockNode = blocks.item(j);
               rb = RenderableBlock.loadBlockNode(blockNode, this, idMapping);
   				# save the loaded blocks to add later
               loadedBlocks.add(rb);
            break;  # should only have one set of page blocks

      return loadedBlocks;

   def getBlocks(self):
      from RenderableBlock import RenderableBlock
      blocks = self.findChildren(RenderableBlock)
      #print(blocks)
      return blocks;


   def getTopLevelBlocks(self):
      topBlocks = []
      for renderable in self.getBlocks():
         block = Block.getBlock(renderable.getBlockID());
         if(block.getPlug() == None or block.getPlugBlockID() == None or block.getPlugBlockID() ==Block.NULL):
            if(block.getBeforeConnector() == None or block.getBeforeBlockID() == None or block.getBeforeBlockID() == Block.NULL):
               topBlocks.append(renderable);
               continue;

      return topBlocks;

   def addLoadedBlocks(self,loadedBlocks, importingPage):
      for rb in loadedBlocks:
         if(rb != None):
            # add graphically
            getRBParent().addToBlockLayer(rb);
            rb.setHighlightParent(this.getRBParent());
   			#System.out.println("loading rb to canvas: "+rb+" at: "+rb.getBounds());
   			#add internallly
            Workspace.getInstance().notifyListeners(WorkspaceEvent(this, rb.getBlockID(), WorkspaceEvent.BLOCK_ADDED));
            if (importingPage):
               Block.getBlock(rb.getBlockID()).setFocus(false);
               rb.resetHighlight();
               rb.clearBufferedImage();



   	#now we need to redraw all the blocks now that all renderable blocks
   	#within this page have been loaded, to update the socket dimensions of
   	#blocks, etc.
      for rb in self.getTopLevelBlocks():
         rb.redrawFromTop();
         if (rb.isCollapsed()):
            # This insures that blocks connected to a collapsed top level block
            # are located properly and have the proper visibility set.
            # This doesn't work until all blocks are loaded and dimensions are set.
            rb.updateCollapse();

      #self.revalidate();
      #self.repaint();

   def setZoomLevel(newZoom):
      Page.zoom = newZoom;

   def getZoomLevel():
      return Page.zoom;


   '''
	 * Sets the page id. Consider the page id "final" but settable - once
	 * set, it cannot be modified or unset.
   '''
   def setPageId(self, id):
      if (self.pageId == None):
         pageId = id;
      else:
         throw("Tried to set pageId again: " + this);

   def getPageDrawer(self):
      return self.pageDrawer;


   def addPixelWidth(self, deltaPixelWidth):
      '''
      * @param deltaPixelWidth
      *
      * @requires Integer.MIN_VAL <= deltaPixelWidth <= Integer.MAX_VAL
      * @modifies this.width
      * @effects Adds deltaPixelWidth to the abstract width taking into
      * 			account the zoom level.  May need to convert form pixel to abstract model.
      '''
      if (self.fullview):
         self.setPixelWidth(self.getAbstractWidth() * self.zoom + deltaPixelWidth);


   def getAbstractWidth(self):
      return self.abstractWidth;

   def contains(self,point):
      return self.rect().contains(point)

   def getAbstractHeight(self):
      return self.abstractHeight;

   def getDefaultPageColor(self):
      return self.defaultColor;

   def getPageColor(self):
      return self.getBackground();

   def setPageColor(self, newColor):
      self.setBackground(newColor);


   def setPixelWidth(self, pixelWidth):
      '''
      * @requires Integer.MIN_VAL <= pixelWidth <= Integer.MAX_VAL
      * @modifies this.width
      * @effects sets abstract width to pixelWidth taking into account the zoom level.
      * 			May need to convert form pixel to abstract model.

      '''
      if (pixelWidth < self.minimumPixelWidth):
         self.abstractWidth = self.minimumPixelWidth / self.zoom;
      else:
         self.abstractWidth = pixelWidth / self.zoom;

   '''
   * Called by RenderableBlocks that get "dropped" onto this Widget
   * @param block the RenderableBlock that is "dropped" onto this Widget
   '''
   def blockDropped(self,block):
      print("page blockDropped")
      # add to view at the correct location
      oldParent = block.parentWidget();
      old_pos = oldParent.mapToGlobal(block.pos())

      block.setParent(self)
      new_pos  = self.mapFromGlobal(old_pos)

      block.move(new_pos.x(),new_pos.y());
      block.show()
      w = self.width()
      #block.setLocation(SwingUtilities.convertPoint(oldParent,
      #       block.getLocation(), this.pageJComponent));
      self.addBlock(block);
      #this.pageJComponent.setComponentZOrder(block, 0);
      #this.pageJComponent.revalidate();
   '''
   * Called by RenderableBlocks as they are dragged over this Widget.
   * @param block the RenderableBlock being dragged
   '''
   def blockDragged(self,block):
      pass

   '''
   * Called when a RenderableBlock is being dragged and goes from being
   * outside this Widget to being inside the Widget.
   * @param block the RenderableBlock being dragged
   '''
   def blockEntered(self,block):
      pass

   '''
   * Called when a RenderableBlock that was being dragged over this Widget
   * goes from being inside this Widget to being outside the Widget.
   * @param block the RenderableBlock being dragged
   '''
   def blockExited(self,block):
      pass

   '''
   * Used by RenderableBlocks to tell their originating Widgets that
   * they're moving somewhere else and so should be removed.
   * @param block the RenderableBlock
   '''
   def removeBlock(self,block):
      pass

   '''
   * Adds the specified block to this widget interally and graphically.  The
   * difference between this method and blockDropped is that blockDropped is
   * activated by user actions, such as mouse drag and drop or typeblocking.
   * Use this method only for single blocks, as it may cause repainting!  For
   * adding several blocks at once use addBlocks, which delays graphical updates
   * until after the blocks have all been added.
   * @param block the desired RenderableBlock to add to this
   '''
   def addBlock(self,block):  #TODO ria maybe rename this to putBlock?
      # update parent widget if dropped block
      oldParent = block.parent();
      if(oldParent != self):
         if (oldParent != None):
            oldParent.removeBlock(block);
            if (block.hasComment()):
               block.getComment().getParent().remove(block.getComment());

         block.setWorkspaceWidget(self);
         #if (block.hasComment()):
         #   block.getComment().setParent(block.parent().getJComponent());


      block.setParent(self)
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
      self.reformBlockPosition(block);

   	#self.pageJComponent.setComponentZOrder(block, 0);
   	# this.pageJComponent.revalidate();


   def reformBlockPosition(self, block):
      # move blocks in
      p = block.mapTo(self,block.pos());
      if(p.x()<block.getHighlightStrokeWidth() / 2 + 1):
         block.move(block.getHighlightStrokeWidth() / 2 + 1, p.y());
         block.moveConnectedBlocks();
         # the block has moved, so update p
         p = block.mapTo(self,block.pos());
      elif(p.x()+block.width()+block.getHighlightStrokeWidth()/2+1>self.width()):
         self.setPixelWidth(p.x()+block.width()+ block.getHighlightStrokeWidth() / 2 + 1);


      if(p.y()<block.getHighlightStrokeWidth() / 2 + 1):
         block.move(p.x(), block.getHighlightStrokeWidth() / 2 + 1);
         block.moveConnectedBlocks();
      elif(p.y()+block.getStackBounds().height()+block.getHighlightStrokeWidth() / 2 + 1>self.height()):
         block.move(p.x(), self.height()-block.getStackBounds().height()- block.getHighlightStrokeWidth() / 2 + 1);
         block.moveConnectedBlocks();

      if (block.hasComment()):
         # p = SwingUtilities.convertPoint(block.getComment().getParent(), block.getComment().getLocation(), this.pageJComponent);
         p = block.getComment().getLocation();
         if (p.x() + block.getComment().width() + 1 > self.width()):
            self.setPixelWidth(p.x() + block.getComment().width() + 1);


      # repaint all pages
   	# PageChangeEventManager.notifyListeners();

   def mouseMoveEvent(self, event):
      print(str(self)+":mouseMoveEvent")

   '''
   * Adds a collection of blocks to this widget internally and graphically.
   * This method adds blocks internally first, and only updates graphically
   * once all of the blocks have been added.  It is therefore preferable to
   * use this method rather than addBlock whenever multiple blocks will be added.
   * @param blocks the Collection of RenderableBlocks to add
   '''
   def addBlocks(self,blocks):
      pass

   def reformBounds(self, pixelXCor):
      if (self.fullview):
         self.resize(self.abstractWidth * self.zoom,  self.abstractHeight * self.zoom);
         w = self.width()
         self.move(pixelXCor,0)
         #self.repaint()
         #this.getJComponent().setFont(new Font("Ariel", Font.PLAIN, (int) (12 * self.zoom)));
         return self.abstractWidth * self.zoom
      else:
         self.resize(self.COLLAPSED_WIDTH + 2,self.abstractHeight * self.zoom);
         self.move(pixelXCor,0)
         #this.getJComponent().setFont(new Font("Ariel", Font.PLAIN, (int) (12 * zoom)));
         return COLLAPSED_WIDTH + 2;
