# Lexxer for Matlab-to-python interpreter
import ply.lex as lex

# Exhaustive list of tokens
tokens = (
    'COMMENT',      # %yadda yadda etc
    'DIRECTORY',    # 'C:\directory\'
    'STRING',       # 'words'
    'FLOAT',        # 0.48
    'INTEGER',      # 0-9+
    'ANDAND',       # &&
    'OROR',         # ||
    'ELAND',        # &
    'ELOR',         # |
    'EQUALEQUAL',   # ==
    'NOTEQUAL',     # ~=
    'GE',           # >=
    'GT',           # >
    'LE',           # <=
    'LT',           # <
    'TRANSPOSE',    # '
    'MPOWER',       # ^
    'POWER',        # .^
    'MDIVIDE',      # /
    'MTIMES',       # *
    'DIVIDE',       # ./
    'TIMES',        # .*
    'BACKSLASH',    # \
    'MINUS',        # -
    'PLUS',         # +
    'NOT',          # ~
    'EQUAL',        # =
    'LPAREN',       # (
    'RPAREN',       # )
    'LBRACKET',     # [
    'RBRACKET',     # ]
    'LBRACE',       # {
    'RBRACE',       # }
    'SEMICOLON',    # ;
    'COLON',        # :
    'COMMA',        # ,
    'PERIOD',       # .
    'TRY',          # try
    'CATCH',        # catch
    'SWITCH',       # switch-case construction
    'CASE',         # switch-case construction
    'OTHERWISE',    # switch-case construction
    'IF',           # if
    'ELSE',         # else
    'END',          # end
    'FUNCTION',     # function
    'FOR',          # for
    'WHILE',        # while
    'BREAK',        # break
    'CONTINUE',     # continue
    'TRUE',         # true
    'FALSE',        # false
    'ALL',          # all
    'RETURN',       # return
    'CLEAR',        # clear
    'CLC',          # clc
    'CLOSE',        # close
#    'NEWLINE',     # \n
    'IDENTIFIER'   # function calls and variable names
    )

## States accessible outside of 'INITIAL'
## Only use if ignoring comments completely, as in compiler/execution
#states = [('comment','exclusive')]

## State transition handlers
#def t_comment (t):
#    r'\%'
#    t.lexer.begin('comment')
#    pass
#def t_comment_end (t):
#    r'\n'
#    t.lexer.begin('INITIAL')
#    pass
#def t_comment_error (t):
#    t.lexer.skip(1)
#    pass

# Token definitions using regular expressions
def t_COMMENT (t):
    r'%.*'
    t.type = 'COMMENT'
    t.value = t.value[1:]
    return t
def t_DIRECTORY (t):
    r"""'[A-Za-z]:\\[^']*'"""
    t.type = 'DIRECTORY'
    t.value = t.value[1:-1]
    return t
def t_STRING (t):
    r"""'[^']*'"""
    t.type = 'STRING'
    t.value = t.value[1:-1]
    return t
def t_FLOAT (t):
    r'-?[0-9]*\.[0-9]+'
    t.type = 'FLOAT'
    t.value = float(t.value)
    return t
def t_INTEGER (t):
    r'-?[0-9]+(?:\.)?'
    t.type = 'INTEGER'
    t.value = int(t.value.rstrip('\.'))
    return t
def t_ANDAND (t):
    r'\&\&'
    t.type = 'ANDAND'
    return t
def t_OROR (t):
    r'\|\|'
    t.type = 'OROR'
    return t
def t_ELAND (t):
    r'\&'
    t.type = 'ELAND'
    return t
def t_ELOR (t):
    r'\|'
    t.type = 'ELOR'
    return t
def t_EQUALEQUAL (t):
    r'\=\='
    t.type = 'EQUALEQUAL'
    return t
def t_NOTEQUAL (t):
    r'\~\='
    t.type = 'NOTEQUAL'
    return t
def t_GREATEREQUAL (t):
    r'\>\='
    t.type = 'GE'
    return t
def t_GREATERTHAN (t):
    r'\>'
    t.type = 'GT'
    return t
def t_LESSEREQUAL (t):
    r'\<\='
    t.type = 'LE'
    return t
def t_LESSERTHAN (t):
    r'\<'
    t.type = 'LT'
    return t
def t_TRANSPOSE (t):
    r'\''
    t.type = 'TRANSPOSE'
    return t
def t_POWER (t):
    r'\.\^'
    t.type = 'POWER'
    return t
def t_MPOWER (t):
    r'\^'
    t.type = 'MPOWER'
    return t
def t_MDIVIDE (t):
    r'\/'
    t.type = 'MDIVIDE'
    return t
def t_MTIMES (t):
    r'\*'
    t.type = 'MTIMES'
    return t
def t_DIVIDE (t):
    r'\.\/'
    t.type = 'DIVIDE'
    return t
def t_TIMES (t):
    r'\.\*'
    t.type = 'TIMES'
    return t
def t_BACKSLASH (t):
    r'\\'
    t.type = 'BACKSLASH'
    return t
def t_MINUS (t):
    r'\-'
    t.type = 'MINUS'
    return t
def t_PLUS (t):
    r'\+'
    t.type = 'PLUS'
    return t
def t_NOT (t):
    r'\~'
    t.type = 'NOT'
    return t
def t_EQUAL (t):
    r'='
    t.type = 'EQUAL'
    return t
def t_LPAREN (t):
    r'\('
    t.type = 'LPAREN'
    return t
def t_RPAREN (t):
    r'\)'
    t.type = 'RPAREN'
    return t
def t_LBRACKET (t):
    r'\['
    t.type = 'LBRACKET'
    return t
def t_RBRACKET (t):
    r'\]'
    t.type = 'RBRACKET'
    return t
def t_LBRACE (t):
    r'\{'
    t.type = 'LBRACE'
    return t
def t_RBRACE (t):
    r'\}'
    t.type = 'RBRACE'
    return t
def t_SEMICOLON (t):
    r'\;'
    t.type = 'SEMICOLON'
    return t
def t_COLON (t):
    r'\:'
    t.type = 'COLON'
    return t
def t_COMMA (t):
    r'\,'
    t.type = 'COMMA'
    return t
def t_PERIOD (t):
    r'\.'
    t.type = 'PERIOD'
    return t
def t_TRY (t):
    r'try'
    t.type = 'TRY'
    return t
def t_CATCH (t):
    r'catch'
    t.type = 'CATCH'
    return t
def t_SWITCH (t):
    r'switch'
    t.type = 'SWITCH'
    return t
def t_CASE (t):
    r'case'
    t.type = 'CASE'
    return t
def t_OTHERWISE (t):
    r'otherwise'
    t.type = 'OTHERWISE'
    return t
def t_IF (t):
    r'if'
    t.type = 'IF'
    return t
def t_ELSE (t):
    r'else'
    t.type = 'ELSE'
    return t
def t_END (t):
    r'end'
    t.type = 'END'
    return t
def t_FUNCTION (t):
    r'function'
    t.type = 'FUNCTION'
    return t
def t_FOR (t):
    r'for'
    t.type = 'FOR'
    return t
def t_WHILE (t):
    r'while'
    t.type = 'WHILE'
    return t
def t_BREAK (t):
    r'break'
    t.type = 'BREAK'
    return t
def t_CONTINUE (t):
    r'continue'
    t.type = 'CONTINUE'
    return t
def t_TRUE (t):
    r'true'
    t.type = 'TRUE'
    return t
def t_FALSE (t):
    r'false'
    t.type = 'FALSE'
    return t
def t_ALL (t):
    r'all'
    t.type = 'ALL'
    return t
def t_RETURN (t):
    r'return'
    t.type = 'RETURN'
    return t
def t_CLEAR (t):
    r'clear'
    t.type = 'CLEAR'
    return t
def t_CLC (t):
    r'clc'
    t.type = 'CLC'
    return t
def t_CLOSE (t):
    r'close'
    t.type = 'CLOSE'
    return t
def t_IDENTIFIER (t):
    r'[A-Za-z][A-Za-z0-9_]*'
    return t


# Lexxer should ignore whitespace in comments and otherwise
t_ignore = ' \t\v\r' # whitespace 
#t_comment_ignore = ' \t\v\r'    # whitespace

# Count the lines as lexxer moves through
def t_newline(t):
        r'\n'
        t.lexer.lineno += 1

# Skip errors and report to user
def t_error(t):
        print("Matlab Lexer: Illegal character " + t.value[0])
        t.lexer.skip(1)

# Code for test cases and general testing

lexer = lex.lex()       # Build lexxer 

def test_lexer(input_string):
  lexer.input(input_string) # Input string to lexxer to process
  result = [ ] 
  while True:               # Move through token list
    tok = lexer.token()
    if not tok: break       # When token list is empty, stop
    result = result + [tok.type]
  return result

#input1 = """ - ~  && () * , / ; { || } + [] < <= = ~= == > >= else false function
#if return true .* ./ . switch case otherwise try catch"""

#output1 = ['MINUS', 'NOT', 'ANDAND', 'LPAREN', 'RPAREN', 'MTIMES', 'COMMA',
#'MDIVIDE', 'SEMICOLON', 'LBRACE', 'OROR', 'RBRACE', 'PLUS', 'LBRACKET',
#'RBRACKET', 'LT', 'LE', 'EQUAL', 'NOTEQUAL', 'EQUALEQUAL', 'GT', 'GE',
#'ELSE', 'FALSE', 'FUNCTION', 'IF', 'RETURN', 'TRUE', 'TIMES', 'DIVIDE',
#'PERIOD', 'SWITCH', 'CASE', 'OTHERWISE', 'TRY', 'CATCH']

#print 'Results of test 1 (operators and basics):'
#print test_lexer(input1) == output1
#print '\n'

##Only use test case 2 when working with states
#input2 = """
#if % else mystery  
#= =
#true % false 
#return"""

#output2 = ['IF', 'EQUAL', 'EQUAL', 'TRUE', 'RETURN']

#print 'Results of test 2 (if, equals, booleans, return, and comments):'
#print test_lexer(input2) == output2
#print '\n'

#input3 = """
#-456.4 89 .3 0.3
#var2 varname_alpha hello__
#'\this is a string\'
#"""

#output3 = ['FLOAT', 'INTEGER', 'FLOAT', 'FLOAT', 'IDENTIFIER', 'IDENTIFIER',
#           'IDENTIFIER', 'STRING']

#print 'Results of test 3 (floats, integers, identifiers, and strings):'
#print test_lexer(input3)
#print test_lexer(input3) == output3
#print '\n'

#input4 = r""" directory_name = 'C:\test_directory\' """

#output4 = ['IDENTIFIER', 'EQUAL', 'DIRECTORY']

#print 'Results of test 4 (directories):'
#print test_lexer(input4)
#print test_lexer(input4) == output4
#print '\n'

#Only use test case 5 when working with comment values
#input5 = """
#if % else: mystery  
#= =
#true % false 
#return"""

#output5 = ['IF', 'COMMENT', 'EQUAL', 'EQUAL', 'TRUE', 'COMMENT', 'RETURN']

#print 'Results of test 5 (comments):'
#print test_lexer(input5) == output5
#print '\n'
