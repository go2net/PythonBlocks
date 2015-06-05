from Blocks.Generator import Generator
import re

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
    self.definitions_ = {}

  def scrub_(self, block, code):
    '''
     * Common tasks for generating Python from blocks.
     * Handles comments for the specified block and any connected value blocks.
     * Calls any statements following this block.
     * @param {!Blockly.Block} block The current block.
     * @param {string} code The Python code created for this block.
     * @return {string} Python code with comments and subsequent blocks added.
     * @private
    '''
    return code
    commentCode = '';
    # Only collect comments for blocks that aren't inline.
    if (not block.outputConnection or not block.outputConnection.targetConnection):
      # Collect comment for this block.
      comment = block.getCommentText();
      if (comment):
        commentCode += Blockly.Python.prefixLines(comment, '# ') + '\n';

      # Collect comments for all value arguments.
      # Don't collect comments for nested statements.
      for  x in range(0, len(block.inputList)):
        if (block.inputList[x].type == Blockly.INPUT_VALUE):
          childBlock = block.inputList[x].connection.targetBlock();
          if (childBlock):
            comment = Blockly.Python.allNestedComments(childBlock);
            if (comment):
              commentCode += Blockly.Python.prefixLines(comment, '# ');

    nextBlock = block.nextConnection and block.nextConnection.targetBlock();
    nextCode = Blockly.Python.blockToCode(nextBlock);
    return commentCode + code + nextCode;

  def scrubNakedValue(self, line):
    '''
     * Naked values are top-level blocks with outputs that aren't plugged into
     * anything.
     * @param {string} line Line of generated code.
     * @return {string} Legal line of code.
    '''
    return line + '\n';


  def finish(self, code):
    '''
     * Prepend the generated code with the variable definitions.
     * @param {string} code Generated code.
     * @return {string} Completed code.
    '''
    # Convert the definitions dictionary into a list.
    imports = [];
    definitions = [];
    for name in self.definitions_:
      define = self.definitions_[name]       
      if re.match("(from\s+\S+\s+)?import\s+\S", define):
        imports.append(define);
      else:
        definitions.append(define);
        
    allDefs = '\n'.join(map(str, imports)) + '\n\n' + '\n\n'.join(map(str, definitions))
    allDefs = re.sub('\n\n+', '\n\n',allDefs)
    allDefs = re.sub('\n*$', '\n\n\n',allDefs)
    return allDefs + code;


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
      PythonGen.ORDER_NONE) or 'False';
      
    #print("argument="+argument)  
    branch = self.statementToCode(block, 'THEN') or PythonGen.PASS;
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
