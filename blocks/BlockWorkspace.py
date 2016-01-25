
from PyQt4 import QtGui,QtCore
from blocks.RenderableBlock import RenderableBlock
from blocks.WorkspaceWidget import WorkspaceWidget
from blocks.TrashCan import TrashCan
from blocks.MiniMap import MiniMap

class Canvas(QtGui.QWidget,WorkspaceWidget):
    def __init__(self, blockWorkspace):
        QtGui.QWidget.__init__(self)
        self.blockWorkspace = blockWorkspace
        self.focusBlock = None
        self.setMouseTracking(True);
        self.family = {}
        pass
    
    def getBlocks(self):
        blocks = []
        for component in self.findChildren(RenderableBlock) :
            blocks.append(component)
        
        # reversed this list to make top most at begining
        return reversed(blocks)        

    def initNewRB(self, rb):
        self.focusBlock = rb      

    def getUnderRB(self, globalPos):
        for rb in self.getBlocks():
            pos = rb.mapFromGlobal( globalPos);
            if rb.blockArea.contains(pos): 
                return rb
        return None 

    def mouseMoveEvent(self, event):        
        if( self.blockWorkspace.focusedBlock != None and not self.blockWorkspace.focusedBlock.pickedUp):  
            self.blockWorkspace.focusedBlock.onMouseLeave()            
            self.blockWorkspace.focusedBlock = None
 
                
    def contains(self,pos):
        return self.rect().contains(pos)

    def blockDropped(self,block):
        self.blockWorkspace.blockDropped(block)

class BlockWorkspace(QtGui.QScrollArea, WorkspaceWidget):

    def __init__(self):
        from blocks.Workspace import Workspace
        QtGui.QScrollArea.__init__(self)
        
        self.workspaceWidgets = []
        
        self.ws = Workspace.ws
        self.canvas = Canvas(self);
        self._focusedBlock = None

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(False)
        self.setWidget(self.canvas)

        #Scroll Area Layer add
        #self.layout = QtGui.QHBoxLayout(self)
        #self.canvas.setLayout(self.layout)

        self.setStyleSheet("background-color: rgba(225, 225, 225,0);")
        self.pages = []
        self.dividers = []
        self.block_list = {}

        screen = QtGui.QDesktopWidget().availableGeometry()
        self.canvas.resize(screen.width(),screen.height());
        
        self.createTrashCan()
        self.miniMap = MiniMap(self);
        self.workspaceWidgets.append(self.miniMap)        
        self.workspaceWidgets.append(self.trash)
        self.workspaceWidgets.append(self.canvas)
        
    @property
    def focusedBlock(self):
        return self._focusedBlock

    @focusedBlock.setter
    def focusedBlock(self, value):
        self._focusedBlock = value
    
    def getCanvas(self):
        return self.canvas
    
    def getWidgetAt(self,point):
      pos = self.ws.factory.getNavigator().mapFromGlobal(point)

      if(self.ws.factory.getNavigator().rect().contains(pos)):
         return self.ws.factory

      for widget in self.workspaceWidgets:
         pos = widget.mapFromGlobal(point)
         if (widget.isVisible() and widget.contains(pos)):
            return widget

      return None; # hopefully we never get here

      
    def createTrashCan(self):
        #add trashcan and prepare trashcan images
        tc = QtGui.QIcon ("support/images/trash.png")
        openedtc = QtGui.QIcon("support/images/trash_open.png");
        sizes = tc.availableSizes();
        maximum = sizes[0].width();
        for i in range(1,len(sizes)):
            maximum = QtGui.qMax(maximum, sizes[i].width());
        self.trash = TrashCan(self,
            tc.pixmap(QtCore.QSize(maximum, maximum)),
            openedtc.pixmap(QtCore.QSize(maximum, maximum))
            );
        self.trash.lower()
        #self.trash.setParent(self.blockCanvas)

        
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


    def reset(self): 
        for block in self.getBlocks():
            block.setParent(None)

    def blockDropped(self,block):
        #print('blockDropped')
        oldParent = block.parentWidget();
        old_pos = oldParent.mapToGlobal(block.pos())

        block.setParent(self.canvas)
        #block.initFinished = True
        new_pos  = self.mapFromGlobal(old_pos)

        block.move(
            new_pos.x()+self.horizontalScrollBar().value()-1,
            new_pos.y()+self.verticalScrollBar().value()-1);
        block.show()

        width = max(new_pos.x()+self.horizontalScrollBar().value()+50,self.canvas.width())
        height = max(new_pos.y()+self.verticalScrollBar().value()+50,self.canvas.height())

        self.canvas.resize(width,height)

        #block.setMouseTracking(True);
        #block.installEventFilter(self.canvas); 
 
    def addBlock(self,block):
      # update parent widget if dropped block
      oldParent = block.parent();
      if(oldParent != self):
         if (oldParent != None):
            oldParent.removeBlock(block);
            if (block.hasComment()):
               block.getComment().getParent().remove(block.getComment());

         block.setParent(self);

      block.linkDefArgs();

      # fire to workspace that block was added to canvas if oldParent != this
      if(oldParent != self):
         pass

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

    def getBlockWorkspaceInfo(self):

        workspace_info = {}

        blocks = self.getBlocks();
        if (len(blocks) > 0):
            rb_list = []
            for rb in blocks:
                rb_list.append(rb.getRenderableBlockInfo());
            
            workspace_info['rb_list'] = rb_list

        return workspace_info

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
         d.resize(5, d.getLeftPage().height());
         d.move(d.getLeftPage().x()+d.getLeftPage().width()-3,  0,)

      self.canvas.resize(widthCounter,(Page.DEFAULT_ABSTRACT_HEIGHT*Page.getZoomLevel()));
      #scrollPane.revalidate();
      self.repaint();
      
    def mouseMoveEvent(self, event):
        #print(str(self)+":mouseMoveEvent")
        #self.canvas.mouseMoveEvent(event)
        pass

    def insertPage(self,page, position):
        from PageDivider import PageDivider
        if(page == None):
            raise Exception("Invariant Violated: May not add null Pages");

        elif(position<0 or position > len(self.pages)):
            raise Exception("Invariant Violated: Specified position out of bounds");

        self.pages.insert(position, page);
        self.layout.addWidget(page)

        pd = PageDivider(page);
        self.dividers.append(pd);
        self.layout.addWidget(pd)


    def loadBlocksFrom(self,blockWorkspaceInfo):
          
        loadedBlocks = []      
        if('rb_list' in blockWorkspaceInfo):
            rb_info_list = blockWorkspaceInfo['rb_list']
            for rb_info in rb_info_list:
                rb = RenderableBlock.loadBlockNode(rb_info, self);
                rb.setParent(self.canvas)
                self.blockDropped(rb)
             
                loadedBlocks.append(rb)
             
            for rb in loadedBlocks:  
                rb.reformBlockShape()
                rb.show()

            for rb in self.getTopLevelBlocks():  
                rb.redrawFromTop()

        return loadedBlocks

    def getTopLevelBlocks(self):
        topBlocks = []
        for renderable in self.getBlocks():
            block = renderable.getBlock()
            if (block.getPlug() == None or 
                block.getPlugBlockID() == None or 
                block.getPlugBlockID()  == ""):
            
                if (block.getBeforeConnector() == None or 
                    block.getBeforeBlockID() == None or 
                    block.getBeforeBlockID() == ""):
                    topBlocks.append(renderable);

        return topBlocks

    def loadSaveString(self,path):
        import json
        f=open(path)
        blockWorkspaceInfo = json.load(f)
        self.loadBlocksFrom(blockWorkspaceInfo);

    def blockEntered(self,block):
        pass

    def blockExited(self,block):
        pass

    def contains(self,point):
        return self.rect().contains(point)     
  
    def resizeEvent(self, event):
        self.trash.rePosition()
        self.miniMap.repositionMiniMap();
