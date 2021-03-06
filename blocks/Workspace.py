
from PyQt4 import QtGui,QtCore
from blocks.PageDrawerLoadingUtils import PageDrawerLoadingUtils
from blocks.FactoryManager import FactoryManager
from blocks.BlockWorkspace import BlockWorkspace
from blocks.WorkspaceWidget import WorkspaceWidget

class Workspace(QtGui.QWidget,WorkspaceWidget):
    ws = None
    everyPageHasDrawer = False
    def __init__(self):
        super(QtGui.QWidget, self).__init__()
        Workspace.ws = self
        #QtGui.QFrame.__init__(self)

        self.setStyleSheet("background-color: rgba(0, 0, 0,0);")

        self.workspaceWidgets = []

        self.factory = FactoryManager(self,True, True)
        self.blockTab = QtGui.QTabWidget()      
        self.blockTab.setTabsClosable (True)
        self.connect(self.blockTab, QtCore.SIGNAL('tabCloseRequested(int)'), self.onCloseBlockCanvas)      

        layout  = QtGui.QHBoxLayout()
        self.setLayout(layout);
        self.layout().setContentsMargins(0, 0, 0, 0)

        splitter = QtGui.QSplitter(self)
        splitter.setContentsMargins(0, 0, 0, 0)

        splitter.addWidget(self.factory.getNavigator())
        splitter.addWidget(self.blockTab)

        splitter.setStretchFactor (1, 1 )
        layout.addWidget(splitter);


        self.addWidget(self.factory, True, False);
        self.setMouseTracking(True)
        
    def onCloseBlockCanvas(self,  index):
        if (index == -1) :
            return
        self.blockTab.removeTab(index); 
  
    def mouseMoveEvent(self, event):
        print(str(self)+":mouseMoveEvent")
        pass
    
    def getRenderableBlocksFromGenus(self,genusName):
        return self.blockCanvas.getBlocksByName(genusName);

    def getActiveCanvas(self):
        assert(isinstance(self.blockTab.currentWidget(), BlockWorkspace))
        return self.blockTab.currentWidget()

    def loadWorkspaceFrom(self, fileName):
        '''
        * Loads the workspace with the following content:
        * - RenderableBlocks and their associated Block instances that reside
        *   within the BlockCanvas
        * @param newRoot the XML Element containing the new desired content.  Some of the
        * content in newRoot may override the content in originalLangRoot.  (For now,
        * pages are automatically overwritten.  In the future, will allow drawers
        * to be optionally overriden or new drawers to be inserted.)
        * @param originalLangRoot the original language/workspace specification content
        * @requires originalLangRoot != null
        '''
        blockWorkspace = BlockWorkspace() 
        self.blockTab.addTab(blockWorkspace, fileName)
        self.blockTab.setCurrentWidget(blockWorkspace) 

        # load pages, page drawers, and their blocks from save file
        blockWorkspace.loadSaveString(fileName);
        PageDrawerLoadingUtils.loadBlockDrawerSets("", self.factory);

    def loadFreshWorkspace(self):
        blockWorkspace = BlockWorkspace() 
        self.blockTab.addTab(blockWorkspace, 'Untitled')
        self.blockTab.setCurrentWidget(blockWorkspace)         
        PageDrawerLoadingUtils.loadBlockDrawerSets("support\\block_drawersets.jason", self.factory);

    def addWidget(self,widget, addGraphically, floatOverCanvas):
        '''
        * Adds the specified widget to this Workspace
        * @param widget the desired widget to add
        * @param floatOverCanvas if true, the Workspace will add and render this widget such that it "floats"
        * above the canvas and its set of blocks.  If false, the widget will be laid out beside the canvas.  This feature
        * only applies if the specified widget is added graphically to the workspace (addGraphically = true)
        * @param addGraphically  a Swing dependent parameter to tell the Workspace whether or not to add
        * the specified widget as a child component.  This parameter should be false for widgets that have a
        * parent already specified
        '''
        if(addGraphically):
            if(floatOverCanvas):
                widget.raise_()
                pass
            else:
                pass
        self.workspaceWidgets.append(widget)

    def reset(self):
      '''
      * Clears the Workspace of:
      * - all the live blocks in the BlockCanvas.
      * - all the pages on the BlockCanvas
      * - all its BlockDrawers and the RB's that reside within them
      * - clears all the BlockDrawer bars of its drawer references and
      *   their associated buttons
      * - clears all RenderableBlock instances (which clears their associated
      *   Block instances.)
      * Note: we want to get rid of all RendereableBlocks and their
      * references.
      *
      * Want to get the Workspace ready to load another workspace
      '''
      from blocks.Block import Block
      from blocks.RenderableBlock import RenderableBlock
      from blocks.FactoryRenderableBlock import FactoryRenderableBlock

      #print("reset")
      # we can't iterate and remove widgets at the same time so
      # we remove widgets after we've collected all the widgets we want to remove
      # TreeSet.remove() doesn't always work on the TreeSet, so instead,
      # we clear and re-add the widgets we want to keep

      '''
      widgetsToRemove = []
      widgetsToKeep = []
      for  w in self.workspaceWidgets:
         #if isinstance(w, BlockCanvas):
         #   widgetsToRemove.append(w);
         #else:
         widgetsToKeep.append(w);

      self.workspaceWidgets[:]= []
      self.workspaceWidgets += widgetsToKeep
      self.workspaceWidgets.append(self.factory);

      # We now reset the widgets we removed.
      # Doing this for each one gets costly.
      # Do not do this for Pages because on repaint,
      # the Page tries to access its parent.
      for w in widgetsToRemove:
         parent = w.parent()
         if isinstance(w, BlockCanvas):
             w.reset();

         if (parent != None):
            w.setParent(None)
            #parent.validate();
            parent.repaint();
      '''

      #self.blockCanvas.reset();

      id_list = []
      Block.NEXT_ID = 0

      for blockID in RenderableBlock.ALL_RENDERABLE_BLOCKS:
         block = RenderableBlock.ALL_RENDERABLE_BLOCKS[blockID]
         if(not isinstance(block,FactoryRenderableBlock)):
            id_list.append(blockID)

      for id in id_list:
         block = RenderableBlock.ALL_RENDERABLE_BLOCKS[id]
         block.setParent(None)
         del RenderableBlock.ALL_RENDERABLE_BLOCKS[id]
         del Block.ALL_BLOCKS[id]
         del(block)

      # We now reset, the blockcanvas, the factory, and the renderableblocks

      #self.addPageAt(Page.getBlankPage(self), 0, False); # TODO: System expects PAGE_ADDED event
      #self.factory.reset();
      #Block.ALL_BLOCKS.clear()
      #Block.NEXT_ID = 1
      #env.resetAll();

      #revalidate();

    def getMiniMap(self):
        return self.miniMap;

    def getWidgetAt(self,point):
      '''
      * Returns the WorkspaceWidget currently at the specified point
      * @param point the <code>Point2D</code> to get the widget at, given
      *   in Workspace (i.e. window) coordinates
      * @return the WorkspaceWidget currently at the specified point
      '''
      # TODO: HUGE HACK, get rid of this. bascally, the facotry has priority
      #topWidget = QtGui.QApplication.topLevelAt(self.factory.canvas.mapFromGlobal(point));

      #return topWidget
      pos = self.factory.canvas.mapFromGlobal(point)
      if(self.factory.canvas.isVisible() and self.factory.canvas.rect().contains(pos)):
         return self.factory

      for widget in self.workspaceWidgets:
         #print(widget)
         pos = widget.mapFromGlobal(point)
         if (widget.isVisible() and widget.contains(pos)):
            #print(widget)
            return widget; # because these are sorted by draw depth, the first hit is on top

      return None; # hopefully we never get here

    def getWorkspaceInfo(self):
        return self.getActiveCanvas().getBlockWorkspaceInfo();

    def resizeEvent(self, event):
        #self.trash.rePosition()
        #self.miniMap.repositionMiniMap();

        self.factory.onResize(event)

      
    def mousePressEvent(self, event):
        self.factory.ResetButtons()



    def getTopBlocks(self, ordered=False):
        '''
        * Finds the top-level blocks and returns them.  Blocks are optionally sorted
        * by position; top to bottom (with slight LTR or RTL bias).
        * @param {boolean} ordered Sort the list if true.
        * @return {!Array.<!Blockly.Block>} The top-level block objects.
        '''
        from blocks.BlockLinkChecker import BlockLinkChecker
        blocks = []
        # Copy the topBlocks_ list.
        all_blocks = self.getActiveCanvas().getBlocks()
        #print(all_blocks)
        for rb in all_blocks:
          block = rb.getBlock()
          #print(block.before)
          
          #if block.before == None:
          #  blocks.append(block)      
          plug = BlockLinkChecker.getPlugEquivalent(block)
          if(plug == None or not plug.hasBlock()):
            blocks.append(block)

        if (ordered and len(blocks) > 1):
          #offset = math.sin(math.toRadians(Blockly.Workspace.SCAN_ANGLE));
          if (self.RTL):
            #offset *= -1;
            pass
          '''
          blocks.sort(function(a, b) {
            var aXY = a.getRelativeToSurfaceXY();
            var bXY = b.getRelativeToSurfaceXY();
            return (aXY.y + offset * aXY.x) - (bXY.y + offset * bXY.x);
          });
          '''
        return blocks;

    def getTopRBs(self, ordered=False):
        from blocks.BlockLinkChecker import BlockLinkChecker
        blocks = []
        # Copy the topBlocks_ list.
        all_blocks = self.blockCanvas.getBlocks()
        #print(all_blocks)
        for rb in all_blocks:
          block = rb.getBlock()    
          plug = BlockLinkChecker.getPlugEquivalent(block)
          if(plug == None or not plug.hasBlock()):
            blocks.append(rb)

        return blocks;
 
        
