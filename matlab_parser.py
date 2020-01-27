#Parser for Matlab-to-python interpreter
import ply.yacc as yacc
import ply.lex as lex
import matlab_lexxer
from matlab_lexxer import tokens

start = 'mat'

# Relative precedence and associativity for expressions,
# especially binary operations
precedence = (
    ('left', 'TRANSPOSE','POWER','MPOWER'),
    ('left', 'NOT'),
    ('left', 'TIMES','DIVIDE','MTIMES','MDIVIDE','BACKSLASH'),
    ('left', 'PLUS','MINUS'),
    ('left', 'COLON'),
    ('left', 'LT','LE','GT','GE','EQUALEQUAL','NOTEQUAL'),
    ('left', 'ELAND'),
    ('left', 'ELOR'),
    ('left', 'ANDAND'),
    ('left', 'OROR')
    )
    

# Parsing definitions to start parsing of matlab files
def p_mat (p):                  # Basic element driver
    'mat : element mat'
    p[0] = [p[1]] + p[2]
def p_mat_empty (p):
    'mat : '
    p[0] = []

# Definitions for base matlab elements
def p_element_compoundstmt (p): # Two options to start:
    'element : compoundstmt'    # list of statements OR a function definition
    p[0] = ('compoundstmt',p[1])
def p_element_function (p):
    'element : FUNCTION IDENTIFIER EQUAL IDENTIFIER LPAREN optargs RPAREN compoundstmt END'
    p[0] = ('function',p[2],p[4],p[6],p[8])

# Statement definitions
def p_compoundstmt_multiple (p):    # Basic unit of one or more statements or comments
    'compoundstmt : stmt SEMICOLON compoundstmt'
    p[0] = [p[1]] + p[3]
def p_compoundstmt_multiple_alt (p):
    'compoundstmt : stmt compoundstmt'
    p[0] = [p[1]] + p[2]
def p_compoundstmt_comment (p):
    'compoundstmt : COMMENT compoundstmt'
    p[0] = [('comment',p[1])] + p[2]
def p_compoundstmt_none (p):
    'compoundstmt : '
    p[0] = []
def p_stmt_if (p):                  # Start of concrete statement rules
    'stmt : IF exp compoundstmt END'
    p[0] = ('if',p[2],p[3])
def p_stmt_if_else (p):
    'stmt : IF exp compoundstmt ELSE compoundstmt END'
    p[0] = ('if-then-else',p[2],p[3],p[5])
def p_stmt_switchclause (p):          # Switch-clause construction
    'stmt : SWITCH exp multiclause END'
    p[0] = ('switch',p[2],p[3])
def p_stmt_trycatch (p):            # Try-catch exception handling clauses
    'stmt : TRY compoundstmt multiclause END'
    p[0] = ('try',p[2],p[3])
def p_stmt_for (p):
    'stmt : FOR range compoundstmt END'
    p[0] = ('for',p[2],p[3])
def p_stmt_while (p):
    'stmt : WHILE exp compoundstmt END'
    p[0] = ('while',p[2],p[3])
def p_stmt_assign (p):
    'stmt : IDENTIFIER EQUAL exp'
    p[0] = ('assign',p[1],p[3])
def p_stmt_assign_multiple (p):
    'stmt : matrix EQUAL exp'
    p[0] = ('multi-assign',p[1],p[3])
def p_stmt_return (p):
    'stmt : RETURN exp'
    p[0] = ('return',p[2])
def p_stmt_keycall (p):             # Allows for keyword functions
    'stmt : keycall'
    p[0] = p[1]
def p_stmt_structcall (p):          # Struct field indexing
    'stmt : IDENTIFIER PERIOD IDENTIFIER'
    p[0] = ('structcall',p[1],p[3])
def p_stmt_exp (p):                 # Allows incorporation of expressions
    'stmt : exp'
    p[0] = ('exp',p[1])


# Multiple clause constructions used in try and switch clauses
def p_multiclause_multiple (p):
    'multiclause : clause multiclause'
    p[0] = [p[1]] + p[2]
def p_multiclause_none (p):
    'multiclause : '
    p[0] = []
def p_clause_case (p):
    'clause : CASE exp compoundstmt'
    p[0] = ('case',p[2],p[3])
def p_clause_otherwise (p):
    'clause : OTHERWISE compoundstmt'
    p[0] = ('otherwise',[],p[2])
def p_clause_catch_arg (p):
    'clause : CATCH IDENTIFIER compoundstmt'
    p[0] = ('catch',p[2],p[3])
def p_clause_catch_noarg (p):
    'clause : CATCH compoundstmt'
    p[0] = ('catch', [], p[2])

    
# Special statement clause, mainly for FOR loops
def p_range_tofrom (p):
    'range : IDENTIFIER EQUAL exp COLON exp'
    p[0] = ('for_range',p[1],p[3],p[5])
def p_range_tostepfrom (p):
    'range : IDENTIFIER EQUAL exp COLON exp COLON exp'
    p[0] = ('for_steppedrange',p[1],p[3],p[5],p[7])

# Special keyword function calls requiring custom rules
def p_keycall_clc (p):
    'keycall : CLC'
    p[0] = ('keycall','clc',[])
def p_keycall_close (p):
    'keycall : CLOSE optvars'
    p[0] = ('keycall','close',p[2])
def p_keycall_clear (p):
    'keycall : CLEAR optvars'
    p[0] = ('keycall','clear',p[2])
def p_keycall_break (p):
    'keycall : BREAK'
    p[0] = ('keycall','break',[])
def p_keycall_continue (p):
    'keycall : CONTINUE'
    p[0] = ('keycall','continue',[])
def p_optvars_multiple (p):
    'optvars : exp optvars'
    p[0] = [p[1]] + p[2]
def p_optvars_single (p):
    'optvars : exp'
    p[0] = [p[1]]

# Number definitions
def p_number_integer (p):
    'number : INTEGER'
    p[0] = ('integer', p[1])
def p_number_float (p):
    'number : FLOAT'
    p[0] = ('float', p[1])

# Basic expression definitions
def p_exp_identifier (p):
    'exp : IDENTIFIER'
    p[0] = ('identifier',p[1])
def p_exp_string (p):
    'exp : STRING'
    p[0] = ('string', p[1])
def p_exp_directory (p):        # For strings containing filepaths
    'exp : DIRECTORY'
    p[0] = ('directory',p[1])
def p_exp_transpose (p):
    'exp : exp TRANSPOSE'
    p[0] = ('transpose',p[1],p[2])
def p_exp_parens (p):
    'exp : LPAREN exp RPAREN'
    p[0] = ('parens',p[2])
def p_exp_function (p):         # Function calls
    'exp : IDENTIFIER LPAREN optargs RPAREN'
    p[0] = ('call',p[1],p[3])
def p_exp_number (p):
    'exp : number'
    p[0] = p[1]
def p_exp_keyword (p):
    'exp : keyword'
    p[0] = p[1]

# Special keywords with simple translations
def p_keyword_all (p):
    'keyword : ALL'
    p[0] = ('keyword', 'all')
def p_keyword_not (p):
    'keyword : NOT'
    p[0] = ('keyword', 'not')
def p_keyword_true (p):
    'keyword : TRUE'
    p[0] = ('keyword', 'true')
def p_keyword_false (p):
    'keyword : FALSE'
    p[0] = ('keyword', 'false')
def p_keyword_colon (p):
    'keyword : COLON'
    p[0] = ('keyword',':')

# Special rules for arguments to functions and indexing
def p_optargs_single (p):
    'optargs : args'
    p[0] = p[1]
def p_optargs_empty (p):
    'optargs : '
    p[0] = []
def p_args (p):
    'args : exp COMMA args'
    p[0] = [p[1]] + p[3]
def p_args_singleton (p):
    'args : exp'
    p[0] = [p[1]]    

# Binary relational operation definitions
def p_exp_binop_elor (p):           # Element-wise
    'exp : exp ELOR exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_eland (p):          # Element-wise
    'exp : exp ELAND exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_oror (p):
    'exp : exp OROR exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_andand (p):
    'exp : exp ANDAND exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_equalequal (p):
    'exp : exp EQUALEQUAL exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_notequal (p):
    'exp : exp NOTEQUAL exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_lessthan (p):
    'exp : exp LT exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_greaterthan (p):
    'exp : exp GT exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_lessequal (p):
    'exp : exp LE exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_greaterequal (p):
    'exp : exp GE exp'
    p[0] = ('binop', p[1],p[2],p[3])

# Binary arithmetic operation definitions
def p_exp_binop_mpower (p):
    'exp : exp MPOWER exp'
    p[0] = ('binop',p[1],p[2],p[3])
def p_exp_binop_power (p):          # Element-wise
    'exp : exp POWER exp'
    p[0] = ('binop',p[1],p[2],p[3])
def p_exp_binop_mtimes (p):
    'exp : exp MTIMES exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_mdivide (p):
    'exp : exp MDIVIDE exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_times (p):          # Element-wise
    'exp : exp TIMES exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_divide (p):         # Element-wise
    'exp : exp DIVIDE exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_backslash (p):
    'exp : exp BACKSLASH exp'
    p[0] = ('binop',p[1],p[2],p[3])
def p_exp_binop_plus (p):           # Element-wise
    'exp : exp PLUS exp'
    p[0] = ('binop', p[1],p[2],p[3])
def p_exp_binop_minus (p):          # Element-wise
    'exp : exp MINUS exp'
    p[0] = ('binop', p[1],p[2],p[3])


# Expressions used primarily for matrix construction and indexing
def p_exp_steppedrange (p):
    'exp : exp COLON exp COLON exp'
    p[0] = ('steppedrange',p[1],p[3],p[5])
def p_exp_range (p):
    'exp : exp COLON exp'
    p[0] = ('range',p[1],p[3])
def p_exp_matrix (p):
    'exp : matrix'
    p[0] = p[1]
def p_matrix (p):
    'matrix : LBRACKET explist RBRACKET'
    p[0] = ('matrix', p[2])
#def p_exp_indexcall (p):
#    'exp : IDENTIFIER LPAREN args RPAREN'
#    p[0] = ('index',p[1],p[3])
def p_explist_single (p):
    'explist : exp'
    p[0] = [p[1]]
def p_explist_multiple (p):
    'explist : explist exp'
    p[0] = p[1] + [p[2]]
def p_explist_multiple_comma (p):
    'explist : explist COMMA exp'
    p[0] = p[1] + [p[3]]
def p_explist_newrow (p):
    'explist : explist SEMICOLON explist'
    p[0] = [('row',p[1],p[3])]

# Expressions for cell arrays
def p_exp_cellindexcall (p):
    'exp : IDENTIFIER LBRACE args RBRACE'
    p[0] = ('cellindex',p[1],p[3])


# Build the parser

lexxer = lex.lex(module=matlab_lexxer)
parser = yacc.yacc()

def test_parser(input_string):  # invokes your parser to get a tree!
    lexxer.input(input_string) 
    parse_tree = parser.parse(input_string,lexer=lexxer) 
    return parse_tree    
    
# Test cases
#input1 = r""" directory_name = 'C:\test_directory\'; """

#output1 = [('compoundstmt',[('assign','directory_name',('directory',\
#           'C:\\test_directory\\'))])]

#print 'Results of test 1 (directory declaration):'
#print test_parser(input1) == output1
#print '\n'

#input2 = r"""
#%Here's a comment
#x = [1 2 3; 4, 5, 6; 7.4 8 9];
#for a = 4 : 500
#    y = x(2,3);
#end"""

#output2 = [('compoundstmt',[('comment',"Here's a comment"),('assign','x',\
#           ('matrix',[('row',[('integer',1),('integer',2),('integer',3)],\
#           [('row',[('integer',4),('integer',5),('integer',6)],[('float',7.4),('integer',8),('integer',9)])])])),('for',\
#           ('for_range','a',('integer',4),('integer',500)),[('assign','y',\
#           ('call','x',[('integer',2),('integer',3)]))])])]

#print 'Results of test 2 (basic statements and matrix calls):'
#print test_parser(input2) == output2
#print '\n'

#input3 = """
#clc; close all; fclose('all')
#x = [4 5 6; 4.5 2.69 3.2; 7. 8.9 .2];
#try
#    x = sum(sum(x .* 8));
#catch exception
#    if (exception ~= MException('MATLAB:badsubscript','Index exceeds matrix dimensions'))
#        disp(exception);
#    else
#        rethrow(exception);
#    end
#end"""

#output3 = [('compoundstmt',[('keycall','clc',[]),\
#                            ('keycall','close',[('keyword','all')]),\
#                            ('exp',('call','fclose',[('string','all')])),\
#                            ('assign','x',('matrix',[('row',[('integer',4),('integer',5),('integer',6)],[('row',[('float',4.5),('float',2.69),('float',3.2)],[('integer',7),('float',8.9),('float',0.2)])])])),\
#                            ('try',[('assign','x',('call','sum',[('call','sum',[('binop',('identifier','x'),'.*',('integer',8))])]))],\
#                             [('catch','exception',[('if-then-else',('parens',('binop',('identifier','exception'),'~=',('call','MException',[('string','MATLAB:badsubscript'),('string','Index exceeds matrix dimensions')]))),\
#                                                                                    [('exp',('call','disp',[('identifier','exception')]))],\
#                                                                                    [('exp',('call','rethrow',[('identifier','exception')]))])])])\
#                            ])]

#print 'Results of test 3 (try-catch and if-then-else clauses):'
#print test_parser(input3) == output3
#print '\n'
