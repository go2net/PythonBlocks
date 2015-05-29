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
from Blocks.Block import Block
class BlockStub(Block):
   parentNameToBlockStubs = {}
   def __init__(self):
      pass

   def parentConnectorsChanged( parentID):
      key = Block.getBlock(parentID).getBlockLabel() + Block.getBlock(parentID).getGenusName();

      # update each stub only if stub is a caller (as callers are the only type of stubs that
      # can change its connectors after being created)
      stubs = BlockStub.parentNameToBlockStubs[key]
      for stub in stubs:
         blockStub = Block.getBlock(stub)
         if(blockStub.stubGenus.startsWith(CALLER_STUB)):
            blockStub.updateConnectors();
            # System.out.println("updated connectors of: "+blockStub);
            blockStub.notifyRenderable();

   def notifyRenderable(self):
      RenderableBlock.getRenderableBlock(blockID).repaint();


if __name__ == '__main__':
    main()
