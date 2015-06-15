from generators.PythonGen import PythonGen
def set_str_var(pythonGen, block):
  # Variable setter.
  argument0 = pythonGen.valueToCode(block, 'VALUE',
      PythonGen.ORDER_NONE) or '0';
  varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'),
      Blockly.Variables.NAME_TYPE);
  return varName + ' = ' + argument0 + '\n';

