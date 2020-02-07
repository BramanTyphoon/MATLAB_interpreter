# MATLAB_interpreter

## Motivation
Over the past decade, the functionality of open access Python packages have accelerated rapidly, repicating nearly all of the functionality of proprietary scientific software like MATLAB, with similar stability. This project was initiated to help scientists using MATLAB port their code to Python.

## Execution
Clone the app to your local machine and test the parser using:
```
pip install -r required_packages.txt
python test_driver.py
```
If running matlab_rewrite.py directly, make sure to change the hard-coded user input directory paths

N.B. This parser works best with a particular coding style (i.e. my MATLAB style) and may produce erroneous results or throw errors for coding styles that vary widely from that.

## Files
* [matlab_lexxer.py](matlab_lexxer.py) - A lexxer module that tokenizes input MATLAB scripts
* [matlab_parser.py](matlab_parser.py) - A parser module that creates a parse tree of tokens from the lexxer
* [matlab_rewrite.py](matlab_rewrite.py) - Interprets the parser tree from the parser to either write the MATLAB script in Python or just evaluate it (run it directly). Is currently set up to run the parser in every '.m' file within a directory tree
* [test_driver.py](test_driver.py) - Script used to import and test the parser at the rewrite level (tests for the lexxer and parser can be found at the ends of those files)
* [io_util.py](io_util.py) - A module of utility functions. Currently only has code to walk through a directory tree to apply matlab_rewrite file-by-file
* [parsetab.py](parsetab.py) and [parser.out](parser.out) - Files automatically generated by the parser pipeline
* [required_packages.txt](required_packages.txt) - Text file listing required packages to install before running
* [convertDn2RadAll.m](convertDn2RadAll.m) - Example, not great MATLAB script for testing

## Built with
* This project was written for Python 2.7
* [PLY](https://www.dabeaz.com/ply/) - An implementation of lex and yacc parsing tools in Python

## Authors
* James Bramante - initial work - [BramanTyphoon](https://github.com/BramanTyphoon)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments
* The file [io_util.py](io_util.py) uses code written by [Robin Parmar](http://code.activestate.com/recipes/users/99666/)
* This project is based on the final project (writing a web browser) in a (now defunct) [Udacity course](https://classroom.udacity.com/courses/cs262)

# TODO

* Saving and loading .mat files and using the functions 'load' and 'save'

* Regular expressions translation from MATLAB to Python

* Add/verify cell and struct functionality

* Screen variable and function names for reserved words and automatically change them



