""" 52093080 """
import re
import json
from ADT import tree_base
from ADT import stack

class OperandsError(Exception):
    pass

class BracketsError(Exception):
    pass

class OperatorsError(Exception):
    pass

def miss_op(string:str):
    p1 = re.compile("\([0-9]\(")
    p2 = re.compile("\)[0-9]\)")
    p3 = re.compile("\([0-9][\+\-\*\/]\)")
    p4 = re.compile("\([\+\-\*\/][0-9]\)")
    p5 = re.compile("\([\+\-\*\/][0-9]\(")
    p6 = re.compile("\)[0-9][\+\-\*\/]\)")

    f1 = re.search(p1, string)
    f2 = re.search(p2, string)
    f3 = re.search(p3, string)
    f4 = re.search(p4, string)
    f5 = re.search(p5, string)
    f6 = re.search(p6, string)

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
    brackets = [str(e) for e in string if e == "(" or e == ")"]
    operators = [str(e) for e in string if e == "+" or e == "-" or e == "*" or e == "/"]

    if len(brackets) != 2*len(operators):
        # raise operands error if there are the wrong number of brackets/operators
        raise OperandsError("invalid expression: wrong number of operands")


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
    while True:
        try:
            option = int(input("choose one of the following options: \n\t 1: Input an expression \n\t 2: quit \n"))
        except ValueError:
            print("please enter a valid option")
        else:
            if option == 1:
                usr_in = input("Please enter an algebraic expression: ")
                validate(usr_in)

            elif option == 2:
                break


if __name__ == '__main__':
    a = '(((5 + 2) * (2 - 1))/((2 + 9) + ((7 - 2) - 1)) * 8)'
    b = '(((2*(3+2))+5)/2)'
    c = '(*2(1+2))'
    print(validate(a))
    print(eval(a))
    print(validate(b))
    print(eval(b))
    print(validate(c))

    menu()
