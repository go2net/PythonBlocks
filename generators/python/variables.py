from generators.PythonGen import PythonGen

def set_num_var(pythonGen, block):
  # Variable setter.
  argument0 = pythonGen.valueToCode(block, '',
      PythonGen.ORDER_NONE) or '0';

  varName = block.getBlockLabel()
  return varName + ' = ' + argument0 + '\n';

def set_str_var(pythonGen, block):
  # Variable setter.
  argument0 = pythonGen.valueToCode(block, '',
      PythonGen.ORDER_NONE) or '0';

  varName = block.getBlockLabel()
  return varName + ' = ' + argument0 + '\n';


def str_var(pythonGen, block):
  varName = block.getBlockLabel()
  return [varName, pythonGen.ORDER_ATOMIC]
