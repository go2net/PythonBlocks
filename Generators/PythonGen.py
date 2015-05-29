from Blocks.Generator import Generator

class PythonGen(Generator):
  '''
  * Order of operation ENUMs.
  * http://docs.python.org/reference/expressions.html#summary
  '''
  ORDER_ATOMIC = 0;            # 0 "" ...
  ORDER_COLLECTION = 1;        # tuples, lists, dictionaries
  ORDER_STRING_CONVERSION = 1; # `expression...`
  ORDER_MEMBER = 2;            # . []
  ORDER_FUNCTION_CALL = 2;     # ()
  ORDER_EXPONENTIATION = 3;    # **
  ORDER_UNARY_SIGN = 4;        # + -
  ORDER_BITWISE_NOT = 4;       # ~
  ORDER_MULTIPLICATIVE = 5;    # * / // %
  ORDER_ADDITIVE = 6;          # + -
  ORDER_BITWISE_SHIFT = 7;     # << >>
  ORDER_BITWISE_AND = 8;       # &
  ORDER_BITWISE_XOR = 9;       # ^
  ORDER_BITWISE_OR = 10;       # |
  ORDER_RELATIONAL = 11;       # in, not in, is, is not,
                               #    <, <=, >, >=, <>, !=, ==
  ORDER_LOGICAL_NOT = 12;      # not
  ORDER_LOGICAL_AND = 13;      # and
  ORDER_LOGICAL_OR = 14;       # or
  ORDER_CONDITIONAL = 15;      # if else
  ORDER_LAMBDA = 16;           # lambda
  ORDER_NONE = 99;             # (...)
  '''
   * Empty loops or conditionals are not allowed in Python.
  '''
  PASS = '  pass\n';

  def __init__(self, workspace):
    Generator.__init__(self,workspace)
    self.name_ = "Python"
    self.functions["controls_if"] = self.controls_if
    self.functions["if"] = self.ifBlock

  def controls_if(self, block):
    # If/elseif/else condition.
    n = 0;
    argument = self.valueToCode(
      block, 
      'IF' + n, 
      PythonGen.ORDER_NONE) or 'False';
    branch = self.statementToCode(block, 'DO' + n) or PythonGen.PASS;
    code = 'if ' + argument + ':\n' + branch;
    for n in range(1, block.elseifCount+1):
      argument = self.valueToCode(block, 'IF' + n,
          PythonGen.ORDER_NONE) or 'False';
      branch = self.statementToCode(block, 'DO' + n) or PythonGen.PASS;
      code += 'elif ' + argument + ':\n' + branch;

    if (block.elseCount_):
      branch = self.statementToCode(block, 'ELSE') or PythonGen.PASS;
      code += 'else:\n' + branch;
    return code;

  def ifBlock(self, block):
    # If/elseif/else condition.
    #n = 0;
    argument = self.valueToCode(
      block, 
      'TEST', 
      PythonGen.ORDER_NONE)# or 'False';
    print("argument="+argument)  
    branch = self.statementToCode(block, 'THEN') or PythonGen.PASS;
    code = 'if ' + argument + ':\n' + branch;
    print (code)
    
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
