#from Blocks.Workspace import Workspace
import os, sys
class Generator():
    def __init__(self, workspace):
        self.STATEMENT_PREFIX = None
        self.INFINITE_LOOP_TRAP = None
        self.INDENT = '    ';
        self.workspace = workspace
        self.functions = {}

    def import_module_from_file(self, full_path_to_module):
        """
        Import a module given the full path/filename of the .py file

        Python 3.4

        """
        module = None

        # Get module name and path from full path
        module_dir, module_file = os.path.split(full_path_to_module)
        module_name, module_ext = os.path.splitext(module_file)
            
        if(sys.version_info >= (3,4)):    
            import importlib
            # Get module "spec" from filename
            spec = importlib.util.spec_from_file_location(module_name,full_path_to_module)
            module = spec.loader.load_module()
        else:
            import imp
            module = imp.load_source(module_name,full_path_to_module)
            
        return module

    def blockToCode(self, block):
        '''
         * Generate code for the specified block (and attached blocks).
         * @param {Blockly.Block} block The block to generate code for.
         * @return {string|!Array} For statement blocks, the generated code.
         *         For value blocks, an array containing the generated code and an
         *         operator order value.    Returns '' if block is null.
        '''
        if (block == None):
            return ''

        if (block.disabled):
            print('block.disabled)')     
            # Skip past this block if it is disabled.
            return self.blockToCode(block.getNextBlock())
            
        genus = block.getGenus()
        
        module_name = block.getProperty('module_name')
        if(module_name == ''):
            module_name = genus.getProperty('module_name')

        module = self.import_module_from_file(os.getcwd()+'\\'+module_name)
        
        function_name = block.getProperty('function_name')
        if(function_name == ''):
            function_name = genus.getProperty('function_name')            
   
        if(module_name == '' or function_name == ''): 
            raise Exception('Language "' + self.name_ + '" does not know how to generate code ' +
                    'for block type "' + block.getGenusName() + '".');

        func = getattr(module, function_name)
        code = func(self,block)
        
        # Release module
        del(module) 

        #if ( block.getGenusName() not in self.functions):
        #    raise Exception('Language "' + self.name_ + '" does not know how to generate code ' +
        #            'for block type "' + block.getGenusName() + '".');
     
        #func = self.functions[block.getGenusName()]
 
        # First argument to func.call is the value of 'this' in the generator.
        # Prior to 24 September 2013 'this' was the only way to access the block.
        # The current prefered method of accessing the block is through the second
        # argument to func.call, which becomes the first parameter to the generator.
        #code = func(self, block);

        if (isinstance(code, list)):
            # Value blocks return tuples of code and operator order.
            return [self.scrub_(block, code[0]), code[1]];
        elif (isinstance(code, str)):
            if (self.STATEMENT_PREFIX):
                code = self.STATEMENT_PREFIX.replace('/%1/g', '\'' + block.id + '\'') + code;
            return self.scrub_(block, code);
        elif (code == None):
            # Block has handled code generation itself.
            return '';
        else:
            raise Exception('Invalid code generated: ' + code)            
        
        
    def workspaceToCode(self):
        if (self.workspace == None):
            # Backwards compatability from before there could be multiple workspaces.
            print('No workspace specified in workspaceToCode call.    Guessing.');
            #self.workspace = Blockly.getMainWorkspace();

        code = [];
        #this.init(workspace);
        blocks = self.workspace.getTopBlocks(False);

        #print(blocks)
        for block in blocks:
            line = self.blockToCode(block);
            if (isinstance(line, list)):
                # Value blocks return tuples of code and operator order.
                # Top-level blocks don't care about operator order.
                line = line[0];

            if (line != None):
                if (block.outputConnection and self.scrubNakedValue):
                    # This block is a naked value.    Ask the language's code generator if
                    # it wants to append a semicolon, or something.
                    line = self.scrubNakedValue(line);

                code.append(line); 

        code = '\n'.join(map(str, code))    # Blank line between each section.
        
        code = self.finish(code);        

        # Final scrubbing of whitespace.
        code = code.replace('/^\s+\n/', '');
        code = code.replace('/\n\s+$/', '\n');
        code = code.replace('/[ \t]+\n/g', '\n');
        return code;    
        
    def valueToCode(self, block, name, order):

        if (order == None):
            raise Exception('Expecting valid order from block "' + block.type + '".');

        targetBlock = block.getInputTargetBlock(name);

        if (targetBlock == None):
            return ''
            
        tuple = self.blockToCode(targetBlock);

        if (tuple == ''):
            # Disabled block.
            return '';

        if (not isinstance(tuple, list)):
            # Value blocks must return code and order of operations info.
            # Statement blocks must only return code.
            raise Exception('Expecting tuple from value block "' + targetBlock.type + '".');

        code = tuple[0];
        innerOrder = tuple[1];
        if (innerOrder == None):
            raise Exception ('Expecting valid order from value block "' + targetBlock.type + '".');

        if (code != None and order <= innerOrder):
            if (order == innerOrder and (order == 0 or order == 99)):
                # Don't generate parens around NONE-NONE and ATOMIC-ATOMIC pairs.
                # 0 is the atomic order, 99 is the none order.    No parentheses needed.
                # In all known languages multiple such code blocks are not order
                # sensitive.    In fact in Python ('a' 'b') 'c' would fail.
                pass
            else:
                # The operators outside this code are stonger than the operators
                # inside this code.    To prevent the code from being pulled apart,
                # wrap the code in parentheses.
                # Technically, this should be handled on a language-by-language basis.
                # However all known (sane) languages use parentheses for grouping.
                code = '(' + code + ')';
        return code;
        
    def prefixLines(self, text, prefix) :
        import re
        return prefix + re.sub(r'\n(.)','\n' + prefix + r'\1', text)

    def addLoopTrap(self, branch, id):
        if (self.INFINITE_LOOP_TRAP) :
            branch = self.INFINITE_LOOP_TRAP.replace('/%1/g', '\'' + id + '\'') + branch;

        if (self.STATEMENT_PREFIX) :
            branch += self.prefixLines(self.STATEMENT_PREFIX.replace('/%1/g',
                    '\'' + id + '\''), self.INDENT);
        return branch;

    def statementToCode(self, block, name) :
        '''
         * Generate code representing the statement.    Indent the code.
         * @param {!Blockly.Block} block The block containing the input.
         * @param {string} name The name of the input.
         * @return {string} Generated code or '' if no blocks are connected.
        '''        
        targetBlock = block.getInputTargetBlock(name);
        if (targetBlock == None):
            return '';

        code = self.blockToCode(targetBlock);

        #if (not isinstance(code, str)):
        #    # Value blocks must return code and order of operations info.
        #    # Statement blocks must only return code.
        #    raise Exception('Expecting code from statement block "' + targetBlock.type + '".');

        if (code != None) :
            code = self.prefixLines(code, self.INDENT);
        return code;
