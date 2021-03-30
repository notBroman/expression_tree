""" 52093080 """
import re
import json
from ADT import tree_base
from ADT import stack


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
                return False
    if len(st1) == 0:
        # return True if all opend brackets were closed
        return True
    else:
        # return False if brackets are missmatched
        return False

def validate(string:str):
    s1 = stack.Stack()
    brac_val = match_bracket(s1, string)
    if brac_val == False:
        print("invalid expression: brackets do not match\n")
    else:
        # check if expression follows X?Y recursively or not
        # TODO
        print("brackets match \n")


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
    print(eval(a))

    menu()
