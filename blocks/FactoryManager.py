#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      A21059
#
# Created:     04/03/2015
# Copyright:   (c) A21059 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PyQt4 import QtGui
from blocks.Block import Block
from functools import partial
from blocks.FactoryCanvas import FactoryCanvas
from blocks.WorkspaceWidget import WorkspaceWidget
class FactoryManager(WorkspaceWidget):
   # The string identifier of static drawers
   STATIC_NAME = "Factory"
   # The string identifier of dynamic drawers */
   DYNAMIC_NAME = "My Blocks"
   # The string identifier of subset drawers */
   SUBSETS_NAME = "Subsets"

   def __init__(self,parent,hasStatic, hasDynamic):

      # The high-level UI that manages the controlling of internal CWsing components
      #navigator = Navigator()
      # The high-level UI widget that manages swicthing between different factories

      self.factorySwicther = None
      self.active_button = None
      self.parentWidget = parent
      self.active_canvas = None
      # the set os static drawers
      self.staticCanvases = []
      # The set of dynaic drawers
      self.dynamicCanvases = []
      # The set of subset drawers
      self.subsetCanvases = []

      # The UI used to navigate between explorers
      self.navigator = QtGui.QScrollArea()
      #self.navigator.setFixedWidth(160)
      self.navigator.setStyleSheet("background-color: #EEEEEE;")
      self.layout  = QtGui.QVBoxLayout()
      self.navigator.setLayout(self.layout )
      self.navigator.resizeEvent = self.onNavResize
      self.navigator.resize(150,self.navigator.height())
      # The UI used to navigate between explorers
      self.canvas = QtGui.QStackedWidget(parent)
      self.canvas.setStyleSheet("background-color: rgba(0, 0, 0,0);")
      self.canvas.setFrameShape(QtGui.QFrame.Box)
      self.canvas.hide()
      #self.canvas.setFixedWidth(150)
      #self.canvas.setStyleSheet("background-color: rgb(250, 170, 0);")

      #self.layout  = QtGui.QVBoxLayout()
      #self.scroll.setLayout(self.layout )
      #layout.addWidget(wc.getWorkspacePanel())

      #self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

      #self.parentWidget.resizeEvent = self.onResize

      pass

   def getparentWidget(self):
      return self.parentWidget



   def addStaticDrawerNoPos(self,name, color):
      '''
      Adds a static drawer if no drawer with the specified name already exists.
      If one alreaedy exist, then do ntohing.  If the name is null, do nothing
      @param name - name os drawer, may not be null
      @param color

      @requires name != null && drawer to not already exist in BOTH static and dynamic set

      '''
      return self.addStaticDrawer(name, len(self.staticCanvases), color)

   def addDynamicDrawer(self,name):
      self.addDynamicDrawerWithPos(name, len(self.dynamicCanvases));


   def addDynamicDrawerWithPos(self,name, position):
      if(self.isValidDrawer(False, True, name, position)):
         canvas = FactoryCanvas(self.canvas,name);
         self.dynamicCanvases.insert(position, canvas);
         #self.navigator.setCanvas(dynamicCanvases, DYNAMIC_NAME);
      else:
         print("Invalid Drawer: trying to add a drawer that already exists: "+name);


   def addStaticDrawer(self,name, position, color):
      '''
      * Adds a static drawer if no drawer with the specified name already exists.
      * If one alreaedy exist, then do ntohing.  If the name is null, do nothing
      * @param name - name os drawer, may not be null
      * @param color
      * @param position
      *
      * @requires name != null &&
      * 			 drawer to not already exist in BOTH static and dynamic set
      '''
      if(self.isValidDrawer(True, False, name, position)):
         canvas = FactoryCanvas(self.canvas,name, color)
         self.staticCanvases.insert(position, canvas)
         self.canvas.addWidget(canvas)
         self.setCanvas(self.staticCanvases, FactoryManager.STATIC_NAME)
         return canvas
      else:
         print("Invalid Drawer: trying to add a drawer that already exists: "+ name);
         return None


   def isValidDrawer(self,sta, dyn, name, position):
      '''
   	 * may not two draers with the same name
   	 * @param sta
   	 * @param dyn
   	 * @param name
   	 * @param position
   	 * @return true if and only if the following conditions are met:
   	 * 			-specified name is not null,
   	 * 			-if "sta" is true, then 0<=position<staticdrawers.size
   	 * 			-if "dyn" is true, then 0<=position<static drawers.size
   	 * 			-there is NO other drawers with the same name as the
   	 * 			 specified name (in oth static or dynamic sets)
      '''
      if(sta):
         if (position < 0): return False
         if (position > len(self.staticCanvases)): return False
         #for canvas in self.staticCanvases:
         #   if (canvas.getName() == name): return False


         if(dyn):
            if (position < 0): return False;
            if (position > len(self.dynamicCanvases)): return False
            for canvas in self.dynamicCanvases:
               if (canvas.getName() == name): return False

      return True



   def addStaticBlocks(self,blocks,drawer):
      '''
       * Add blocks to drawer if drawer can be found.  Add graphically
       * and alos throw event.  Do nothing if no drawer if specified
       * name is found.
       *
       * @param blocks
       * @param drawer
      '''
      # find canvas
      for canvas in self.staticCanvases:
         if (canvas.getName() == drawer):
            #canvas.addBlocks(blocks)
            for block in blocks:
               if(block == None or Block.NULL == block.blockID): continue
               canvas.addBlock(block)
                  #Workspace.getInstance().notifyListeners(new WorkspaceEvent(this, block.blockID, WorkspaceEvent.BLOCK_ADDED));


            canvas.layoutBlocks()
            return

      print("Drawer not found: "+drawer)
      return

   def getNavigator(self):
      '''
       * @return the JCOmponent representation of this.  MAY NOT BE NULL
      '''
      return self.navigator


   def setCanvas(self,canvases, explorer):
      '''
       * Reassigns the canvases to the explorer with the specified name.  If
       * no explorer is found to have that name, or if the name is null,
       * then do nothing.
       * @param canvases
       * @param explorer
       *
       * @requires canvases!= null
   '''
      for widget in self.navigator.findChildren(QtGui.QPushButton):
         widget.deleteLater()

      for index in range(0,self.canvas.count()):
         name = self.canvas.widget(index).getName()
         button = QtGui.QPushButton(name,self.navigator)
         #button.setFlat(True)
         button.clicked.connect(partial(self.OnPressed,sender=button))
         button.setStyleSheet('QPushButton {background-color: #EEEEEE; color: black;border=1}')
         #button.setFlat(True)
         #button.setMinimumWidth(self.navigator.width()-10)
         button.move(5,index*(button.height() + 5)+5)
         index += 1
         #self.layout.addWidget(button)

   def ResetButtons(self):
      self.canvas.hide()
      if(self.active_button != None):
         self.active_button.setStyleSheet('QPushButton {background-color: #EEEEEE; color: black;}')
      

   def OnPressed(self,sender):
      #print (sender.text()+" Pressed!")

      for index in range(0,self.canvas.count()):
         widget = self.canvas.widget(index)
         if(widget.getName() == sender.text()):
            self.canvas.setCurrentIndex(index)
            self.active_canvas = widget
            break

      if(self.canvas.isVisible()):
         self.canvas.hide()
         if(self.active_button != None):
            self.active_button.setStyleSheet('QPushButton {background-color: #EEEEEE; color: black;}')

         if(self.active_button != sender):
            sender.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
            self.canvas.show()

      else:
         sender.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
         self.canvas.show()

      self.active_button = sender
      self.canvas.raise_()
      self.canvas.move(self.navigator.width(),0)

      self.adjustSize()

   def adjustSize(self):
      if(self.active_canvas != None):
         width = self.active_canvas.getCanvasWidth()
         height = self.parentWidget.height()

         if(self.active_canvas.getCanvasHeight() < self.parentWidget.height()-self.active_canvas.getCaptionHeight()):
            height = self.active_canvas.getCanvasHeight() + self.active_canvas.getCaptionHeight()+4
         else:
            width += 20

         self.canvas.resize(width,height)

   def onResize(self,event):
      self.navigator.resize(self.navigator.width(),self.parentWidget.height())
      self.canvas.move(self.navigator.width(),0)
      self.adjustSize()

   def onNavResize(self,event):
      buttons = self.navigator.findChildren(QtGui.QPushButton)
      for button in buttons:
         button.resize(self.navigator.width()-10,button.height())


   def underMouse(self):
      return False
      pass

   def blockEntered(self,block):
      '''
       * Called when a RenderableBlock is being dragged and goes from being
       * outside this Widget to being inside the Widget.
       * @param block the RenderableBlock being dragged
      '''
      print("FactoryManager blockEntered")

      bitmap = QtGui.QPixmap("support\\DeleteCursor.png")
      cursor = QtGui.QCursor(bitmap,0,0)
      QtGui.QApplication.setOverrideCursor(cursor);
      #currentColor = Color.RED;
      #self.repaint();

   def blockExited(self, block):
      '''
      * Called when a RenderableBlock that was being dragged over this Widget
      * goes from being inside this Widget to being outside the Widget.
      * @param block the RenderableBlock being dragged
      '''
      #self.currentColor = Color.BLACK;
      #self.currentImage = self.tcImage;
      QtGui.QApplication.restoreOverrideCursor()
      #self.repaint();

   def blockDropped(self, block):
      from blocks.BlockUtilities import BlockUtilities
      # remove the block from the land of the living
      BlockUtilities.deleteBlock(block);
      #selfcurrentColor = Color.BLACK;
      #self.currentImage = self.tcImage;
      #self.revalidate();
      QtGui.QApplication.restoreOverrideCursor()
      #self.navigator.repaint();


   def contains(self,point):
      return self.navigator.rect().contains(point)

   def mapFromGlobal(self,pos):
      return self.navigator.mapFromGlobal(pos)

   def isVisible(self):
      return self.navigator.isVisible()

   def reset(self):
     self.staticCanvases = []
     self.dynamicCanvases = []
     self.subsetCanvases = []
     #self.navigator.setCanvas(self.staticCanvases, STATIC_NAME);
     #self.navigator.setCanvas(self.dynamicCanvases, DYNAMIC_NAME);
     #self.navigator.setCanvas(self.subsetCanvases, SUBSETS_NAME);

   def getWidgetAt(self,point):
        from blocks.Workspace import Workspace
        return Workspace.ws.getWidgetAt(point)
