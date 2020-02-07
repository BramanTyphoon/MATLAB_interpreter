# Driver for matlab interpreter code
import matlab_lexxer as mat
import matlab_parser as par
import matlab_rewrite as interp
import sys

# Pulls out the lexer and parser
matter = mat.lexer
patter = par.parser

# Define varables for opening and processing matlab files
fname = 'convertDn2RadAll.m'

with open(fname,'r') as fil:
    instring = fil.read()
#print instring
#print '\n'

# Test that the lexer is in working order
def test_lexer(input_string):
  matter.input(input_string) # Input string to lexxer to process
  result = [ ] 
  while True:               # Move through token list
    tok = mat.lexer.token()
    if not tok: break       # When token list is empty, stop
    result = result + [tok.type]
  return result

# Test that the parser is working properly
def test_parser(input_string):  # invokes your parser to get a tree!
    matter.input(input_string) 
    parse_tree = patter.parse(input_string,lexer=matter) 
    return parse_tree

lexxed = test_lexer(instring)
#print (lexxed)

parsed = test_parser(instring)
#print (parsed)

# Try to open and read Matlab code
infile = fname
outfile = 'convertDn2RadAll.py'

with open(infile, 'r') as rea:
    instring = rea.read()

output_text = interp.rewrite(instring)
#print(output_text)

# Write all of the text to a text file
with open(outfile,'w') as wri:
    wri.write(output_text)
    print('Parsed MATLAB file successfully written to: ' + outfile)