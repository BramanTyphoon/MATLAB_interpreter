#Full interpreter for Matlab-to-python interpreter
import ply.yacc as yacc
import ply.lex as lex
import io_util as util
import os
import glob
import string
import matlab_lexxer
from matlab_lexxer import tokens
import matlab_parser
import time
#import numpy as num
#import scipy as sci

### Left to do: ###
### -test case development
### -debugging
###_____________###


# Define directories containing all matlab functions
userfuns = ''
matfuns = 'C:\\\\Program Files\\\\MATLAB\\\\R2011a\\\\toolbox\\\\'

# Build lexer and parser from predefined rules
matlexer = lex.lex(module=matlab_lexxer)
matparser = yacc.yacc(module=matlab_parser,tabmodule='parsetab')

# Dictionary containing matlab to python symbol mappings
binops = {
    '+' : '+',
    '-' : '-',
    '~' : 'not ',
    ':' : ':',
    '<' : '<',
    '>' : '>',
    '<=' : '<=',
    '>=' : '>=',
    '==' : '==',
    '~=' : '!=',
    '&&' : 'and',
    '||' : 'or',
    '&' : 'tricky',
    '|' : 'tricky',
    '.*' : '*',
    '*' : 'tricky',
    '/' : '/',
    './' : '/',
    '.^' : '**',
    '^' : '**',
    '\'' : '\.conj\.transpose()',
    '\.\'' : '.transpose()',
    '\\' : 'tricky'
    }

# Dictionary containing function equivalencies
fun_trans = {
    'max' : 'np.amax',
    'min' : 'np.amin',
    'size' : 'special',
    'double' : 'float',
    'length' : 'len',
    'int' : 'int',
    'zeros' : 'special',
    'ones' : 'special',
    'eye' : 'eye',
    'error' : 'raise Exception',
    'diag' : 'diag',
    'rand' : 'random.rand',
    'linspace' : 'linspace',
    'repmat' : 'special',
    'norm' : 'linalg.norm',
    'fft' : 'fft',
    'ifft' : 'ifft',
    'sort' : 'sort',
    'sortrows' : 'special',
    'num2str' : 'str',
    'strcat' : 'special',
    'ceil' : 'math.ceil',
    'floor' : 'math.floor',
    'abs' : 'abs',
    'sum' : 'fsum',
    'mod' : 'special',
    'rem' : 'special',
    'run' : 'execfile',
    'disp' : 'print',
    'sqrt' : 'sqrt',
    'round' : 'round',
    'strcmp' : 'special',
    'cat' : 'special',
    'eig' : 'special',
    'throw' : 'special',
    'rethrow' : 'special',
    'cd' : 'os.chdir',
    'dir' : 'special',
    'fullfile' : 'os.path.join',
    'regexp' : 'special',
    'fclose' : 'special',
    'clear' : 'special',    # Keycall
    'close' : 'special',    # Keycall
    'break' : 'special',    # Keycall
    'clc' : 'special',      # Keycall
    'continue' : 'special'  # Keycall
    }

# Dictionary of functions to import as modules at the end
fun_to_import = {}



# Main driver for interpreting Matlab code
def rewrite(instring):
    

    # Parse the input file
    parsetree = matparser.parse(instring,lexer=matlexer)
    #print parsetree

    # Interpret the parse tree branch-by-branch to build a string
    # to be later written to a file
    output_text = interpret(parsetree)

    # Add names of modules that need to be added manually
    import_text = '### Modules to be imported ###\n' + \
                  'import os \nfrom numpy import \*\n' + \
                  'import scipy as Sci\nimport scipy.linalg\nimport os\n' + \
                  'import numpy as np\n'
    for fun in fun_to_import:
        import_text += '#\t' + fun + ': ' + str(fun_to_import[fun]) + '\n'
    output_text = import_text + '\n\n\n' + output_text

    # Add parser and parse-time information
    time_text = '### This module was automatically generated from MATLAB\'s  ###\n' + \
                '### scripting language using software written by:          ###\n' + \
                '### James F. Bramante.                                     ###\n' + \
                '### This module translation was completed at:              ###\n' + \
                '### ' + time.asctime(time.gmtime()) + ' UTC                           ###\n\n\n'
    output_text = time_text + output_text

    # Manually edit some inefficient/duplicate code caused by imperfect
    # coding solutions
    
    return output_text



# The overall interpreter
def interpret (ptree):
    env = (None,env_new())   # Initialize an environment
    outstring = ''                  # Initialize output string

    # Iterate through branches of a parse tree, interpreting them
    # individually and keeping track of the environment
    for branch in ptree:
        outputs = interpret_branch(branch,0,env)
        outstring += ('\n' + outputs[0])

    return outstring
    

# Interpreter for individual branches of a parse tree
def interpret_branch (branch,tabs,env):

    out = ''        # Initialize output variable
    
    # Determine whether each parse 'branch' is a compound statement
    # or a function definition and interpret accordingly
    if branch[0] == 'function':
        foutput = branch[1]
        fname = branch[2]
        fargs = interpret_args(branch[3])
        fbody = branch[4]
        
        # Nest, then update environment with function's arguments
        new_env = (env,env_new)
        for arg in fargs:
            env_update(arg,'IDENTIFIER','variable',new_env)
                
        # Construct output string
        out += ('\n\t'*tabs + 'def ' + fname + ' (' + fargs + ')\n' + \
                interpret_branch(fbody,tabs+1,new_env)[0] + '\n' + \
                '\t'*tabs + 'return ' + foutput + '\n')
        return (out,tabs,env)


    elif branch[0] == 'compoundstmt':
        # Iterate through the statements, translating one by one
        for stmt in branch[1]:
            # If the statement is a comment, handling is simple
            if stmt[0] == 'COMMENT':
                out += '\t'*tabs + '# ' + stmt[1] + '\n'
            else:
                # Note that the environment is updated within interpret_stmt
                out += '\n' + interpret_stmt(stmt,tabs,env)
        return (out,tabs,env)


# Interpret individual statements
def interpret_stmt (stmt, tabs, env):

    if type(stmt) == type([]):
        return (''.join([interpret_stmt(st,tabs,env) for st in stmt]))

    stype = stmt[0]
    out = '\t'*tabs

    # For every type, translation is customized
    if stype == 'if' or stype == 'for' or stype == 'while':
        out += (stype + ' ' + interpret_exp(stmt[1],env) + ':\n' + \
                ''.join([interpret_stmt(st,tabs+1,env) for st in stmt[2]]) + '\n')
        return out
    elif stype == 'if-then-else':
        out += ('if ' + interpret_exp(stmt[1],env) + ':\n' + ''.join([interpret_stmt(st,tabs+1,env) for st in stmt[2]]) + \
               '\n' + '\t'*tabs + 'else:\n' + ''.join([interpret_stmt(st,tabs+1,env) for st in stmt[3]]) + '\n')
        return out
    elif stype == 'return':
        return (out + 'return ' + interpret_exp(stmt[1],env) + '\n')
    elif stype == 'exp':
        return (out + interpret_exp(stmt[1],env) + '\n')
    elif stype == 'structcall':
        return (out + stmt[1] + '[' + stmt[2] + ']\n')
    elif stype == 'comment':
        return (out + '#' + stmt[1] + '\n')
    elif stype == 'assign':
        out += stmt[1] + ' = '
        env_update(stmt[1],'identifier','variable',env)
        val = interpret_exp(stmt[2],env)
        valtype = env_lookup(val, env)
        if valtype[0] == 'variable':
            env_update(stmt[1],valtype[1],'variable',env)
            if valtype[1] == 'matrix' or valtype[1] == 'identifier':
                out += val + '.copy()\n'
                out = string.replace(out,'\.copy()\.copy()','\.copy()')
            else:
                out += val + '\n'
        else:
            env_update(stmt[1],'undefined','variable',env)
            out += val + '\n'         
        return out
    
    # Used for assign statements assigning values to multiple variables
    # e.g. '[a,b,c] = size(mat)'
    elif stype == 'multi-assign':
        fargs = [interpret_exp(x, env) + ',' for x in stmt[1]]
        fargs = ''.join(fargs)
        fargs = string.rstrip(fargs,',')
        val = interpret_exp(stmt[2],env)
        out += fargs + ' = ' + val + '\n'
        vartype = env_lookup(val, env)
        for exp in stmt[1]:
            env_update(interpret_exp(exp,env),vartype,'variable',env)
        return out       

    # Handle keyword function calls as normal function calls
    elif stype == 'keycall':
        fname = stmt[1]
        if stmt[2]:
            fargs = [interpret_exp(x,env) + ',' for x in stmt[2]]
            fargs = ''.join(fargs)
            fargs = string.rstrip(fargs,',')
        else:
            fargs = ''
        if fun_trans[fname] != 'special':
            return (out + fun_trans[fname] + '(' + fargs + ')\n')
        else:
            return (out + interpret_functions(fname,stmt[2],env) + '\n')

    # Handle switch-case statements, which have no direct python equivalent
    elif stype == 'switch':
        case1 = stmt[2][0]
        casevar = interpret_exp(stmt[1],env)
        # Consider the odd case of just an otherwise clause, which renders
        # the switch clause useless, but might be technically admissable
        if case1[0] == 'otherwise':
            return ('\n' + interpret_stmt(case1[2],tabs,env))
        # Normal cases
        out += ('if ' + casevar + ' == ' + interpret_exp(case1[1],env) + ':\n')
        out += (interpret_stmt(case1[2],tabs+1,env) + '\t'*tabs)
        for clause in stmt[1:]:
            if clause[0] == 'case':
                out += ('elif ' + casevar + ' == ' + \
                        interpret_exp(clause[1],env) + ':\n')
                out += interpret_stmt(case[2],tabs+1,env)
            elif clause[0] == 'otherwise':
                out += ('else:' + '\n')
                out += interpret_stmt(clause[2],tabs+1,env)
        return out

    # Handle try-catch statements, requiring some finagling
    elif stype == 'try':
        out += 'try:\n'
        out += (interpret_stmt(stmt[1],tabs+1,env) + '\t'*tabs)
        for clause in stmt[2]:
            if clause[1]:
                out += ('except Exception as ' + interpret_exp(clause[1],env) +\
                        ':\n')
            else:
                out += 'except:\n'
            out += interpret_stmt(clause[2],tabs+1,env)
        return out

    # Handle loose expressions, often function calls without important
    # returns or results
    elif stype == 'exp':
        return (out + interpret_exp(stmt[1],env) + '\n')
    else:
        raise GenError('Ihis statement is of an unknown type: ' + str(stmt))



# Interpret individual expressions
def interpret_exp (exp, env):

    # Takes care of the empty string
    if not exp:
        return ''

    # The expression's subtype
    etype = exp[0]
    
    # Number terminals
    if etype == 'float':
        env_update(str(exp[1]),etype,'variable',env)
        return str(exp[1])
    elif etype == 'integer':
        env_update(str(exp[1]),etype,'variable',env)
        return str(exp[1])
    
    # Keyword terminals
    elif etype == 'keyword':
        return (' ' + exp[1] + ' ')
    
    # String terminals
    elif etype == 'string':
        env_update(str(exp[1]),etype,'variable',env)
        return ('"' + exp[1] + '"')
    # Directory terminals - special cases of string terminals for filepaths
    elif etype == 'directory':
        env_update(str(exp[1]),etype,'variable',env)
        return string.replace('"' + exp[1] + '"','\\','\\\\')
    
    # Identifier terminals
    elif etype == 'identifier':
        env_update(str(exp[1]),etype,'variable',env)
        return exp[1]

    # Matrix declarations and semi-terminal
    elif etype == 'row':
        out1 = ''.join([interpret_exp(x,env) + ',' for x in exp[1]])
        out1 = '[' + string.rstrip(out1,',') + ']'
        out2 = ''.join([interpret_exp(x,env) + ',' for x in exp[2]])
        out2 = '[' + string.rstrip(out2,',') + ']'
        return out1 + ',' + out2
    elif etype == 'matrix':
        out = ''.join([interpret_exp(x,env) + ',' for x in exp[1]])
        out = string.rstrip(out,',')
        out = string.replace(out,'[[','[')
        out = string.replace(out,']]',']')
        out = 'array([' + out + '])'
        env_update(out,etype,'variable',env)
        return out
    
    # The transpose operation
    elif etype == 'transpose':
        return interpret_exp(exp[1],env) + binops[exp[2]]
    
    # Expressions inside parentheses
    elif etype == 'parens':
        out = '(' + interpret_exp(exp[1],env) + ')'
        env_update(out,etype,'variable',env)
        return out
    
    # All binary operations, taking arrays into account
    elif etype == 'binop':
        op = exp[2]
        out = ''
        a = interpret_exp(exp[1],env)
        b = interpret_exp(exp[3],env)
        atype = env_lookup(a,env)[1]
        btype = env_lookup(b,env)[1]
        
        # Go through all the tricky operations, defining how to handle
        # each one separately
        if binops[op] == 'tricky':
            if op == '\&':
                out = ('logical_and(' + interpret_exp(a,env) + ',' +\
                        interpret_exp(b,env) + ')')
            if op == '\|':
                out = ('logical_or(' + interpret_exp(a,env) + ',' +\
                        interpret_exp(b,env) + ')')
            if op == '*':
                if atype == 'matrix' and btype == 'matrix':
                    out = ('dot(' + interpret_exp(a,env) + ',' +\
                            interpret_exp(b,env) + ')')
                else:
                    out = (a + ' ' + '*' + ' ' + b)
            if op == '\\':
                out = ('linalg.lstlq(' + a + ',' + b+ ')')
            
        # Regular operations
        else:
            out = (a + ' ' + binops[op] + ' ' + b)
        if atype == 'matrix' or btype == 'matrix':
            env_update(out,'matrix','variable',env)
        else:
            env_update(out,'number','variable',env)
        return out
        
    # Interpreting function calls (and matrix indexing)
    elif etype == 'call':
        fname = exp[1]
        fargs = [interpret_exp(x,env) + ',' for x in exp[2]]
        fargs = ''.join(fargs)
        fargs = string.rstrip(fargs,',')
        
        # If the Matlab function has an exact replacement in python, use that
        if fname in fun_trans:
            if fun_trans[fname] != 'special':
                return (fun_trans[fname] + '(' + fargs + ')')
            else:
                return interpret_functions(fname,exp[2],env)
        else:
            # Look for the functions in the environment and then
            # user directories
            ftype = env_lookup(fname,env)

            # Beware over-slicing with the 'assign' statement code
            if ftype[0] == 'variable':
                fargs = [interpret_exp(x,env) + '-1,' for x in exp[2]]
                fargs = ''.join(fargs)
                fargs = string.replace(fargs,': -1,',': ,')
                fargs = string.rstrip(fargs,',')
                return (fname + '[' + fargs + '].copy()')
            
            elif ftype[0] == 'internal_function':
                return (fname + '(' + fargs + ')')
            elif ftype[0] == 'user_function' or ftype[0] == 'matlab_function':
                if fname not in fun_to_import:
                    fun_to_import[fname] = ftype
                return (fname + '(' + fargs + ')')
            elif ftype[0] == 'undefined':
                if fname not in fun_to_import:
                    fun_to_import[fname] = ftype
                return (fname + '(' + fargs + ')')

    # Interpreting ranges usually found as part of indexing
    elif etype == 'range':
        st = interpret_exp(exp[1],env)
        en = interpret_exp(exp[2],env)
        return (st + '-1' + ':' + en + '+1')
    elif etype == 'steppedrange':
        st = interpret_exp(exp[1],env)
        step = interpret_exp(exp[2],env)
        en = interpret_exp(exp[3],env)
        return (st + '-1' + ':' + en + '+1' + ':' + step)

    # Interpreting ranges associated with MATLAB for loops
    elif etype == 'for_range':
        var = exp[1]
        st = interpret_exp(exp[2],env)
        en = interpret_exp(exp[3],env)
        env_update(var,'number','variable',env)
        return (var + ' in ' + 'range(' + st + ',' + en + '+1)')
    elif etype == 'for_steppedrange':
        var = exp[1]
        st = interpret_exp(exp[2],env)
        step = interpret_exp(exp[3],env)
        en = interpret_exp(exp[4],env)
        env_update(var,'number','variable',env)
        return (var + ' in ' + 'range(' + st + ',' + en + '+1,' + step + ')')

    # Interpreting cell index calls
    elif etype == 'cellindex':
        fname = exp[1]
        fargs = [interpret_exp(x,env) + '-1,' for x in exp[2]]
        fargs = ''.join(fargs)
        fargs = string.rstrip(fargs,',')
        env_update(fname,'cell','variable',env)
        return (fname + '[' + fargs + ']')

        

# Creates a new environment with two separate dictionaries for functions and
# variables
def env_new ():
    env = dict()
    env['function'] = dict()
    env['variable'] = dict()
    return env

# Updates an environment, either its function or variable sections
def env_update (varname, varvalue, env_type, env):
    env[-1][env_type][varname] = varvalue

# Looks up variables in hierarchy of environments and directories
def env_lookup (varname, env):
    # Look first in variable section
    if varname in env[-1]['variable']:
        return ('variable', env[-1]['variable'][varname])
    # Look next in functions
    elif varname in env[-1]['function']:
        return ('internal_function', env[-1]['function'][varname])
    # Look higher up in environment
    elif env[-2]:
        return env_lookup(varname, env[-2])
    # Look to see if found in an earlier call to env_lookup
    elif varname in fun_to_import:
        return fun_to_import[varname]
    # Look in user-defined directories for function m-files
    else:
        func = util.Walk(userfuns, 1, varname + '.m', 0)
        if func:
            return ('user_function',func)
        else:
            #func = util.Walk(matfuns, 1, varname + '.m', 0)
            func = 1
            if func:
                return ('matlab_function',func)
            else:
                return ('undefined','')

        

# Translates common functions in MATLAB to their python equivalents
def interpret_functions (fname, args, env):

    if args:
        fargs = [interpret_exp(x,env) + ',' for x in args]
        fargs = ''.join(fargs)
        fargs = string.rstrip(fargs,',')

    # Iterate through function names and make adjustments
    # Minor adjustments, mostly on function name or input
    if fname == 'zeros':
        return fname + '((' + interpret_exp(fargs, env) + '))'
    elif fname == 'ones':
        return fname + '((' + interpret_exp(fargs, env) + '))'
    elif fname == 'mod' or fname == 'rem':
        return (interpret_exp(args[0],env) + ' % ' + interpret_exp(args[1],env))
    elif fname == 'strcat':
        out = ("''.join([" + fargs + "])")
        env_update(out,'string','variable',env)
        return ("''.join([" + fargs + "])")
    elif fname == 'strcmp':
        return (interpret_exp(args[0],env) + ' == ' + interpret_exp(args[1],env))
    elif fname == 'eig':
        return 'reversed(linalg.eig(' + fargs + '))'
    elif fname == 'rethrow' or fname == 'throw':
        return 'raise ' + fargs 
    elif fname == 'repmat':
        return ('tile(' + interpret_exp(args[0], env) + '(' + \
               interpret_exp(args[1], env) + ',' + interpret_exp(args[2],env) +\
                '))')
    elif fname == 'sortrows':
        return ('argsort(' + interpret_exp(args[0], env) + '[:,' + \
                interpret_exp(args[1],env) + '])')

    # Keyword functions handled
    elif fname == 'clear':
        return ('# "clear(' + fargs + ')" Generally one does not destroy variables explicitly\n' + \
               '# in Python. The following variables were not destroyed:\n' + \
               '# ' +  fargs)
    elif fname == 'clc':
        return 'os.system(\'cls\')'
    elif fname == 'close':
        if args:
            return fname + '(' + fargs + ')'
        else:
            return fname + '()'
    elif fname == 'break':
        return fname
    elif fname == 'continue':
        return fname
    elif fname == 'dir':
        ls = os.getcwd()
        if 'glob' not in fun_to_import:
            fun_to_import['glob'] = ('python_module',['glob'])
        return 'glob.glob("' + string.replace(ls,'\\','\\\\\\\\') + '\\\\\\\\" + ' + fargs + ')'

    # Functions whose translation hinges more on numbers of arguments
    # and the like
    elif fname == 'size':
        numargs = len(args)
        if numargs == 2:
            return (interpret_exp(args[0],env) + '.shape(' + \
                    interpret_exp(args[1],env) + '-1)')
        else:
            return ('shape(' + fargs + ')')
    elif fname == 'min' or fname == 'max':
        numargs = len(args)
        base = '.' + fname + '(0)'
        if numargs == 1:
            out = fargs + base
            out = string.replace(out,base + base,'.' + fname + '()')
        elif numargs == 2:
            out = fname + 'imum(' + fargs + ')'
        elif numargs == 3:
            out = fargs + '.' + fname + '(1)'
        else:
            out = fname + '(' + fargs + ')'
        return out
    elif fname == 'cat':
        dim = interpret_exp(args[0],env)
        a = interpret_exp(args[1],env)
        b = interpret_exp(args[2],env)
        if dim == '2':
            return ('concatenate((' + a + ',' + b + '),1)')
        else:
            return ('concatenate((' + a + ',' + b + '))')
    elif fname == 'fclose':
        out = ''
        if not args:
            out += ('\n### There is no Python clone for \'fclose() ###\n')
        elif fargs == ' all ':
            out += ('\n### There is no Python clone for \'fclose(\'all\') ###\n')
        else:
            for arg in args:
                out += interpret_exp(arg, env) + '.close()\n'
        return out
    elif fname == 'regexp':
        out = 're.search(' + interpret_exp(args[1],env) + ',' + interpret_exp(args[0],env) + ').start()'
        return out

# Exceptions to handle common problems
class GenError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)



# Test Cases for the interpreter

input1 = """
%.........Script for converting WV DN's to radiance for all images.........
%Author: James Bramante
%Date: 20/12/2010

close all;
clear all;
clc;

%Define directories for input and output images, if different, the input
%image file extension, and a regular expression for finding the input
%images
path = 'E:\\raw\\vietnam\Danang\satellite\\052440347010_01\\052440347010_01_P001_MUL\\';
outpath = 'D:\documents\jimmy\matlab\imageVietnam\';
filext = '.TIF';
regex = ('R[1-7]C[1-3]');

%Create a list of input filenames and iterate through them, converting each
%pixel from digital number expression to absolute radiance (W/(m^2*nm*sr))
cd(path);
list = dir('*.TIF');
for i = 1 : length(list)
    
%     %Load image file and parse filename for output
%     filename = fullfile(path,list(i).name);
%     image = imread(filename);
%     [pathstr, name, ext, versn] = fileparts(filename);
%     ind = regexp(name,regex);
%     [x y z] = size(image);
%     close all;
%     
%     %Keep image as one whole and convert to radiance values
%     name = name(ind:ind+3);
%     image = double(image);
%     image = wvDN2Rad(image);
%     save(fullfile(outpath, name), 'image');
    
    %Split each image in half and convert to radiance values
    image = image(1:ceil(x/2),:,:);
    name1 = strcat(name(ind:ind+3),'upper.mat');
    image = double(image);
    image = wvDN2Rad(image);
    save (fullfile(outpath,name1),'image');
    clear name1 image;
    image = imread(filename);
    close all;
    image = image(ceil(x/2)+1:x,:,:);
    name2 = strcat(name(ind:ind+3),'lower.mat');
    image = double(image);
    image = wvDN2Rad(image);
    save (fullfile(outpath,name2),'image');
    clear name2 image;
end"""

print('Results of test 1 (Basic file and command flow operations):')
test_output = rewrite(input1)
print(test_output)
print('\n')


