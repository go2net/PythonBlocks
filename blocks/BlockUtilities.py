
from blocks.BlockStub import BlockStub
from blocks.Block import Block
from blocks.RenderableBlock import RenderableBlock

class BlockUtilities():

   instanceCounter = {}

   def isLabelValid(block, label, canvas):
      if(block == None or label == None):
         return False;
      elif(block.labelMustBeUnique()):
         # search through the current block instances active in the workspace
         for rb in canvas.getBlocksByName(block.getGenusName()):
            if(label == (rb.getBlock().getBlockLabel())):
               return False;

      # either label doesn't have to be unique or
      # label was found to be unique in the search
      return True;


   def cloneBlock(myblock, canvas):
      mygenusname = myblock.getGenusName();
      label = myblock.getBlockLabel();

      # sometimes the factory block will have an assigned label different
      # from its genus label.
      if(myblock.getInitialLabel() != (myblock.getBlockLabel())):
         # acquire prefix and suffix length from myblock label
         prefixLength = len(myblock.getLabelPrefix());
         suffixLength = len(myblock.getLabelSuffix());
         # we need to set the block label without the prefix and suffix attached because those
         # values are automatically concatenated to the string specified in setBlockLabel.  I know its
         # weird, but its the way block labels were designed.
         if(prefixLength > 0 or suffixLength > 0):  # TODO we could do this outside of this method, even in constructor
            label = myblock.getBlockLabel()


      # check genus instance counter and if label unique - change label accordingly
      # also check if label already has a value at the end, if so update counter to have the max value
      # TODO ria need to make this smarter
      # some issues to think about:
      #  - what if they throw out an instance, such as setup2? should the next time they take out
      #    a setup block, should it have setup2 on it?  but wouldn't that be confusing?
      #  - when we load up a new project with some instances with numbered labels, how do we keep
      #    track of new instances relative to these old ones?
      #  - the old implementation just iterated through all the instances of a particular genus in the
      #    workspace and compared a possible label to the current labels of that genus.  if there wasn't
      #    any current label that matched the possible label, it returned that label.  do we want to do this?
      #   is there something more efficient?

      labelWithIndex = label;  # labelWithIndex will have the instance value

      # initialize value that will be appended to the end of the label
      if(mygenusname in BlockUtilities.instanceCounter):
         value = BlockUtilities.instanceCounter[mygenusname];
      else:
         value = 0;
      # begin check for validation of label
      # iterate until label is valid
      while(not BlockUtilities.isLabelValid(myblock, labelWithIndex, canvas)):
         value +=1;
         labelWithIndex = labelWithIndex + value;


      # set valid label and save current instance number
      BlockUtilities.instanceCounter[mygenusname] = value
      if(labelWithIndex != (label)): # only set it if the label actually changed...
         label = labelWithIndex;

      if(isinstance(myblock,BlockStub)):
         parent = myblock.getParent();
         block = BlockStub(parent.blockID, parent.getGenusName(), parent.getBlockLabel(), myblock.getGenusName());
      else:
         block = Block.createBlock(myblock.getGenusName(), True, label);

      # TODO - djwendel - create a copy of the RB properties too, using an RB copy constructor.  Don't just use the genus.
      # RenderableBlock renderable = new RenderableBlock(this.getParentWidget(), block.blockID);

      renderable = RenderableBlock.from_blockID(None, block.blockID);
      renderable.initFinished = False
      #renderable.setZoomLevel(BlockUtilities.zoom);
      #renderable.redrawFromTop();
      #renderable.repaint();
      return renderable;

   def deleteBlock(block):
      block.move(0,0);

      #widget = block.getParentWidget();
      #if(widget != None):
      #   widget.removeBlock(block)

      #parent = block.getParent();
      #if(parent != None):
      #   parent.remove(block);
      #   parent.validate();

      block.setParent(None);
      #WorkspaceController.workspace.notifyListeners(WorkspaceEvent(widget, block.blockID, WorkspaceEvent.BLOCK_REMOVED));
