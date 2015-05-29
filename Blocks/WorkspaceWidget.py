#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      shijq
#
# Created:     18/04/2015
# Copyright:   (c) shijq 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class WorkspaceWidget():

   '''
   * Called by RenderableBlocks that get "dropped" onto this Widget
   * @param block the RenderableBlock that is "dropped" onto this Widget
   '''
   def blockDropped(self,block):
      pass
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
      pass

   '''
   * Adds a collection of blocks to this widget internally and graphically.
   * This method adds blocks internally first, and only updates graphically
   * once all of the blocks have been added.  It is therefore preferable to
   * use this method rather than addBlock whenever multiple blocks will be added.
   * @param blocks the Collection of RenderableBlocks to add
   '''
   def addBlocks(self,blocks):
      pass

   '''
   * Widgets must be able to report whether a given point is inside them
   * @param x
   * @param y
   '''
   def contains(self,x, y):
      pass

   '''
   * Very Java Swing dependent method
   * @return the JComponent-ized cast of this widget.
   '''
   def getJComponent(self):
      pass

   '''
   * Returns the set of blocks that abstract "lives" inside this widget.
   * Does not return all the blocks that exists in thsi component,
   * or return all the blocks that are handled by this widget.  Rather,
   * the set of blocks returned all the blocks that "lives" in this widget.
   '''
   def getBlocks(self):
      pass
