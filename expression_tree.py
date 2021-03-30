""" 52093080 """
import re
import json
from ADT import tree_base
from ADT import stack

""" error classes """
# this lets me catch the exception, when looking for invalid expressions
# makes the validate function much more readable
# new criteria for invalid expressions can easily be added
class OperandsError(Exception):
    # something is wrong with the operands
    # i.e. operands are missing
    pass

class BracketsError(Exception):
    # something is wrong with the brackets
    # i.e. opened but not closed
    # missing pairs of brackets
    pass

class OperatorsError(Exception):
    # something is wrong with the operators
    # i.e. operator is missing
    # operator is places incorrectly
    pass

def miss_op(string:str):
    """ a function that matched patterns in the string, that make an expression invalid"""
    # stripping all whitespaces
    # so i dont have to deal with them when matching patterns
    for i in string:
        if i == " ":
            string.replace(" ","")

    # matching patterns using regex
    # it seems to be the easiest way to catch certain kinds of invalid expressions
    # the regex expressions are a pain to read tho
    # ( <number> ( && ) <number> ) kind os mistakes in next two lines
    p1 = re.compile("\([0-9]\(")
    p2 = re.compile("\)[0-9]\)")
    # ( <number> <operator> ) && ( <operator> <number> ) mistakes
    p3 = re.compile("\([0-9][\+\-\*\/]\)")
    p4 = re.compile("\([\+\-\*\/][0-9]\)")
    # ( <operator> <number> ( &&  ) <number> <operator> ) mistakes
    p5 = re.compile("\([\+\-\*\/][0-9]\(")
    p6 = re.compile("\)[0-9][\+\-\*\/]\)")

    # re.search returns None if nothing was found
    # otherwise it returns a regex object
    f1 = re.search(p1, string)
    f2 = re.search(p2, string)
    f3 = re.search(p3, string)
    f4 = re.search(p4, string)
    f5 = re.search(p5, string)
    f6 = re.search(p6, string)

    # checking if the the return from the match is None
    # if not a match was found and the expression is invalid
    # different cases for different kinds of invalid
    if f1 is not None or f2 is not None:
        raise OperatorsError("invalid expression: missing operator")
    elif f3 is not None or f4 is not None:
        raise OperandsError("invalid expression: missing operant")
    elif f5 is not None or f6 is not None:
        raise OperatorsError("invalid expression: elements in wrong order")
    else:
        pass

def num_brackets(string:str):
    """ there need to be twice as many brackets as operators """
    """ otherwise there is more than 1 operator in bracket pair """
    """ check after the closing of brackets is checked"""
    # unforunately has overlap with some of the regex cases
    brackets = [str(e) for e in string if e == "(" or e == ")"]
    operators = [str(e) for e in string if e == "+" or e == "-" or e == "*" or e == "/"]

    if len(brackets) != 2*len(operators):
        # raise operands error if there are the wrong number of brackets/operators
        raise OperandsError("invalid expression: wrong number of brackets/operators")


def match_bracket(st1:stack, string:str):
    """ use a stack to see if brackets are closed"""
    # use a comprehension to filter out brackets
    brackets = [str(e) for e in string if e == "(" or e == ")"]
    # iterate through list and pop an open bracket if it is closed
    for element in brackets:
        if element == '(':
            st1.push(element)
        elif element == ')' and st1.get_top != None:
            try:
                st1.pop()
            except IndexError:
                # an index error is raised if we try to pop from an empty stack
                raise BracketsError("invalid expression: mismatched brackets")
    if len(st1) != 0:
        # return True if all opend brackets were closed
        raise BracketsError("invalid expression: mismatched brackets")

def validate(string:str):
    """ function that calls all valiadation functions back to back"""
    # NOTE: this does not say there are multiple
    # errors in the expression if there are
    # this approach was choosen to prioritize readability and expandability
    # also streamlines the interface of all the validation functions
    s1 = stack.Stack()
    try:
        match_bracket(s1, string)
        num_brackets(string)
        miss_op(string)
    except Exception as e:
        print(e)
        return False
    else:
        return True


def menu():
    """ menu for choosing what to do """
    while True:
        try:
            option = int(input("choose one of the following options: \n\t 1: Input an expression \n\t 2: quit \n"))
        except ValueError:
            print("please enter a valid option\n")
        else:
            if option == 1:
                usr_in = input("Please enter an algebraic expression: ")
                valid = validate(usr_in)
                if valid == True:
                    print(f"{usr_in} = {eval(usr_in)}\n")

            elif option == 2:
                break


if __name__ == '__main__':
    # calling menu to run the program, ideally this would be compiled into a .exe or .deb
    # to not have to run the source code manually, this would make it more portable
    # packages would not need to be installed by the end user
    a = '(((5 + 2) * (2 - 1))/((2 + 9) + ((7 - 2) - 1)) * 8)'
    b = '(((2*(3+2))+5)/2)'
    c = '(*2(1+2))'
    print(validate(a))
    print(eval(a))
    print(validate(b))
    print(eval(b))
    print(validate(c))

    menu()
