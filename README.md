# Simple command line PMPV calculator in Python
Author: Robert (Nayan) Sawyer\
Date: Jan 24 2024

### Description
A simple command line calculator that supports addition, 
subtraction, variables, and parentheses. This program was 
written for a homework assignment for COS 301: Programming 
Languages at the University of Maine taught by Sudarshan S. 
Chawathe.

### Language specification
This assignment had intentionally vague instructions, however, 
I wrote my code to the following specifications:
- The code accepts mathematical expressions that include plus, 
minus, variables, and parentheses (PMPV)
- Variable names must meet python's criteria of letters, 
underscores, and numbers, so long as they don't start with a 
number.
- Numbers must be positive or negative integers
- Negative integers must be preceded by a space ' ' or an open 
paranthesis '('
- Consecutive operators, dangling operators at the beginning or 
end of an expression, undefined variables, and mismatched 
parentheses are invalid syntax
#### Terminals and Backus-Naur Form
Terminals are numbers and identifiers (variable names), and 
['=', '+', '-', '(', ')']
```
BNF:
<program> ::= <assignment> | <expression>
<assignment> ::= identifier = <expression>
<expression> ::= <expression> + <term> | 
                 <expression> - <term> | 
                 <term>
<term> ::= (<expression>) |  identifier  |  number
```

### Input examples
```
input                                   output
3 + 5 - -2 - 2                          8
x = 3 + 5 - -2 - 2
y = x - (x - 2)
y                                       2
ans = (17 - (5 - 20)) - (1 - 11)
ans                                     42

ans = ans - (-42 - ans)
ans                                     126
(17-(5-20))-(1-11)                      42
```

### How to run
You can run the program interactively with the command \
`python pmpv.py` \
Alternatively, you can pipe files in and out.
On linux that can be acheived with the arrow operator\
`python pmpv.py < in.txt` or `python pmpv.py < in.txt > out.txt`\
On windows output redirection works the same way, but you need to 
use piping for input redirection. It is the same in essence, but a 
little more clunky\
`Get-Content in.txt | python pmpv.py > out.txt`

### Dependencies
This program uses python's built-in re module (regex), and there 
are no external dependencies. The test file uses unittest.

### Diagnostics
The program sends error messages to stderr, so you can redirect 
that away if you don't want those messages.

There is a testing file inluded `test_pmpv.py` that can be run 
with the command `python test_pmpv.py` that will run a sereices 
of unit and integration tests. unittest was used as the testing 
library  of choice. The selection of tests is not complete, but 
was enought to verify that the program met the requirements of the 
assignment.

### Bugs and limitations
Typical behaviour is to ignore invalid inputs and send a warning 
to stderr. It is possible for the program to crash or throw an 
exception, but I have tested it extensively, and crashes during 
normal use are *hopefully* rare.

One issue with the program is that behaviour when given invalid 
input undefined. Some inputs will be ignored, but there may be 
some cases where the input is invalid, but the program interprets 
it anyway, and may give a mathematically incorrect result.


### Sources used:
- https://regexr.com/
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions/Cheatsheet
- https://www.delftstack.com/howto/python/python-print-to-stderr/
- https://stlab.cc/legacy/how-to-write-a-simple-lexical-analyzer-or-parser.html
- https://www.tutorialsteacher.com/python/public-private-protected-modifiers
- https://stackoverflow.com/questions/1155617/count-the-number-of-occurrences-of-a-character-in-a-string
- https://stackoverflow.com/questions/152580/whats-the-canonical-way-to-check-for-type-in-python
- https://www.geeksforgeeks.org/python-method-overloading/
- https://docs.python.org/3/library/functions.html#iter (for info on iter)
- https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner
- https://stackoverflow.com/questions/11447598/redirecting-standard-input-output-in-windows-powershell
- https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines?view=powershell-7.4
