""" 52093080 """
import re
import pickle
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

""" Tree node base and utils"""
# inspired by @julkar9 post "Program to convert Infix notation to Expression Tree"
# on geeksforgeeks.org
# https://www.geeksforgeeks.org/program-to-convert-infix-notation-to-expression-tree/
# adapted to work with our string format in pyhton
class _TreeNode():

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def __str__(self):
        if self.data == None:
            return "\0"
        else:
            return self.data

class _ExpressionTree():
    def __init__(self, root:_TreeNode):
        self.root = root

    def __str__(self) -> str:
        return str(inorder_trav(self.root, []))

    def print(self):
        lst = inorder_trav(self.root, [])
        print(lst)
        return lst

def inorder_trav(start:_TreeNode, travd:list) -> list:
    """ traverses left->root->right """
    if start:
        inorder_trav(start.left, travd)
        travd.append(start.data)
        inorder_trav(start.right, travd)

        return travd


def build_tree(string:str) -> _TreeNode:
        """ traverses the string an builds the expression tree while doing so """
        # traverses the string from left to right
        # all operators prioritze the left operand, so this should work fine
        # have an operator stack and an operand stack
        # operators are pushed on the operator stack as strings
        # operands are pushed on operand stack as tree nodes

        # when a closed bracket would be pushed:
        #   take the last two items on the operand stack
        #   make a new node with them the operator as parent node and the operatnds as children nodes
        #   pop the operator and the the opened bracket below it
        #   push the newly created node on the operand stack

        for ch in string:
            if ch == " ":
                ch.replace(" ","")

        op_stack = stack.Stack()
        node_stack = stack.Stack()

        p1 = re.compile("[\(\+\-\*\/]")

        for ch in string:
            if ch.isalnum():
                new = _TreeNode(ch)
                node_stack.push(new)

            elif re.match(p1, ch) is not None:
                op_stack.push(ch)

            elif ch == ")":
                parent = _TreeNode(op_stack.pop())

                parent.right = node_stack.pop()
                parent.left = node_stack.pop()
                node_stack.push(parent)

                op_stack.pop()

                # print("new")
                # print(op_stack)
                # print(node_stack)

            else:
                raise Exception("Error: unxpected character in expression")

        return node_stack.pop()

def format_tree(string:str) -> str:
    s1 = stack.Stack()
    ops = ["+","-","*","/"]
    out = ""
    for char in string:
        if char == "(":
            s1.push(char)
        elif char == ")":
            s1.pop()
        elif char.isnumeric():
            out += "\t"*len(s1) + char + "\n"
        elif char in ops:
            out += "\t"*(len(s1)-1) + char + "\n"
    return out



""" validation functions """
def contained_charcters(string:str) -> Exception:
    p1 = re.compile("[^0-9\+\-\*\/\(\)]+")
    f1 = re.search(p1, string)

    if f1 != None:
        raise SyntaxError(f"Invalid character/s: {f1.group()}")
    else:
        pass

def miss_op(string:str) -> Exception:
    """ a function that matched patterns in the string, that make an expression invalid"""
    # stripping all whitespaces
    # so i dont have to deal with them when matching patterns
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
        raise OperandsError("invalid expression: missing operand")
    elif f5 is not None or f6 is not None:
        raise OperatorsError("invalid expression: elements in wrong order")
    else:
        pass

def num_brackets(string:str) -> Exception:
    """ there need to be twice as many brackets as operators """
    """ otherwise there is more than 1 operator in bracket pair """
    """ check after the closing of brackets is checked"""
    # unforunately has overlap with some of the regex cases
    brackets = [str(e) for e in string if e == "(" or e == ")"]
    operators = [str(e) for e in string if e == "+" or e == "-" or e == "*" or e == "/"]

    if len(brackets) != 2*len(operators):
        # raise operands error if there are the wrong number of brackets/operators
        raise OperandsError("invalid expression: wrong number of brackets/operators")


def match_bracket(st1:stack, string:str) -> Exception:
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

def validate(string:str)->bool:
    """ function that calls all valiadation functions back to back"""
    # NOTE: this does not say there are multiple
    # errors in the expression if there are
    # this approach was choosen to prioritize readability and expandability
    # also streamlines the interface of all the validation functions
    s1 = stack.Stack()
    try:
        match_bracket(s1, string)
        num_brackets(string)
        contained_charcters(string)
        miss_op(string)
        if len(string) < 2:
            raise SyntaxError("SyntaxError: expression too short")
    except Exception as e:
        print(e)
        return False
    else:
        return True

""" saving and loading from a .json file """
def save(string:str, name="save.txt"):
    with open(name, mode="a", encoding="utf-8") as file:
        file.write(string + "\n")

def load(name:str="save.txt"):
    with open(name, mode="r", encoding="utf-8") as file:
        lst = (file.readlines())
        lst = [e.replace("\n","") for e in lst]
        return lst

""" menu for user interaction """
def menu():
    """ menu for choosing what to do """
    while True:
        try:
            option = int(input("choose one of the following options: \n\t 0: quit \n\t 1: Input an expression \n\t 2: load from a file \n\t"))
        except ValueError:
            print("please enter a valid option\n")
        else:

            if option == 0:
                break

            elif option == 1:
                usr_in = input("Please enter an algebraic expression: ")
                usr_in = usr_in.replace(" ","")
                print(usr_in)
                valid = validate(usr_in)
                if valid == True:
                    print("expression is valid")
                    print(f"{usr_in} = {eval(usr_in)}\n")
                    r1 = build_tree(usr_in)
                    t1 = _ExpressionTree(r1)
                    print(format_tree(usr_in))

                    input_string = input("Do You want to save this tree? (Y/n)")
                    input_string = input_string.replace(" ","")
                    input_string = input_string[:1]

                    if input_string == "Y" or input_string == "y":
                        # the valid usr input is a serializantion of the binary tree, it will be saved
                        save(usr_in)
                        print("tree was saved to file")
                    else:
                        print("The tree was not be saved")


            elif option == 2:
                entries = load()
                print(entries)
                input_string = input("Do You want to print a saved tree? (Y/n)")
                input_string = input_string.replace(" ", "")[:1]
            if input_string == "Y" or input_string == "y":
                for e in entries:
                    print(e + "\n")
                    print(format_tree(e) + "\n")
            else:
                print("no trees were printed")

if __name__ == '__main__':
    # calling menu to run the program, ideally this would be compiled into a .exe or .deb
    # to not have to run the source code manually, this would make it more portable
    # packages would not need to be installed by the end user
    a = '(((5 + 2) * (2 - 1))/((2 + 9) + ((7 - 2) - 1)) * 8)'
    b = '(((2*(3+2))+5)/2)'
    c = '(((2*(3+2))+5)/2)'

    # print("----------------Tree test-----------------")
    # t1 = _ExpressionTree(build_tree(c))
    # root = build_tree(c)
    # print(root)
    # print("\n")
    # print(t1)
    # print(format_tree(c))

    menu()
