# Driver for matlab interpreter code
import matlab_lexxer as mat
import matlab_parser as par
import matlab_rewrite as interp

# Pulls out the lexer and parser
matter = mat.lexer
patter = par.parser

# Define varables for opening and processing matlab files
fname = 'E:\\documents\\matlab\\convertDn2RadAll.m'

fil = open(fname,'r')
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
print lexxed

parsed = test_parser(instring)
print parsed

# Try to open and read Matlab code
infile = fname
outfile = 'E:\\documents\\matlab\\convertDn2RadAll.py'

try:
    rea = open(infile,'r')
    wri = open(outfile,'w')
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
except:
    print 'Unexpected error:', sys.exc_info()[0]
    raise

instring = rea.read()

output_text = interp.rewrite(instring)

# Write all of the text to a text file
wri.write(output_text)

# Close the files
rea.close()
wri.close()
