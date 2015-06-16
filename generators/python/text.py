from generators.PythonGen import PythonGen
def text_print(pythonGen, block):
  # Print statement.
  argument0 = pythonGen.valueToCode(block, '',
      PythonGen.ORDER_NONE) or '0';
      
  return 'print(' + argument0 + ')\n';
