""" 52093080 """
import re
import json
import expression
from ADT import tree_base
from ADT import stack


def match_bracket(stack:stack, string:str):
    """ use a stack to see if brackets are closed"""
    # use a comprehension to filter out brackets
    brackets = [str(e) for e in string if e == "(" or e == ")"]
    # iterate through list and pop an open bracket if it is closed
    for element in brackets:
        if element == '(':
            st1.push(element)
        elif element == ')' and st1.get_top != None:
            st1.pop()
    if len(st1) == 0:
        # return 1 if all opend brackets were closed
        return 1
    else:
        # return 0 if brackets are missmatched
        return 0


if __name__ == '__main__':
    a = '(((5 + 2) * (2 - 1))/((2 + 9) + ((7-2)-1)) * 8)'
    st1 = stack.Stack()

    print(match_bracket(st1, a))
