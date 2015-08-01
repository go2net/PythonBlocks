
from PyQt4 import QtGui,QtCore
from blocks.RenderableBlock import RenderableBlock
from blocks.WorkspaceWidget import WorkspaceWidget

class Canvas(QtGui.QWidget,WorkspaceWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.focusBlock = None
        self.setMouseTracking(True);
        pass
    
    def getBlocks(self):
        blocks = []
        for component in self.findChildren(RenderableBlock) :
            blocks.append(component)

        return blocks        

    def eventFilter(self, source, event):   
        if event.type() == QtCore.QEvent.MouseMove:      
            globalPos = event.globalPos()
            #print(globalPos)
            if(self.focusBlock != None):
                pos = self.focusBlock.mapFromGlobal( globalPos);
                if not self.focusBlock.blockArea.contains(pos):
                    self.focusBlock.onMouseLeave()
                        
            #if event.buttons() == QtCore.Qt.NoButton:                    
            for rb in self.getBlocks():
                pos = rb.mapFromGlobal( globalPos);
                if rb.blockArea.contains(pos):
                    rb.onMouseEnter()
                    self.focusBlock = rb
                    break  

        return QtGui.QMainWindow.eventFilter(self, source, event)


    def mouseMoveEvent(self, event):
        globalPos = event.globalPos()

        #print(globalPos)
        if(self.focusBlock != None):
            pos = self.focusBlock.mapFromGlobal( globalPos);
            if not self.focusBlock.blockArea.contains(pos):
                self.focusBlock.onMouseLeave()


class BlockCanvas(QtGui.QScrollArea):

   def __init__(self):
      QtGui.QScrollArea.__init__(self)
      
      self.canvas = Canvas();
      
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

   def blockDropped(self,block):

      oldParent = block.parentWidget();
      old_pos = oldParent.mapToGlobal(block.pos())

      block.setParent(self.canvas)

      new_pos  = self.mapFromGlobal(old_pos)

      block.move(new_pos.x()+self.horizontalScrollBar().value(),new_pos.y()+self.verticalScrollBar().value());
      block.show()

      width = max(new_pos.x()+self.horizontalScrollBar().value()+50,self.canvas.width())
      height = max(new_pos.y()+self.verticalScrollBar().value()+50,self.canvas.height())

      self.canvas.resize(width,height)
      
      block.setMouseTracking(True);
      block.installEventFilter(self.canvas); 
 
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

   def getSaveNode(self, document):

      blocks = self.getBlocks();
      if (len(blocks) > 0):
         blocksElement = document.createElement("Blocks");
         for rb in blocks:
            blocksElement.appendChild(rb.getSaveNode(document));
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
         d.resize(5, d.getLeftPage().height());
         d.move(d.getLeftPage().x()+d.getLeftPage().width()-3,  0,)

      self.canvas.resize(widthCounter,(Page.DEFAULT_ABSTRACT_HEIGHT*Page.getZoomLevel()));
      #scrollPane.revalidate();
      self.repaint();
      
   def mouseMoveEvent(self, event):
      print(str(self)+":mouseMoveEvent")
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


   def loadBlocksFrom(self,blocksNode):
      blocks = blocksNode.getchildren();
      loadedBlocks = []

      for blockNode in blocks:
         rb = RenderableBlock.loadBlockNode(blockNode, self);
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
              block.getPlugBlockID()  == -1):
            if (block.getBeforeConnector() == None or 
                block.getBeforeBlockID() == None or 
                block.getBeforeBlockID() == -1):
                  topBlocks.append(renderable);

      return topBlocks

   def loadSaveString(self,root):
      blocksRoot = root.findall("Blocks");
      if(blocksRoot != None and len(blocksRoot) == 1):
         self.loadBlocksFrom(blocksRoot[0]);

   def blockEntered(self,block):
      pass

   def blockExited(self,block):
      pass

   def contains(self,point):
      return self.rect().contains(point)     
