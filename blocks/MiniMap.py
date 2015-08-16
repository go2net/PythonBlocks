#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      shijq
#
# Created:     19/04/2015
# Copyright:   (c) shijq 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time,sched
from PyQt4 import QtGui, QtCore
from blocks.WorkspaceWidget import WorkspaceWidget

class MiniMapEnlargerTimer():
   '''
   * This animator is responsible for enlarging or shrinking the
   * size of the MiniMap when expand() or shrink() is called,
   * respectively.
   '''
   # Constuctors an animator that can enlarge or skrink the miniMap
   def __init__(self,mini_map):
      self.mini_map = mini_map
      self.count = 0;
      #**absolute value of width growth*/

      self.step = 10
      self.dx = MiniMap.DEFAULT_WIDTH / self.step;

      #**absolute value of height Growth*/
      self.dy = MiniMap.DEFAULT_HEIGHT / self.step;
      self._expand = True;
      self.scheduler = sched.scheduler(time.time, time.sleep)
      self._running = False

   def _perform(self):
      if (self.count <= 0 or self.count > self.step*2):
         self.scheduler.cancel(self.event_perform)
         print("cancel")
      else:
         if (self._expand):
            self.count += 1;
         else:
            self.count -= 1;

      self.mini_map.MAPWIDTH = MiniMap.DEFAULT_WIDTH + self.count * self.dx;
      self.mini_map.MAPHEIGHT = MiniMap.DEFAULT_HEIGHT + self.count * self.dy;
      #print("Width: {0], Height: [1]",(self.mini_map.MAPWIDTH,self.mini_map.MAPHEIGHT))
      self.mini_map.repositionMiniMap();

   def periodic(self, action, actionargs=()):
      if self._running:
         self.event_perform = self.scheduler.enter(0.002, 2, self.periodic, (action, actionargs))
         action(*actionargs)

   def stop_func(self,string1):
      print("stop_func")
      self._running = False
      pass

   def expand(self):
      # enlargest this minimap
      self._expand = True;
      self.count+=1;
      self._running = True
      #self.event_stop = self.scheduler.enter(0.5, 1, self.stop_func, ("Large event.",))
      self.periodic(self._perform)
      self.scheduler.run( )


   def shrink(self):
      # enlargest this minimap
      self._expand = False;
      self.count-=1;
      self._running = True
      #self.event_stop = self.scheduler.enter(1, 1, self.stop_func, ("Large event.",))
      self.periodic(self._perform)
      self.scheduler.run( )

class MiniMap(QtGui.QFrame,WorkspaceWidget):

   #**the border width of the this mini map*/
   BORDER_WIDTH = 5;
   #**the default width of a mini map*/
   DEFAULT_WIDTH = 150;
   #**the default height of a mini map*/
   DEFAULT_HEIGHT = 75;


   def __init__(self,blockCanvas):
      QtGui.QWidget.__init__(self,blockCanvas)
      #print(blockCanvas)
      self.blockCanvas = blockCanvas;

      self.setAttribute(QtCore.Qt.WA_Hover);
      #**this.width*/
      self.MAPWIDTH = 150;
      #**this.height*/
      self.MAPHEIGHT = 75;
      #self.installEventFilter(self)
      self.setStyleSheet("background-color: rgb(240, 240, 240,200);")
      self.enlarger = MiniMapEnlargerTimer(self);
      self.resize(self.MAPWIDTH, self.MAPHEIGHT);
      pass

   def repositionMiniMap(self):
      if (self.parent() != None):
         self.resize(self.MAPWIDTH + 2 * MiniMap.BORDER_WIDTH, self.MAPHEIGHT + 2 * MiniMap.BORDER_WIDTH)
         self.move(self.parent().width() - self.MAPWIDTH - 2*self.BORDER_WIDTH-26, 0)
      self.repaint()

   def mouseMoveEvent(self, event):
      if event.buttons()&QtCore.Qt.LeftButton:
         self.mouseDragged(event)

   def enterEvent(self,event):
      print("enterEvent")
      self.expand = True;
      self.enlarger.expand();

   def leaveEvent(self,event):
      print("enterEvent")
      self.expand = False;
      self.enlarger.shrink();

   def contains(self,point):
      return self.rect().contains(point)

   def blockEntered(self,block):
      print ("blockEntered")
      self.expand = True;
      self.enlarger.expand();

   def blockExited(self,block):
      print ("blockExited")
      self.expand = False;
      self.enlarger.shrink();

   def rescaleRect(self, rec):
      return QtCore.QRect(
                (rec.x()*self.transformX),
                (rec.y()*self.transformY),
                (rec.width()*self.transformX),
                (rec.height()*self.transformY));

   def rescaleX(self, x):
      return (x*self.transformX);

   def rescaleY(self, y):
      return (y*self.transformY);

   def drawBoundingBox(self,p, block):
      blockRect = block.rect();
      #if(block.parent() != self.getCanvas()):
      blockRect.moveTopLeft(block.mapTo(self.getCanvas(),blockRect.topLeft()));
      blockRect = self.rescaleRect(blockRect);
      p.fillRect(blockRect,block.getBLockColor());
      p.setPen(QtGui.QColor(255,255,255));
      p.drawRect(blockRect);

   def getCanvas(self):
      return self.blockCanvas;

   def rescaleToWorld(self, p):
     point = QtCore.QPoint(p.x() / self.transformX, p.y() / self.transformY);
     return point;

   def scrollToPoint(self, p):
      transform = self.rescaleToWorld(p);
      self.blockCanvas.horizontalScrollBar().setValue(transform.x() - 0.5 * self.blockCanvas.width());
      self.blockCanvas.verticalScrollBar().setValue(transform.y() - 0.5 * self.blockCanvas.height());
      self.repaint();

   def mousePressEvent(self, e):
      self.scrollToPoint(e.pos());

   def mouseDragged(self, e):
      self.scrollToPoint(e.pos());

   def mouseReleased(self, e):
      self.scrollToPoint(e.pos());

   def paintEvent(self,event):
      from blocks.RenderableBlock import RenderableBlock
      from blocks.PageDivider import PageDivider
      #from Comment import Comment
      '''
        * @modifies this.bounds && this.blockCanvas && this.blocks && this.comments
        * @effects 1] Point this.blockCanvas to whatever current block
        * 			   canvas is in Workspace
        * 			2] Reset this.bounds to maintain aspect ratio and be
        * 			   16 pixels away from upper-right edge corner &&
        * 			3] Rerender this.blocks and this.comment toreflect
        * 			   real-time relative positions and dimension
      '''
      #should paint super first then reset canvas.
      #using new canvas, find new height and ratio.
      QtGui.QFrame.paintEvent(self,event);
      p = QtGui.QPainter();
      p.begin(self)
      # draw shadow border
      for i in range(0,self.BORDER_WIDTH):
         p.setPen(QtGui.QColor(200, 200, 150, 50 * (i + 1)));
         p.drawRect(i, i, self.width() - 1 - 2 * i, self.height() - 1 - 2 * i);

      # Aspect-Ratio Logic
      #self.blockCanvas = self.workspace;
      self.transformX = self.MAPWIDTH / self.getCanvas().width(); # MUST CAST MAPHEIGHT TO DOUBLE!!
      self.transformY = self.MAPHEIGHT / self.getCanvas().height();

      p.translate(5, 5);

      #for page in self.blockCanvas.getPages():
         #pageColor = page.getPageColor();
         #pageRect = self.rescaleRect(page.frameGeometry());
         #p.setPen(QtGui.QColor(pageColor.red(), pageColor.green(), pageColor.blue(), 200));
         #p.fillRect(pageRect,page.getPageColor());
         #p.setPen(QtGui.QColor.WHITE);
         #g.clipRect(pageRect.x, pageRect.y, pageRect.width, pageRect.height);
         #p.drawString(page.getPageName(), pageRect.x + 1, pageRect.height - 3);
         #if (page.getIcon() != None and self.expand):
         #    g.drawImage(page.getIcon(), pageRect.x + 1, pageRect.height - 28, 15, 15, null);

         #g.setClip(null);

      
      for component in self.findChildren(RenderableBlock):
         #print(component)
         # re-render this.blocks and this.comments
         if component != None and component.isVisible():
            if (component.isSearchResult()):
               p.setColor(Color.yellow);
            else:
               p.setColor(component.getBLockColor());

            self.drawBoundingBox(g, component);
      '''
      for component in self.findChildren(Comment):
         if component.isVisible():
            p.setColor(Color.yellow);
            self.drawBoundingBox(g, component);

      '''

      for component in self.getCanvas().findChildren(PageDivider) :
         #g.setPen(QtGui.QColor(0xCC,0xCC,0xCC));
         dividerRect = self.rescaleRect(component.frameGeometry());
         p.fillRect(dividerRect,QtGui.QColor(0xCC,0xCC,0xCC));

      '''
      for component in self.workspace.findChildren(RenderableBlock):
         if (isinstance(component,RenderableBlock) and component != None and component.isVisible()):
            #print(component)
            p.setPen(component.getBLockColor());
            self.drawBoundingBox(p, component);
         #elif (isinstance(component,Comment) and component.isVisible()):
         #   g.setColor(Color.yellow);
         #   drawBoundingBox(g, component);
      '''

      #print("for component in self.getCanvas().findChildren(RenderableBlock) :")
      #for component in self.getCanvas().findChildren(RenderableBlock) :
      #   #print(component)
      #   #g.setPen(QtGui.QColor(0xCC,0xCC,0xCC));
      #   p.setPen(component.getBLockColor());
      #   self.drawBoundingBox(p, component);
      #print(self.blockCanvas)
      for component in self.blockCanvas.getBlocks():
         if (isinstance(component,RenderableBlock) and component != None and component.isVisible()):
            #print(component)
            p.setPen(component.getBLockColor());
            self.drawBoundingBox(p, component);
         #elif (isinstance(component,Comment) and component.isVisible()):
         #   g.setColor(Color.yellow);
         #   drawBoundingBox(g, component);

      p.setPen(QtGui.QColor(255,0,0));
      p.drawRect(
             self.rescaleX(self.blockCanvas.horizontalScrollBar().value()),
             self.rescaleY(self.blockCanvas.verticalScrollBar().value()),
             self.rescaleX(self.blockCanvas.width()),
             self.rescaleY(self.blockCanvas.height()));

      p.end()
