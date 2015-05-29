#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      A21059
#
# Created:     10/03/2015
# Copyright:   (c) A21059 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Blocks.BlockControlLabel import BlockControlLabel

class CollapseLabel(BlockControlLabel):
   def __init__(self,blockID):
      BlockControlLabel.__init__(self,blockID)

if __name__ == '__main__':
    main()
