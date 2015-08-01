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
from blocks.Block import Block
class BlockStub(Block):
  parentNameToParentBlock = {}
  parentNameToBlockStubs = {}
  def __init__(self, initParentID, parentGenus, parentName, stubGenus):

    self.parentGenus = parentGenus;
    self.parentName = parentName;
    self.stubGenus = stubGenus;    
    
    # there's a chance that the parent for this has not been added to parentNameToBlockStubs mapping
    key = parentName + parentGenus;
    if(key in BlockStub.parentNameToBlockStubs):
      BlockStub.parentNameToBlockStubs[parentName+parentGenus].append(self.blockID);
    else:
      stubs = []
      stubs.append(self.blockID);
      BlockStub.parentNameToBlockStubs[key] = stubs


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


  def parentNameChanged(oldParentName, newParentName, parentID):
    '''
     * Updates BlockStub hashmaps and the BlockStubs of the parent of its new name
     * @param oldParentName
     * @param newParentName
     * @param parentID
    '''
    oldKey = oldParentName + Block.getBlock(parentID).getGenusName();
    newKey = newParentName + Block.getBlock(parentID).getGenusName();

    # only update if parents name really did "change" meaning the new parent name is 
    # different from the old parent name
    if(oldKey !=newKey):
      BlockStub.parentNameToParentBlock[newKey] = parentID;

      # update the parent name of each stub 
      stubs = BlockStub.parentNameToBlockStubs[oldKey];
      for stub in stubs:
        blockStub = Block.getBlock(stub);
        blockStub.parentName = newParentName;
        # update block label of each
        blockStub.setBlockLabel(newParentName);
        blockStub.notifyRenderable();

      
      # check if any stubs already exist for new key
      existingStubs = parentNameToBlockStubs[newKey]
      if existingStubs != None:
        stubs += existingStubs
  
      parentNameToBlockStubs[newKey] = stubs
  
      # remove old parent name from hash maps
      parentNameToParentBlock.remove(oldKey);
      parentNameToBlockStubs.remove(oldKey);


if __name__ == '__main__':
    main()
