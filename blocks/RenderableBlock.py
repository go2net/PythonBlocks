
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import math, os, sys

from blocks.Block import Block
from blocks.BlockShape import BlockShape
from blocks.InfixBlockShape import InfixBlockShape
from blocks.CollapseLabel import CollapseLabel
from blocks.ConnectorTag import ConnectorTag
from blocks.NameLabel import NameLabel
from blocks.BlockLabel import BlockLabel
from blocks.SocketLabel import SocketLabel
from blocks.BlockConnectorShape import BlockConnectorShape
from blocks.GraphicsManager import GraphicsManager
from blocks.BlockShapeUtil import BlockShapeUtil
from blocks.BlockLinkChecker import BlockLinkChecker
from blocks.BlockImageIcon import BlockImageIcon

class RenderableBlock(QtGui.QWidget):

    ALL_RENDERABLE_BLOCKS = {} 
        
    def __init__(self, _workspaceWidget):         
        QtGui.QWidget.__init__(self)
        self._workspaceWidget = _workspaceWidget
        self.setMouseTracking(True);
        
    def __del__(self):
        pass

    @classmethod
    def from_block(cls, _workspaceWidget, block, isLoading=False,back_color=QtGui.QColor(225,225,225,255)):
        from blocks.WorkspaceController import WorkspaceController
        from blocks.FactoryManager import FactoryManager
        
        obj = cls(_workspaceWidget)
        
        obj.workspace = WorkspaceController.workspace
        obj.back_color = back_color
        obj.isLoading= isLoading
        
        obj._blockID = block.blockID;

        if(obj._blockID != -1):
          RenderableBlock.ALL_RENDERABLE_BLOCKS[obj.blockID] = obj
        else:
          RenderableBlock.tmpRB = obj
          
        #self.setAttribute(74, True);
        obj.mouse_enter = False
        obj.pickedUp = False
        obj.linkedDefArgsBefore = False
        obj.commentLabelChanged = False
        obj.dragging = False
        obj.overTrash = False

        obj.blockLabel = None
        obj.blockWidget = None
        obj.comment = None
        obj.buffImg = None
        obj.collapseLabel = None
        obj.last_link = None
        obj.blockShape = None
        
        obj.zoom = 1.0;
        obj.socketTags = []
        obj.imageMap = {}
        
        # initialize block image map
        # note: must do this before updateBuffImg();
        for  loc, img in obj.getBlock().getInitBlockImageMap().items():
            #print('BlockImageIcon')
            #print('Image ICON width=%d,height=%d'%(img.icon.width(), img.icon.height()))
            icon = BlockImageIcon(
                img.icon, 
                img.location, 
                img.isEditable,
                img.wrapText)
            obj.imageMap[loc] = icon
            icon.setParent(obj)
            #print('ICON width=%d,height=%d'%(icon.width(), icon.height()))
            #obj.add(icon)


        # initialize tags, labels, and sockets:
        obj.plugTag = ConnectorTag(block.getPlug());
        obj.afterTag = ConnectorTag(block.getAfterConnector());
        obj.beforeTag = ConnectorTag(block.getBeforeConnector());

        obj.blockLabel = NameLabel(obj, block.getBlockLabel(), block.getLabelPrefix(), block.getLabelSuffix(), BlockLabel.Type.NAME_LABEL, block.isLabelEditable, obj.blockID);

        #self.pageLabel = PageLabel(self.getBlock().getPageLabel(), BlockLabel.Type.PAGE_LABEL, False, self.blockID);

        obj.synchronizeSockets();

        # initialize collapse label
        if(block.isProcedureDeclBlock() and (obj.parent() == None or (not isinstance(obj.parent(), FactoryManager)))):
            obj.collapseLabel = CollapseLabel(obj.blockID);
            obj.collapseLabel.parent = obj

        if(block.isInfix()):
            obj.blockShape = InfixBlockShape(obj);
        else:
            obj.blockShape = BlockShape(obj);

        if(not obj.isLoading):
            obj.reformBlockShape()
            obj.updateBuffImg()
        else:
            obj.blockArea = QtGui.QPainterPath ()        
        
        #if(isinstance(obj,FactoryRenderableBlock)):
        #  Block.MAX_RESERVED_ID = max(Block.MAX_RESERVED_ID, obj.blockID)
          
        return obj
        
    
    @classmethod
    def from_blockID(cls, _workspaceWidget, blockID, isLoading=False,back_color=QtGui.QColor(225,225,225,255)): 
        return RenderableBlock.from_block(_workspaceWidget, Block.getBlock(blockID), isLoading,back_color)

    @property
    def blockID(self):
        """I'm the 'x' property."""
        return self._blockID

    @blockID.setter
    def blockID(self, value):
        self._blockID = value

    @blockID.deleter
    def blockID(self):
        del self._blockID 

    @property
    def workspaceWidget(self):
        """I'm the 'x' property."""
        #print(self._workspaceWidget)
        return self._workspaceWidget

    @workspaceWidget.setter
    def workspaceWidget(self, value):
        self._workspaceWidget = value

    def setBlockLabelUneditable(self):
        pass

    def getBlock(self):
        return Block.getBlock(self.blockID)

    def hasComment(self):
        if (self.comment != None):
            return True;
        return False;

    def reformBlockShape(self):

        if(self.blockShape == None): return

        self.abstractBlockArea = self.blockShape.reformArea();

        # TODO for zooming, create an AffineTransform to scale the block shape
        #at = AffineTransform();
        #at.setToScale(zoom, zoom);
        self.blockArea = self.abstractBlockArea #.createTransformedArea(at);
        #if(True): return
        #note: need to add twice the highlight stroke width so that the highlight does not get cut off
        updatedDimensionRect = QtCore.QRectF(
          self.x(),
          self.y(),
          self.blockArea.controlPointRect().width(),
          self.blockArea.controlPointRect().height());

        if (not self.contentsRect() == updatedDimensionRect):
            self.moveConnectedBlocks(); # bounds have changed, so move connected blocks

        self.setGeometry(updatedDimensionRect.toRect());

        #/////////////////////////////////////////
        #//set position of block labels.
        #//////////////////////////////////////////
        #if(self.pageLabel != None and self.getBlock().hasPageLabel()):
        #    self.pageLabel.update()

        if(self.blockLabel != None):
            self.blockLabel.update();

        if (self.collapseLabel != None):
            self.collapseLabel.update();

        if (self.comment != None):
            self.comment.update();

        for tag in self.socketTags:
            socket = tag.getSocket();
            label = tag.getLabel();
            if(label == None or SocketLabel.ignoreSocket(socket)):
                continue;

            label.update(self.getSocketAbstractPoint(socket));

    '''
     * Returns the height of the block shape of this
     * @return the height of the block shape of this
    '''
    def getBlockHeight(self):
        height = self.blockArea.controlPointRect().height()
        return height;


    '''
     * Returns the dimensions of the block shape of this
     * @return the dimensions of the block shape of this
    '''
    def getBlockSize(self):
        return self.blockArea.controlPointRect().size();


    def getSocketAbstractPoint(self, socket):
        tag = self.getConnectorTag(socket);
        return tag.getAbstractLocation();


    '''
     * Returns the width of the block shape of this
     * @return the width of the block shape of this
    '''
    def getBlockWidth(self):
        #return 0
        width = self.blockArea.controlPointRect().width()

        return width;

    def accomodateLabelsWidth(self):
        maxSocketWidth = 0;
        width = 0;

        for tag in self.socketTags:
            label = tag.getLabel()
            if(label != None):
                maxSocketWidth = max(maxSocketWidth, label.getAbstractWidth());

        if(self.blockLabel != None):
            if(self.getBlock().hasPageLabel()):
                width += math.max(self.blockLabel.getAbstractWidth(), self.pageLabel.getAbstractWidth()) + maxSocketWidth;
                width += self.getControlLabelsWidth();
            else:
                width += self.blockLabel.getAbstractWidth() + maxSocketWidth;
                width += self.getControlLabelsWidth() + 4;

        return width;


    def accomodatePageLabelHeight(self):
        if(self.getBlock().hasPageLabel()):
            return self.pageLabel.getAbstractHeight();
        else:
            return 0;

    def accomodateImagesHeight(self):
        maxImgHt = 0;
        for img in self.getBlock().getInitBlockImageMap().values():
            maxImgHt += img.icon.height();

        return maxImgHt;


    def accomodateImagesWidth(self):
        maxImgWt = 0;
        for img in self.getBlock().getInitBlockImageMap().values():
            maxImgWt += img.icon.width();

        return maxImgWt;

    def getBlockWidgetDimension(self):
        if (self.blockWidget == None):
            return QtCore.QSize(0,0);
        else:
            return self.blockWidget.getSize();


    def getMaxSocketShapeWidth(self):
        maxSocketWidth = 0;
        for socket in self.getBlock().getSockets():
            socketWidth = BlockConnectorShape.getConnectorDimensions(socket).width();
            if( socketWidth > maxSocketWidth):
                maxSocketWidth = socketWidth;

        return maxSocketWidth;

    def paintEvent(self,event):
        try:
          painter = QtGui.QPainter();
          #painter.setRenderHints(QtGui.QPainter.HighQualityAntialiasing)
          painter.begin(self)
          #painter.drawPath(self.blockArea);
          #return
          if(not self.isLoading):
              # if buffImg is null, redraw block shape
              if (self.buffImg == None):
                  self.reformBlockShape()
                  self.updateBuffImg(); #this method also moves connected blocks

              if (self.dragging):
                  #g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER,DRAGGING_ALPHA));
                  painter.drawImage(self.blockArea.controlPointRect(),self.buffImg);
                #g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER,1));
              else:
                  painter.drawImage(0,0,self.buffImg);
          painter.end()
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno,exc_obj)          

    def synchronizeLabelsAndSockets(self):
        blockLabelChanged = self.getBlock().getBlockLabel() != None and self.blockLabel.getText() != (self.getBlock().getBlockLabel())
        #pageLabelChanged = self.getBlock().getPageLabel() != None and not self.pageLabel.getText() == (self.getBlock().getPageLabel())
        socketLabelsChanged = False;

        # If tag label isn't the same as socket label, synchronize.
        # If the block doesn't have an editable socket label, synchronize.
        #
        #  Needed to not synchronize the socket if it is label editable so it doesn't synchronize when
        # it gains focus.
        #
        # May possibly be done better if synchronizeSockets is rewritten. It has to be written such that
        # it doesn't remove the sockets' JComponents/remake them. Currently relies on the synchronizeSockets()
        # call in getSocketPixelPoint(BlockConnector) to make sure the dimensions and number of sockets
        # are consistent.
        for i in range(0,self.getBlock().getNumSockets()):
            socket = self.getBlock().getSocketAt(i);
            tag = self.getConnectorTag(socket);
            if (tag != None):
                if(tag.getLabel() != None):
                    if (tag.getLabel().getText() != socket.getLabel()):
                        socketLabelsChanged = self.synchronizeSockets();
                        break;

            if (not socket.isLabelEditable):
                socketLabelsChanged = self.synchronizeSockets();
                break;

        if(blockLabelChanged):
            self.blockLabel.setText(self.getBlock().getBlockLabel());

        #if(pageLabelChanged):
        #    self.pageLabel.setText(getBlock().getPageLabel());

        if (blockLabelChanged or socketLabelsChanged or self.commentLabelChanged):
            self.reformBlockShape();
            self.commentLabelChanged = False;

        '''
        if(BlockLinkChecker.hasPlugEquivalent(getBlock())):
            plug = BlockLinkChecker.getPlugEquivalent(getBlock());
            plugBlock = Block.getBlock(plug.blockID);
            if(plugBlock != None):
                if (plugBlock.getConnectorTo(blockID) == None):
                    pass
                    #throw new RuntimeException("one-sided connection from "+getBlock().getBlockLabel()+" to "+Block.getBlock(blockID).getBlockLabel());

                RenderableBlock.getRenderableBlock(plug.blockID).updateSocketSpace(plugBlock.getConnectorTo(blockID), blockID, true);
        '''
        return False;

    def updateBuffImg(self, reform = True):

        # if label text has changed, then resync labels/sockets and reform shape
        if(not self.synchronizeLabelsAndSockets() and reform):
            self.reformBlockShape(); # if updateLabels is true, we don't need to reform AGAIN

        # update bounds of this renderableBlock as bounds of the shape
        updatedDimensionRect = self.blockArea.controlPointRect();

        # create image
        # note: need to add twice the highlight stroke width so that the highlight does not get cut off
        #GraphicsManager.recycleGCCompatibleImage(self.buffImg);

        #image = GraphicsManager.getGCCompatibleImage(
        #        self.blockArea.controlPointRect().width()+1,
        #        self.blockArea.controlPointRect().height()+1,
        #        self.back_color);

        #painter = QtGui.QPainter(image);
        #painter.setRenderHints(QtGui.QPainter.Antialiasing)
        #painter.begin(self)


        # ADD BLOCK COLOR
        #blockColor = self.getBLockColor();
        #blockColor.setAlpha(180)
        #brush = QtGui.QBrush(blockColor);
        #painter.setPen(blockColor);
        #painter.fillPath(self.blockArea,brush)
        #painter.drawPath(self.blockArea);
        #painter.end()

        #img.save("d:\\temp.bmp")

        #buff = create_string_buffer(image.width()*image.height()*4)
        #img_ptr = image.bits()
        #memmove(buff,int(img_ptr),buff._length_)

        #Bevel().bevelImage(buff,image.width(),image.height(),self.back_color.rgba());
        #bevelImage = QtGui.QImage(sip.voidptr(addressof(buff)), image.width(), image.height(), QtGui.QImage.Format_ARGB32)
        bevelImage = BlockShapeUtil.getBevelImage(updatedDimensionRect.width(), updatedDimensionRect.height(), self.blockArea);
        #bevelImage.save("d:\\temp.png")
        #GraphicsManager.recycleGCCompatibleImage(image);
        #del image

        self.buffImg = GraphicsManager.getGCCompatibleImage(
          self.blockArea.controlPointRect().width(),
          self.blockArea.controlPointRect().height(),
          self.back_color);

        p = QtGui.QPainter();        
        p.begin(self.buffImg)
        p.setRenderHint(QtGui.QPainter.Antialiasing, True)
        blockColor = self.getBLockColor();
        blockColor.setAlpha(180)
        brush = QtGui.QBrush(blockColor);
        p.setPen(QtGui.QColor(blockColor.red(), blockColor.green(), blockColor.blue(), 180));
        p.fillPath(self.blockArea,brush)
        #p.drawPath(self.blockArea);
        p.drawImage(0,0,bevelImage);
        
        # DRAW BLOCK IMAGES
        self.repositionBlockImages(self.blockArea.controlPointRect().width(),
            self.blockArea.controlPointRect().height());
        
        p.end()
        del p
        
        #self.buffImg.save("d:\\temp1.png")


    def repositionBlockImages(self, width,  height):
        '''
        * Draws the BlockImageIcon instances of this onto itself
        * @param buffImgG2 the current Graphics2D representation of this
         * @param width the current width of the buffered image
         * @param height the current height of the buffered image
        '''        
        margin = 5

        # TODO need to take other images into acct if we enable multiple block images
        for loc, img  in self.imageMap.items():
            icon = img.icon
            imgLoc = QPoint(0,0);
            if(img.location == 'CENTER'):
                imgLoc = QPoint((width-icon.width())/2, (height - icon.height())/2);
            elif(img.location ==  'NORTH'):
                imgLoc = QPoint((width-icon.width())/2, margin);
            elif(img.location ==  'SOUTH'):
                imgLoc = QPoint((width-icon.width())/2, height-margin-icon.height());
            elif(img.location ==  'EAST'):
                imgLoc = QPoint(width - margin-icon.width(), (height - icon.height())/2);
            elif(img.location ==  'WEST'):
                imgLoc = QPoint(margin, (height-icon.height())/2);
            elif(img.location ==  'NORTHEAST'):
                imgLoc = QPoint(width-margin-icon.width(), margin);
            elif(img.location ==  'NORTHWEST'):
                imgLoc = QPoint(margin, margin);
            elif(img.location ==  'SOUTHEAST'):
                imgLoc = QPoint(width-margin-icon.width(), height-margin-icon.height());
            elif(img.location ==  'SOUTHWEST'):
                # put in southwest corner
                imgLoc = QPoint(margin, height - (icon.height() + margin));

            if(self.getBlock().hasPlug() and  (img.location != 'EAST' or 
                img.location != 'NORTHEAST' or 
                img.location != 'SOUTHEAST')):
                        
                imgLoc.setX(imgLoc.x() + 4)  # need to nudge it a little more because of plug
            img.move(imgLoc.x(), imgLoc.y())

    def synchronizeSockets(self):
        changed = False;
        newSocketTags = []
        #for tag in self.socketTags:
        #    if(tag.getLabel() != None):
        #        tag.getLabel().setParent(None)
        #        #self.remove(tag.getLabel().getJComponent());

        for i in range(0, self.getBlock().getNumSockets()):
            socket = self.getBlock().getSocketAt(i);
            tag = self.getConnectorTag(socket);
            if(tag == None):
                tag = ConnectorTag(socket);
                if( SocketLabel.ignoreSocket(socket) ):
                    tag.setLabel(None); #ignored sockets have no label
                else:
                    label = SocketLabel(self, socket, socket.getLabel(),BlockLabel.Type.PORT_LABEL,socket.isLabelEditable,self.blockID);
                    argumentToolTip = self.getBlock().getArgumentDescription(i);
                    if(argumentToolTip != None):
                        label.setToolTipText(self.getBlock().getArgumentDescription(i).trim());

                    tag.setLabel(label);
                    label.setZoomLevel(self.getZoom());
                    label.setText(socket.getLabel());
                    #label.setParent(self)
                    #self.add(label.getJComponent());
                    changed = True;
            else:
                label = tag.getLabel();
                if( not SocketLabel.ignoreSocket(socket)):
                    # ignored bottom sockets or sockets with label == ""
                    if(label == None):
                        label = SocketLabel(socket, socket.getLabel(),BlockLabel.Type.PORT_LABEL,socket.isLabelEditable(),self.blockID);
                        argumentToolTip = self.getBlock().getArgumentDescription(i);
                        if(argumentToolTip != None):
                            label.setToolTipText(self.getBlock().getArgumentDescription(i).trim());

                        tag.setLabel(label);
                        label.setText(socket.getLabel());
                        self.add(label.getJComponent());
                        changed = True;
                    else:
                        if(label.getText() != socket.getLabel() or label.getParent() == None):
                            label.setText(socket.getLabel());
                            label.setParent(self)
                            #self.add(label.getJComponent());
                            changed = True;

                    label.setZoomLevel(self.getZoom());

            newSocketTags.append(tag);

        self.socketTags= []
        self.socketTags = newSocketTags;
        return changed;

    def getCollapseLabelWidth(self):
        if (self.collapseLabel != None):
            return self.collapseLabel.width();
        return 0;

    def getControlLabelsWidth(self):
        x = 0;
        if (self.getComment() != None):
            x += math.max(self.getComment().getCommentLabelWidth(), self.getCollapseLabelWidth());
        else:
            x += self.getCollapseLabelWidth();

        return x;


    def getConnectorTag(self,socket):
        if (socket == None):
            return
            #throw new RuntimeException("Socket may not be null");
        if(socket == (self.plugTag.getSocket())): return self.plugTag;
        if(socket == (self.afterTag.getSocket())): return self.afterTag;
        if(socket == (self.beforeTag.getSocket())): return self.beforeTag;
        for  tag in self.socketTags:
            if(socket == tag.getSocket()) :return tag;

        return None;

    def getSocketSpaceDimension(self,socket):
        if(self.getConnectorTag(socket)==None):
            return None;
        else:
            return self.getConnectorTag(socket).getDimension();

    def getRenderableBlock(blockID):
        if(blockID in RenderableBlock.ALL_RENDERABLE_BLOCKS):
            return RenderableBlock.ALL_RENDERABLE_BLOCKS[blockID]
        else:
            if(blockID == -1):
              return RenderableBlock.tmpRB
            else:
             print("Can not find block" + str(blockID))

    def getBlockWidget(self):
        return self.blockWidget;

    def getAbstractBlockArea(self):
        return self.abstractBlockArea;

    def isCollapsed(self):
        if (self.collapseLabel != None):
            return self.collapseLabel.isActive();
        return False;

    def getBLockColor(self):
        return self.getBlock().getColor();

    def getComment(self):
        return self.comment;

    def getZoom(self):
        return self.zoom;

    def rescale(self, x):
        return x*self.zoom;

    def getBlockShape(self):
        return self.blockShape;


    def updateSocketPoint(self,socket,  point):
        tag = self.getConnectorTag(socket);
        # TODO: what if tag does not exist?  should we throw exception or add new tag?
        if(tag != None):
          tag.setAbstractLocation(point);


    def linkDefArgs(self):

        if(not self.linkedDefArgsBefore and self.getBlock().hasDefaultArgs()):
            ids = iter(self.getBlock().linkAllDefaultArgs());
            sockets = iter(self.getBlock().getSockets());

            # Store the ids, sockets, and blocks we need to update.
            idList = []
            socketList = []
            argList = []

            while(True):
                try:
                    id = next(ids)
                    socket = next(sockets)
                    if(id != Block.NULL):
                        # for each block id, create a new RenderableBlock
                        arg = RenderableBlock(self.parent(), id);
                        arg.setZoomLevel(self.zoom);
                        # getParentWidget().addBlock(arg);
                  # arg.repaint();
                  # this.getParent().add(arg);
                  # set the location of the def arg at
                        myLocation = self.pos();
                        socketPt = self.getSocketPixelPoint(socket);
                        plugPt = arg.getSocketPixelPoint(arg.getBlock().getPlug());
                        arg.move((socketPt.x()+myLocation.x()-plugPt.x()), (socketPt.y()+myLocation.y()-plugPt.y()));
                        # update the socket space of at this socket
                        self.getConnectorTag(socket).resize(QtCore.QSize(
                            arg.getBlockWidth()-BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH,
                            arg.getBlockHeight()));
                        # drop each block to this parent's widget/component
                        # getParentWidget().blockDropped(arg);
                        self.parent().addBlock(arg);

                        idList.append(id);
                        socketList.append(socket);
                        argList.append(arg);
                except StopIteration:
                    break


            size = len(idList);
            for i in range(0,size):
                # Workspace.getInstance().notifyListeners(
                #     new WorkspaceEvent(this.getParentWidget(),
                #                argList.get(i).blockID,
                #                WorkspaceEvent.BLOCK_ADDED, true));

                # must call this method to update the dimensions of this
                # TODO ria in the future would be good to just link the default args
                # but first creating a block link object and then connecting
                # something like notifying the renderableblock to update its dimensions will be
                # take care of
                self.blockConnected(socketList.get(i), idList.get(i));
                argList[i].repaint();

        #self.redrawFromTop();
        self.linkedDefArgsBefore = True;


    '''
     * Returns a new Point object that represents the pixel location of this socket's center.
     * Mutating the new Point will not affect future calls to getSocketPoint; that is, this
     * method clones a new Point object.  The new Point object MAY NOT BE NULL.
     *
     * @param socket - the socket whose point we want.  socket MAY NOT BE NULL.
     * @return a Point representing the socket's center
     * @requires socket != null and socket is one of this block's socket
    '''
    def getSocketPixelPoint(self,socket):
        tag = self.getConnectorTag(socket);
        if (tag != None):
            return tag.getPixelLocation();

        print("Error, Socket has no connector tag: " + socket);
        return QtCore.QPoint(0,-100); #JBT hopefully this doesn't hurt anything,  this is masking a bug that needs to be tracked down, why is the connector tag missing?


    '''
     * Helper method for updateSocketSpace and calcStackDim.
     * Returns the maximum width of the specified blockID's socket blocks
     * @param blockID the Long blockID of the desired block
    '''
    def getMaxWidthOfSockets(self, blockID):
        width = 0;
        block = Block.getBlock(blockID);
        rb = RenderableBlock.getRenderableBlock(blockID);

        for socket in block.getSockets():
            socketDim = rb.getSocketSpaceDimension(socket);
            if(socketDim != None):
                if(socketDim.width() > width):
                    width = socketDim.width();

        return width;



    '''
     * Calculates the dimensions at the specified socket
     * @param socket BlockConnector to calculate the dimension of
     * @return Dimension of the specified socket
    '''
    def calcDimensionOfSocket(self,socket):
        finalDimension = QtCore.QSize(0,0);
        curBlockID = socket.blockID;
        while(curBlockID != Block.NULL):
            curBlock = Block.getBlock(curBlockID);
            # System.out.println("evaluating block :" + curBlock.getBlockLabel());
            curRenderableBlock = RenderableBlock.getRenderableBlock(curBlockID);
            if(curRenderableBlock == None) :
                return
            curRBSize = curRenderableBlock.getBlockSize();

            # add height
            finalDimension.setHeight(finalDimension.height() + curRBSize.height());
            # subtract after plug
            if(curBlock.hasAfterConnector()):
                finalDimension.setHeight(finalDimension.height() - BlockConnectorShape.CONTROL_PLUG_HEIGHT);

            # set largest width by iterating through to sockets and getting
            # the max width ONLY if curBlockID == connectedToBlockID
            width = curRBSize.width();

            if(curBlock.getNumSockets() > 0 and not curBlock.isInfix()):
                maxSocWidth = self.getMaxWidthOfSockets(curBlockID);
                # need to add the placeholder width within bottom sockets if maxSocWidth is zero
                if(maxSocWidth == 0):

                    # Adjust for zoom
                    width += 2 * BlockShape.BOTTOM_SOCKET_SIDE_SPACER * curRenderableBlock.getZoom();

                if(maxSocWidth > 0):
                    # need to minus the data plug width, otherwise it is counted twice
                    maxSocWidth -= BlockConnectorShape.NORMAL_DATA_PLUG_WIDTH;

                    # Adjust for zoom
                    width += maxSocWidth * curRenderableBlock.getZoom();


            if(width > finalDimension.width()): finalDimension.setWidth(width);

            # move down the afters
            curBlockID = Block.getBlock(curBlockID).getAfterBlockID();

        return finalDimension;
    def repaintBlock(self):
        self.clearBufferedImage();

        if(self.isVisible()):
          # NOTE: If it's not visible, this will throw an exception.
          # as during the redraw, it will try to access location information
          # of this
          self.repaint();
          #self.highlighter.repaint();



    #
    # Clears the BufferedImage of this
    #
    def clearBufferedImage(self):
        GraphicsManager.recycleGCCompatibleImage(self.buffImg);
        self.buffImg = None;


    '''
     * Updates the socket socket space of the specified connectedSocket of this after a block
     * connection/disconnection.  The socket space specifies the dimensions of the block
     * with id connectedToBlockID. RenderableBlock will use these dimensions to
     * determine the appropriate bounds to stretch the connectedSocket by.
     * @param connectedSocket BlockConnector which block connection/disconnection occurred
     * @param connectedToBlockID the Long block ID of the block connected/disconnected to the specified connectedSocket
     * @param isConnected boolean flag to determine if a block connected or disconnected to the connectedSocket
    '''
    def updateSocketSpace(self,connectedSocket, connectedToBlockID, isConnected):
        from blocks.BlockConnector import BlockConnector
        # System.out.println("updating socket space of :" + connectedSocket.getLabel() +" of rb: "+this);
        if(not isConnected):
            #remove the mapping
            self.getConnectorTag(connectedSocket).setDimension(None);

        else:
            # Block connectedToBlock = Block.getBlock(connectedToBlockID);
        # if no before block, then no recursion
        # if command connector with position type bottom (just a control connector socket)
        #  and we have a before, then skip and recurse up
            if(self.getBlock().getBeforeBlockID() != Block.NULL
             and BlockConnectorShape.isCommandConnector(connectedSocket)
             and connectedSocket.getPositionType() == BlockConnector.PositionType.BOTTOM):

                # get before connector
                beforeID = self.getBlock().getBeforeBlockID();
                beforeSocket = Block.getBlock(beforeID).getConnectorTo(self.blockID);
                RenderableBlock.getRenderableBlock(beforeID).updateSocketSpace(beforeSocket, self.blockID, True);
                return;


            # if empty before socket, then return
            # if(getBlock().hasBeforeConnector() && getBlock().getBeforeBlockID() == Block.NULL) return;

        # add dimension to the mapping
        self.getConnectorTag(connectedSocket).setDimension(self.calcDimensionOfSocket(connectedSocket));


        # reform shape with new socket dimension
        self.reformBlockShape();
        # next time, redraw with new positions and moving children blocks
        self.clearBufferedImage();

        # after everything on this block has been updated, recurse upward if possible
        plugEquiv = BlockLinkChecker.getPlugEquivalent(self.getBlock());
        if (plugEquiv != None and plugEquiv.hasBlock()):
            plugID = plugEquiv.blockID;
            socketEquiv = Block.getBlock(plugID).getConnectorTo(self.blockID);
            # update the socket space of a connected before/parent block
            RenderableBlock.getRenderableBlock(plugID).updateSocketSpace(socketEquiv, self.blockID, True);


    '''
     * Aligns all RenderableBlocks plugged into this one with the current location of this RenderableBlock.
     * These RenderableBlocks to move include blocks connected at sockets and the after connector.
    '''
    def moveConnectedBlocks(self):
        #if (True):
        #    print("move connected blocks of this: "+self);

        # if this hasn't been added anywhere, asking its location will break stuff
        if (self.parentWidget() == None): return;

        b = Block.getBlock(self.blockID);

        myScreenOffset = self.pos()

        for socket in BlockLinkChecker.getSocketEquivalents(b):
            socketLocation = self.getSocketPixelPoint(socket);
            if (socket.hasBlock()) :
                rb = RenderableBlock.getRenderableBlock(socket.blockID);

                # TODO: djwendel - this is a patch, but the root of the problem
                # needs to be found and fixed!!
                if (rb == None):
                    print("Block doesn't exist yet: "+str(socket.blockID));
                    continue;


                plugLocation = rb.getSocketPixelPoint(BlockLinkChecker.getPlugEquivalent(Block.getBlock(socket.blockID)));
                otherScreenOffset = self.parent().mapFrom(rb.parent(), rb.pos());
                otherScreenOffset = QtCore.QPoint(otherScreenOffset.x()-rb.x(), otherScreenOffset.y()-rb.y());

                rb.move(round(myScreenOffset.x()+socketLocation.x()-otherScreenOffset.x()-plugLocation.x()),
                          round(myScreenOffset.y()+socketLocation.y()-otherScreenOffset.y()-plugLocation.y()));

                rb.moveConnectedBlocks();

    '''
     * Notifies this renderable block that its socket connectedSocket had a block
     * disconnected from it.
    '''
    def blockDisconnected(self,disconnectedSocket):
        # notify block first so that we will only need to repaint this block once
        self.getBlock().blockDisconnected(disconnectedSocket);

        self.updateSocketSpace(disconnectedSocket, Block.NULL, False);

        # synchronize sockets
        self.synchronizeSockets();

    def hoverEnterEvent(self, event):
      print('inside')

    def hoverLeaveEvent(self, event):
      print('outside')

    def onMouseEnter(self):
        #print(self)
        self.mouse_enter = True
        painter = QtGui.QPainter();
        
        painter.begin(self.buffImg)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(255,170,0,255))
        pen.setWidth(3)
        painter.setPen(pen);
        painter.drawPath(self.blockArea);
        painter.end()
        
        self.repaint()

        #QtGui.QFrame.enterEvent(self,event);

    def onMouseLeave(self):
        self.mouse_enter = False
        self.updateBuffImg(False)
        self.repaint()

    def drawHighlightSocket(self,link,hightlight):
        if(link != None):
            #peer_block = link.peer_block
            peer_rb = RenderableBlock.getRenderableBlock(link.peer_block.blockID)
            if(peer_rb == self):
                print("peer_rb can not be self")
                return
            tag = peer_rb.getConnectorTag(link.peer_socket);
            self.last_peer_socket = tag
            #print (tag.aLoc)

            if(hightlight):
                painter = QtGui.QPainter();
                painter.begin(peer_rb.buffImg)
                pen = QtGui.QPen()
                pen.setColor(QtGui.QColor(255,170,0,255))
                pen.setWidth(3)
                painter.setPen(pen);
                path = QtGui.QPainterPath()
                if (BlockConnectorShape.isCommandConnector(link.peer_socket)):
                    path.moveTo(tag.aLoc.x()-BlockConnectorShape.CONTROL_PLUG_WIDTH / 2,tag.aLoc.y())
                    BlockShape.BCS.addControlConnectorShape(path,BlockConnectorShape.CONTROL_PLUG_WIDTH / 2,True)
                else:
                    path.moveTo(tag.aLoc.x(),tag.aLoc.y()-BlockConnectorShape.DATA_PLUG_HEIGHT / 2)
                    BlockShape.BCS.addDataConnection(path, link.peer_socket.type, True,False);

                painter.drawPath(path);
                painter.end()
            else:
                peer_rb.updateBuffImg(False)

            peer_rb.repaint()

        pass

    def descale(self,x):
        return x / self.zoom


    def getSaveNode(self, document):
        return self.getBlock().getSaveNode(document, self.descale(self.x()),
          self.descale(self.y()),
          self.comment.getSaveNode(document) if self.comment != None else None,
          self.isCollapsed());

    def blockConnected(self,connectedSocket, connectedBlockID):
        # notify block first so that we will only need to repaint this block once
        self.getBlock().blockConnected(connectedSocket, connectedBlockID);

        # synchronize sockets
        self.synchronizeSockets();

        # make sure the connected block is positioned correctly
        self.moveConnectedBlocks();

        self.updateSocketSpace(connectedSocket, connectedBlockID, True);

    def getHighlightStrokeWidth(self):
        return 12;

    def getStackBounds(self):
        return QtCore.QRect(self.pos(), self.calcStackDimensions(self));

    def calcStackDimensions(self,rb):
        if(rb.getBlock().getAfterBlockID() != Block.NULL):
            dim = self.calcStackDimensions(RenderableBlock.getRenderableBlock(rb.getBlock().getAfterBlockID()));
            return QtCore.QSize(max(rb.width() + rb.getMaxWidthOfSockets(rb.blockID),dim.width()),
                rb.height() + dim.height());
        else:
            return QtCore.QSize(rb.width() + rb.getMaxWidthOfSockets(rb.blockID),    rb.height());


    def getNearbyLink(self):
        return BlockLinkChecker.getLink(self, self.workspace.getActiveCanvas().getBlocks());


    def getLocationOnScreen(self):
        return self.parent().mapToGlobal(self.pos())

    def redrawFromTop(self):
        self.isLoading = False;

        for socket in BlockLinkChecker.getSocketEquivalents(self.getBlock()):

            if (socket.hasBlock()):
                #loop through all the afters of the connected block
                curBlockID = socket.blockID;
                # TODO: this is a patch, but we need to fix the root of the problem!
                if(RenderableBlock.getRenderableBlock(curBlockID) == None):
                    print(curBlockID) 
                    print("does not exist yet, block: "+curBlockID);
                    continue;

                RenderableBlock.getRenderableBlock(curBlockID).redrawFromTop();

                # add dimension to the mapping
                self.getConnectorTag(socket).setDimension(self.calcDimensionOfSocket(socket));
            else:
                self.getConnectorTag(socket).setDimension(None);

        # reform shape with new socket dimension
        self.reformBlockShape();
        # next time, redraw with new positions and moving children blocks
        self.clearBufferedImage();


    def loadBlockNode(blockNode, canvas):
        isBlock = blockNode.tag == ("Block");
        isBlockStub = blockNode.tag == ("BlockStub");

        if (isBlock or isBlockStub):
            rb = RenderableBlock.from_blockID(
                canvas,
                Block.loadBlockFrom(blockNode, canvas).blockID, 
                True);

            if (isBlockStub):
                # need to get actual block node
                stubchildren = blockNode.getchildren();
                for j in range(0,len(stubchildren)):
                    node = stubchildren[j];
                    if (node.tag == ("Block")):
                        blockNode = node;
                        break;


            if (rb.getBlock().labelMustBeUnique()):
             # TODO check the instance number of this block
                # and update instance checker
                pass

            blockLoc = QtCore.QPoint(0, 0);
            children = blockNode.getchildren();

            for child in children:
                if (child.tag == ("Location")):
                    # extract location information
                    RenderableBlock.extractLocationInfo(child, blockLoc);
                elif (child.tag == ("Comment")):
                    #rb.comment = Comment.loadComment(workspace, child.getChildNodes(), rb);
                    if (rb.comment != None):
                        rb.comment.setParent(rb.getParentWidget()    .getJComponent());

                elif (child.tag == ("Collapsed")):
                    rb.setCollapsed(True);

            # set location from info
            #rb.setParent(parent)
            rb.move(blockLoc.x(), blockLoc.y());
            #rb.show()
            #print(blockLoc);
            if (rb.comment != None):
                rb.comment.getArrow().updateArrow();          
          
            return rb;

        return None;

    def extractLocationInfo(location, loc):
        coordinates = location.getchildren()
        for coor in coordinates:
            if (coor.tag == ("X")):
                loc.setX(float(coor.text))
            elif (coor.tag == ("Y")):
                loc.setY(float(coor.text))
    
    def mousePressEvent(self, event):
        if self.blockArea.contains(event.globalPos()):
            rb = self
        else:
            rb = self.getUnderRB(event.globalPos())
    
        if(rb != None): 
            rb.onMousePress(event)         
  
    def onMousePress(self, event):
        for socket in BlockLinkChecker.getSocketEquivalents(self.getBlock()):
            if (socket.hasBlock()):
                RenderableBlock.getRenderableBlock(socket.blockID).raise_()

        self.raise_()
        #print('self.pickedUp = True')
        self.pickedUp = True; # mark this block as currently being picked up
        self.pressedPos = self.mapFromGlobal(event.globalPos())
        self.last_peer_socket = None
        self.focusedBlock = self
        
    def mouseMoveEvent(self, event): 
        
        if(self.focusedBlock != None and self.focusedBlock.pickedUp):
            self.focusedBlock.mouseDragged(event)
            return            

        if self.blockArea.contains(event.globalPos()):
            rb = self
        else:
            rb = self.getUnderRB(event.globalPos())

        if(rb != None):
            rb.onMouseEnter() 

        if(rb != self.focusedBlock):
            if(self.focusedBlock != None):
                self.focusedBlock.onMouseLeave() 
                
            self.focusedBlock = rb          

            
    def mouseReleaseEvent(self, event):
        
        if(self.focusedBlock != None and self.focusedBlock.pickedUp):
            self.focusedBlock.onMouseRelease(event) 
            return         
 
    def onMouseRelease(self, event):       
        self.window().onBlockClick(self)
        
        if event.button() == QtCore.Qt.LeftButton:
            if (not self.pickedUp):
                raise Exception("dropping without prior dragging?");
                return

            #dragHandler.mouseReleased(e);
          # if the block was dragged before...then
            if(self.dragging):
                widget =  self.workspace.getActiveCanvas().getWidgetAt(event.globalPos());
                self.stopDragging(widget);
                
                link = self.getNearbyLink(); # look for nearby link opportunities
                if (link != None):
                    link.connect();
                    #Workspace.getInstance().notifyListeners(WorkspaceEvent(widget, link, WorkspaceEvent.BLOCKS_CONNECTED));
                    RenderableBlock.getRenderableBlock(link.getSocketBlockID()).moveConnectedBlocks();

                # set the locations for X and Y based on zoom at 1.0
                #self.unzoomedX = self.calculateUnzoomedX(self.getX());
                #self.unzoomedY = self.calculateUnzoomedY(self.getY());

                #Workspace.getInstance().notifyListeners(WorkspaceEvent(widget, link, WorkspaceEvent.BLOCK_MOVED, true));
                #if(isinstance(widget, MiniMap)):
                #    Workspace.getInstance().getMiniMap().animateAutoCenter(this);

        self.pickedUp = False

        #if(e.isPopupTrigger() or SwingUtilities.isRightMouseButton(e) or e.isControlDown()):
        #    # add context menu at right click location to provide functionality
        #    # for adding new comments and removing comments
        #    popup = ContextMenu.getContextMenuFor(this);
        #    add(popup);
        #    popup.show(this, e.getX(), e.getY());

        self.workspace.getActiveCanvas().miniMap.repaint();
        #QtGui.QFrame.mouseReleaseEvent(self,event);

    def mouseDragged(self, event):

        from blocks.BlockLink import BlockLink
        if event.buttons()&QtCore.Qt.LeftButton:

            old_pos = self.parent().mapToGlobal(self.pos())

            dx = event.globalPos().x()-old_pos.x()-self.pressedPos.x()
            dy = event.globalPos().y()-old_pos.y()-self.pressedPos.y()

            self.move(self.x()+dx,self.y()+dy);
            widget = self.workspace.getActiveCanvas().getWidgetAt(event.globalPos());

            # if this is the first call to mouseDragged
            if(not self.dragging):
                block = self.getBlock();
                plug = BlockLinkChecker.getPlugEquivalent(block);

                if (plug != None and plug.hasBlock()):
                    parent = Block.getBlock(plug.blockID);
                    socket = parent.getConnectorTo(self.blockID);
                    link = BlockLink.getBlockLink(block, parent, plug, socket);
                    link.disconnect();
                    # socket is removed internally from block's socket list if socket is expandable
                    RenderableBlock.getRenderableBlock(parent.blockID).blockDisconnected(socket);
                self.startDragging(widget, event);


            # drag this block and all attached to it
            self.drag(widget, dx,dy,True);

            self.workspace.getActiveCanvas().miniMap.repaint();

    def drag(self, widget, dx,dy,isTopLevelBlock):

        #if (not self.pickedUp):
        #    return
        
        #throw new RuntimeException("dragging without prior pickup");
        # mark this as being dragged
        self.dragging = True;
        # move the block by drag amount
        if(not isTopLevelBlock):
            self.move(self.x()+dx, self.y()+dy);

        # send blockEntered/blockExited/blogDragged as appropriate
        if(widget != None):
            if (widget != self.lastDragWidget) :
                widget.blockEntered(self);
                if (self.lastDragWidget != None):
                    self.lastDragWidget.blockExited(self);

            #widget.blockDragged(self);
            self.lastDragWidget = widget;

        link = self.getNearbyLink(); # look for nearby link opportunities

        if((link == None and self.last_link!= None) or
            (link != None and not link.equal(self.last_link))):

            if(self.last_link != None):
                self.drawHighlightSocket(self.last_link,False)
                # erase last link highlight
                pass

        if(link != None):
          self.drawHighlightSocket(link,True)
          # hightlight current link
          pass

        self.last_link = link

        if(link != None):
            #peer_block = self.last_link.peer_block
            peer_rb = RenderableBlock.getRenderableBlock(self.last_link.peer_block.blockID)
            tag = peer_rb.getConnectorTag(link.peer_socket);
            self.last_peer_socket = tag

        # translate highlight along with the block - this would happen automatically,
        # but putting the call here takes out any lag.
        #self.highlighter.repaint();
        # Propagate the drag event to anything plugged into this block
        for socket in BlockLinkChecker.getSocketEquivalents(self.getBlock()):
            if (socket.hasBlock()):
                RenderableBlock.getRenderableBlock(socket.blockID).drag(widget, dx,dy,False);


    def startDragging(self, widget, event):
        self.lastDragWidget = widget;
        #if(renderable.hasComment()):
        #    renderable.comment.setConstrainComment(False);

        old_parent = self.parent()
        new_parent = self.workspace.getActiveCanvas().getWidgetAt(event.globalPos());

        #print('startDragging')
        #print(old_parent)
        #print(new_parent)

        old_pos = old_parent.mapToGlobal(self.pos())

        self.setParent(new_parent)
        #pp = self.parent()
        new_pos  = new_parent.mapFromGlobal(old_pos)


        self.move(new_pos.x(),new_pos.y());

        #new_pos = renderable.parent().mapFromGlobal(QtGui.QCursor.pos())
        #renderable.move(new_pos.x()-renderable.dx,new_pos.y()-renderable.dy);

        self.show()
        #renderable.raise_()
        self.repaint()
        #renderable.setHighlightParent(Workspace.getInstance());
        for socket in BlockLinkChecker.getSocketEquivalents(Block.getBlock(self.blockID)):
            if (socket.hasBlock()):
                RenderableBlock.getRenderableBlock(socket.blockID).startDragging(widget, event);


    def stopDragging(self, widget):
        '''
        * This method is called when this RenderableBlock is plugged into another RenderableBlock that has finished dragging.
        * @param widget the WorkspaceWidget where this RenderableBlock is being dropped.
        '''
        if (not self.dragging):
            return
        #throw new RuntimeException("dropping without prior dragging?");
        # notify children
        for socket in BlockLinkChecker.getSocketEquivalents(self.getBlock()):
            if (socket.hasBlock()):
                RenderableBlock.getRenderableBlock(socket.blockID).stopDragging(widget);

        # drop this block on its widget (if w is null it'll throw an exception)
     
        if(widget != None):
            #print("Dropped on"), print(widget)
            widget.blockDropped(self);
            #print(self.parent())
        # stop rendering as transparent
        self.dragging = False;

        # move comment
        if(self.hasComment()):
            if(self.parent() !=None):
                self.comment.setParent(self.parent());
            else:
                self.comment.setParent(None);


        #self.comment.setConstrainComment(true);
        #self.comment.setLocation(renderable.comment.getLocation());
        #self.comment.getArrow().updateArrow();

    def getUnderRB(self, globalPos):
        return self.workspaceWidget.canvas.getUnderRB(globalPos)
        
    @property
    def focusedBlock(self):
        return self.workspaceWidget.focusedBlock

    @focusedBlock.setter
    def focusedBlock(self, value):
        self.workspaceWidget.focusedBlock = value
