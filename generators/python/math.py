from generators.PythonGen import PythonGen

def math_number(pythonGen, block):
  # Numeric value.
  code = block.getBlockLabel()
  #order = pythonGen.ORDER_UNARY_SIGN if code < 0 else  pythonGen.ORDER_ATOMIC
  
  return [code, pythonGen.ORDER_ATOMIC];


def math_const(pythonGen, block):
  # Constants: PI, E, the Golden Ratio, sqrt(2), 1/sqrt(2), INFINITY.
  CONSTANTS = {
    'π': ['math.pi', pythonGen.ORDER_MEMBER],
    'e': ['math.e', pythonGen.ORDER_MEMBER],
    'GOLDEN_RATIO': ['(1 + math.sqrt(5)) / 2',  pythonGen.ORDER_MULTIPLICATIVE],
    'SQRT2': ['math.sqrt(2)', pythonGen.ORDER_MEMBER],
    'SQRT1_2': ['math.sqrt(1.0 / 2)', pythonGen.ORDER_MEMBER],
    'INFINITY': ['float(\'inf\')',pythonGen.ORDER_ATOMIC]
  }  
  
  constant = block.getBlockLabel()

  if (constant != 'INFINITY') :
    pythonGen.definitions_['import_math'] = 'import math';
   
  return  CONSTANTS[constant];

def text_print(pythonGen, block):
  # Print statement.
  argument0 = pythonGen.valueToCode(block, '',
      PythonGen.ORDER_NONE) or '0';
      
  return 'print(' + argument0 + ')\n';
