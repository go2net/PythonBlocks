from generators.PythonGen import PythonGen

def controls_if(pythonGen, block):
  # If/elseif/else condition.
  n = 0;
  argument = pythonGen.valueToCode(
    block, 
    'IF' + str(n), 
    PythonGen.ORDER_NONE) or 'False';

  branch = pythonGen.statementToCode(block, 'DO' + str(n)) or PythonGen.PASS;
  code = 'if ' + argument + ':\n' + branch;
  elseifCount = 0 #block.elseifCount
  for n in range(1, elseifCount+1):
    argument = pythonGen.valueToCode(block, 'IF' + str(n),
        PythonGen.ORDER_NONE) or 'False';
    branch = pythonGen.statementToCode(block, 'DO' + str(n)) or PythonGen.PASS;
    code += 'elif ' + argument + ':\n' + branch;
  elseCount_ = 1 #block.elseCount_
  if (elseCount_):
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

  return code;
 
 
def boolean(pythonGen, block):
  code = 'True' if block.getBlockFullLabel()=='true' else 'False'
  return [code, pythonGen.ORDER_ATOMIC];

def print_(pythonGen, block):
  # Print statement.
  argument0 = "\'Hello\'" #pythonGen.valueToCode(block, 'TEXT',
  #    PythonGen.ORDER_NONE) or '\'\'';
  
  return 'print(' + argument0 + ')\n';
