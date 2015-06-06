from Generators.PythonGen import PythonGen

def controls_if(pythonGen, block):
  # If/elseif/else condition.
  n = 0;
  argument = pythonGen.valueToCode(
    block, 
    'IF' + n, 
    PythonGen.ORDER_NONE) or 'False';

  branch = pythonGen.statementToCode(block, 'DO' + n) or PythonGen.PASS;
  code = 'if ' + argument + ':\n' + branch;
  for n in range(1, block.elseifCount+1):
    argument = pythonGen.valueToCode(block, 'IF' + n,
        PythonGen.ORDER_NONE) or 'False';
    branch = pythonGen.statementToCode(block, 'DO' + n) or PythonGen.PASS;
    code += 'elif ' + argument + ':\n' + branch;

  if (block.elseCount_):
    branch = pythonGen.statementToCode(block, 'ELSE') or PythonGen.PASS;
    code += 'else:\n' + branch;
  return code;

def ifBlock(pythonGen, block):
  # If/elseif/else condition.
  #n = 0;
  argument = pythonGen.valueToCode(
    block, 
    'TEST', 
    PythonGen.ORDER_NONE) or 'False';
    
  #print("argument="+argument)  
  branch = pythonGen.statementToCode(block, 'THEN') or PythonGen.PASS;
  code = 'if ' + argument + ':\n' + branch;
  #print (code)
  
  '''
  for n in range(1, block.elseifCount+1):
    argument = self.valueToCode(block, 'IF' + n,
        PythonGen.ORDER_NONE) or 'False';
    branch = self.statementToCode(block, 'DO' + n) or PythonGen.PASS;
    code += 'elif ' + argument + ':\n' + branch;

  if (block.elseCount_):
    branch = self.statementToCode(block, 'ELSE') or PythonGen.PASS;
    code += 'else:\n' + branch;
  '''
  return code;
  
def boolean_(pythonGen, block):
  code = 'True' if block.getBlockLabel()=='true' else 'False'
  return [code, pythonGen.ORDER_ATOMIC];