from generators.PythonGen import PythonGen

def controls_repeat(pythonGen, block):
  # Repeat n times (internal number).
  repeats = pythonGen.valueToCode(block, 'times', PythonGen.ORDER_NONE) or 'False';
  branch = pythonGen.statementToCode(block, 'do') or PythonGen.PASS;
  branch = pythonGen.addLoopTrap(branch, block.getBlockID()) or  PythonGen.PASS;
  loopVar = 'count' # pythonGen.getDistinctName('count', pythonGen.NAME_TYPE);
  code = 'for ' + loopVar + ' in range(' + repeats + '):\n' + branch;
  return code;
