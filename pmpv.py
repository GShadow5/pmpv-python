"""
pmpv.py
Description: A simple command line calculator that supports addition, subtraction, variables, and parentheses
Author: Robert (Nayan) Sawyer
Date: 2024-01-24
Licence: MIT
Dependencies: Python's built-in re module, and two local modules: Variables.py and eprint.py
Comments: This program was written for a homework assignment for COS 301: Programming Languages at the University of Maine
"""

import re, sys

class Variables:
    ''' A singleton class that stores all variables in the program.
        This is a singleton so that we can access the variables from anywhere in the program.'''
    __variables = {}
    __instance = None

    def __init__(self):
        if Variables.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Variables.__instance = self

    @classmethod
    def get_instance(self):
        if Variables.__instance == None:
            Variables()
        return Variables.__instance
    
    def get(self, name):
        if name not in self.__variables:
            return None
        return self.__variables[name]
    def get_all(self):
        yield from self.__variables
    def contains(self, name):
        return name in self.__variables
    def set(self, name, value):
        self.__variables[name] = value
    def clear(self):
        self.__variables = {}
    def __str__(self):
        return str(self.__variables)
    def __repr__(self):
        return str(self.__variables)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

pmpv = {
    'number': r'(?:(?:^-)*|(?:(?<=[ \()])-))?[0-9]+',
    'identifier': r'[a-zA-Z]+',
    'plus': r'\+',
    'minus': r'\-',
    'left_paren': r'\(',
    'right_paren': r'\)',
    'equals': r'\=',
}
compound_pmpv = '|'.join(pmpv.values())

def tokenize(userInput):
    ''' Tokenize the user input into a list of tokens '''
    equals = userInput.count("=")
    # Check for parentheses mismatch
    if userInput.count("(") != userInput.count(")"):
        eprint("Invalid expression: mismatched parentheses")
        return None
    # Check for invalid assignment characters
    if userInput.count("=") > 1:
        eprint("Invalid expression: too many '='")
        return None
    # Use regex to tokenize the input
    tokens = re.findall(compound_pmpv, userInput)

    # Check that the tokens are valid
    for i,token in enumerate(tokens):
        # Check for valid assignment syntax
        if equals == 1 and i == 0:
            if not re.match(pmpv['identifier'], token) and \
                not tokens[i+1] == "=":
                eprint("Invalid expression: expected '='")
                return None
            continue
        # Replace variables with their values
        if re.match(pmpv['identifier'], token):
            var = Variables.get_instance().get(token)
            if var == None:
                eprint("Invalid expression: variable not defined")
                return None
            else:
                tokens[i] = var
        # Convert numbers to integers
        if re.match(pmpv['number'], token):
            tokens[i] = int(token)
    return tokens

def evaluate_tokens(tokens):
    ''' Evaluate the tokens into a single value '''
    left = None
    right = None
    operator = None
    i = 0

    def paren_recurse():
        ''' Recursively evaluate the parenthesized expression '''
        nonlocal i
        nonlocal tokens
        depth = 1
        # Check for empty parentheses
        if tokens[i+1] == ")":
            return None

        # Find the end of the parenthesized expression and count
        # the depth of the parentheses to catch nested parentheses
        depth = 1
        i += 1
        start = i
        while True:
            if i >= len(tokens):
                # Check for mismatched parentheses. This should never happen because we check for mismatched parentheses in tokenize()
                eprint("Invalid expression: mismatched parentheses")
                return None
            if tokens[i] == "(":
                depth += 1
            elif tokens[i] == ")":
                depth -= 1
            if depth == 0:
                break
            i += 1
        # Recursively evaluate the parenthesized expression
        return evaluate_tokens(tokens[start:i])

    # Check for empty expression
    if len(tokens) == 0:
        return None
    # Check for single value expression. Since we already converted variables to their values, this should only be a number
    if len(tokens) == 1:
        if type(tokens[0]) != int:
            eprint("Invalid expression: invlaid token" + str(tokens[0]) + type(tokens[0]))
            return None
        else:
            return tokens[0]

    # ~~ LEFT VALUE ~~
    # Handle variable assignment
    if type(tokens[i]) == str and re.match(pmpv['identifier'], tokens[0]):
        if tokens[1] != "=":
            eprint("Invalid expression: expected '='")
            return None
        Variables.get_instance().set(tokens[i], evaluate_tokens(tokens[2:]))
        return None
    # Another check for invalid syntax
    if tokens[i] in ["-", "+"]:
        eprint("Invalid expression")
        return None
    # If the left value is in parenthesis, recursively evaluate the parenthesized expression
    if tokens[i] == "(":
        left = paren_recurse()
    # Otherwise, just set the left value to the token
    else:
        left = tokens[i]
    i += 1
    # If the left value is the only value in the expression, return it 
    if i >= len(tokens):
        return left

    # ~~ OPERATOR VALUE ~~
    operator = tokens[i]
    # Make sure the operator is valid
    if operator not in ["-", "+"]:
        eprint("Invalid expression: expected operator")
        return None
    i += 1

    # ~~ RIGHT VALUE ~~
    # If the right value is in parenthesis, recursively evaluate the parenthesized expression
    if tokens[i] == "(":
        right = paren_recurse()
    # Another check for invalid syntax
    elif tokens[i] in ["-", "+"]:
        eprint("Invalid expression: expression cannot end with operator")
        return None
    # Otherwise, just set the right value to the token
    else:
        right = tokens[i]
    i += 1


    # Check that the left, right, and operator values are valid
    if left == None or right == None or operator == None:
        eprint("Invalid expression: invalid token")
        return None
    if type(left) != int or type(right) != int:
        eprint("Invalid expression: invalid token")
        return None
    if operator not in ["-", "+"]:
        eprint("Invalid expression: invalid token")
        return None

    # Calculate the sum of the expression
    sum = 0
    if operator == "+":
        sum = left + right
    elif operator == "-":
        sum = left - right
    else:
        eprint("Invalid expression: invalid operator")
        return None

    # If there are more tokens, recursively evaluate them
    if i <= len(tokens):
        sum = evaluate_tokens([sum] + tokens[i:])

    return sum

def main():
    ''' Main function to handle user input '''
    while True:
        try: # Handle EOF
            userInput = input("")
            tokens = tokenize(userInput) # Tokenize the input
            if tokens == None: # If the input is invalid
                continue
            tokens = evaluate_tokens(tokens) # Evaluate the tokens
            if tokens != None: # If the tokens are valid, print the result
                print(tokens)
            else:
                print("")

        except EOFError: # Gracefully exit on EOF
            break

if __name__ == '__main__':
    main()