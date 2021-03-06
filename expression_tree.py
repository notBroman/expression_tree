""" 52093080 """
import re
import unittest

#############################################################################################################
########################################### README.md #######################################################
#############################################################################################################
#
# Installation:
# 1. change expression_tree.txt to expression_tree.py
# 2. open in your favourite IDE/text editor
# 3. run with the run botton or in commandline with
#   '''
#   python3 expression_tree.py
#   '''
# 4. there a menu pops up in the commandline, instructions should be depicted
#
# Changing to unittest:
# 1. in the last 10 lines of the program, comment out menu and decomment unittest.main
# 2. make sure that there is only one of the two options above running
#
# License:
# You can use this code and program under the GNU General Public License v3.0
# however I cannot guarantee that any of this code works outside of this project
# port at your own risk, I will not take responsibility for any damges caused by this code, when
# copied into another codebase
#
# CHANGLE.LOG:
# 0.1:      basic expression validation and calculation of result
# 0.2:      basic menu
# 0.3:      inorder traversal
# 0.3.1:    conversion from expression into expression tree
# 0.4:      integration of tree conversion of parsed expression into menu
# 0.4.1:    inorder traversal
# 0.5:      extension of expression validation with regex
# 0.6:      saving and loading
# 0.6.1:    inegtration of saving an loading into menu
# 0.7:      formatting of tree for printing
# 0.7.1:    implementation into menu
# 0.8:      test cases
# 0.8.1:    more exception handling
# 0.9:      porting into a single file
# 0.9.1:    removing dead && redundant code
#
# Misc:
# If there are any potential bugs or you notice bad practices please add them with the line number
# and in which function/class/subclass they are in the potential bugs section below.
# sadly opening an issue not going to be possible here
#
# If an algorithm was taken from somewhere, the source is referanced before the function
# thank you to black tea for the caffeine that kept me going,
# shoutouts lofi hiphop beats to relax and study to, as well as mac miller
#
# POTENTIAL BUGS:
#
#############################################################################################################
#############################################################################################################
#############################################################################################################
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

""" classes for testing: tree conversion, stack implementation, validation of expressions"""

class test_tree(unittest.TestCase):
    def test_buildtree(self):
        t1 = _ExpressionTree("(((1+9)*3)-8)")
        t1.build_tree()
        t2 = _ExpressionTree("(((1+9)*4)-(4+8))")
        t2.build_tree()

        self.assertIsInstance(t1.build_tree(), _TreeNode)
        self.assertEqual(t1.root.data, "-")
        self.assertEqual(t1.inorder_trav(t1.root, []), ["1","+","9","*","3","-","8"])

        self.assertIsInstance(t1.build_tree(), _TreeNode)
        self.assertEqual(t2.root.data, "-")
        self.assertEqual(t2.inorder_trav(t2.root, []), ["1","+","9","*","4","-","4","+","8"])

class test_stack(unittest.TestCase):
    def test_push(self):
        s1 = Stack()

        expression = "(((1+9)*4)-(4+8))"
        for char in expression:
            s1.push(char)
            self.assertEqual(s1.get_top(), char)

    def test_pop(self):
        s1 = Stack()

        expression = "(((1+9)*4)-(4+8))"
        for char in expression:
            if char != ")":
                s1.push(char)
            else:
                oldsize = len(s1)
                oldtop = s1.get_top()
                s1.pop()
                self.assertNotEqual(len(s1), oldsize)
                self.assertNotEqual(s1.get_top(), oldtop)

class test_valid(unittest.TestCase):
    def test_validate(self):
        self.assertFalse(validate("(4*3*2)"))
        self.assertFalse(validate("(4*(2))"))
        self.assertFalse(validate("(4*(3+2)*(2+1))"))
        self.assertFalse(validate("(2*4)+(3+2)"))
        self.assertFalse(validate("((2+3)*(4*5)"))
        self.assertFalse(validate("(((2+3)*(4*5))+(1(2+3)))"))
        self.assertFalse(validate("2"))
        self.assertFalse(validate("((1+1)2*)"))
        self.assertFalse(validate("!@#$^%&{:>>?<\|}"))
        self.assertFalse(validate("(+2(1+1))"))

""" stack implmentation with sinlgy linked list"""
# based off of goodrich book and lecture notes
class _Node():
    __slots__ = '_element', 'next', 'prev'

    def __init__(self, element, next_node=None, prev_node=None):
        self._element = element
        self.next = next_node
        self.prev = prev_node

    def __str__(self) -> str:
        try:
            return str(self._element)
        except Exception as e:
            return e

class Singly_Linked_List():

    def __init__(self, values=None):
        self._tail = None
        self._head = None
        if values is not None:
            self.add_multiple(values)

    def __str__(self):
        values = [str(x) for x in self]
        return ' -> '.join(values)

    def __len__(self) -> int:
        length = 0
        for element in self.__iter__():
            length += 1
        return length

    def add_first(self, value):
        newest = _Node(value)
        if self._head is None:
            newest.next = None
            self._head = self._tail = newest
        else:
            newest.next = self._head
            self._head = newest

    def rm_first(self):
        if self._head is None:
            raise ValueError("Value Error: No elements in Linked List")
        else:
            removed = self._head
            self._head = self._head.next

""" Stack """
""" my own implementation of a basic stack """
class Stack():
    def __init__(self):
        self._data = Singly_Linked_List()
        self._bot = self._data._tail
        self._top = self._data._head
        self._size = 0

    def __str__(self) -> str:
        return self._data.__str__()

    def __len__(self) -> int:
        return self._size

    def pop(self) -> str:
        if self._size == 0:
            raise IndexError("Error: the stack is empty")
        else:
            popped = self._data._head._element
            self._data.rm_first()
            self._top = self._data._head
            self._size -= 1
            return popped

    def push(self, element):
       self._data.add_first(element)
       self._size += 1

    def get_top(self) -> str:
        return self._data._head._element


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

    def __str__(self) -> str:
        if self.data == None:
            return "\0"
        else:
            return self.data

class _ExpressionTree():
    def __init__(self, expr:str):
        self.root = None
        self.expr = expr

    def __str__(self) -> str:
        return self.format_tree()

    def inorder_trav(self, start:_TreeNode, travd:list) -> list:
        """ traverses left->root->right """
        if start:
            self.inorder_trav(start.left, travd)
            travd.append(start.data)
            self.inorder_trav(start.right, travd)

            return travd


    def build_tree(self) -> _TreeNode:
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

        string = self.expr
        for ch in string:
            if ch == " ":
                ch.replace(" ","")

        op_stack = Stack()
        node_stack = Stack()

        p1 = re.compile("[\(\+\-\*\/]")

        for ch in string:
            if ch.isalnum():
                new = _TreeNode(ch)
                node_stack.push(new)

            elif re.match(p1, ch) is not None:
                op_stack.push(ch)

            elif ch == ")":
                """ convert operand pair and operator to node """
                parent = _TreeNode(op_stack.pop())

                parent.right = node_stack.pop()
                parent.left = node_stack.pop()
                node_stack.push(parent)

                op_stack.pop()

        self.root = node_stack.pop()
        return self.root

    def format_tree(self) -> str:
        """ get tree in decent format for printing to user """
        # my own idea after realizing that the indentation is dependant on depth of node

        # the depth can be depermined by counting the brackets
        # ( -> depth++
        # ) -> depth--
        # operators are always at depth of operand - 1
        # if open brackets are push onto a stack the size of the stack is the depth of the operand
        # when brackets are closed pop an opened bracket from the stack
        # add tabulators \t * depth to string for operands, then operand, then newline \n
        # add tabulators \t * (depth--) to string for operators, then operator, then newline \n
        string = self.expr
        s1 = Stack()
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
# own work no inspration other than lofi hiphop to relax and study too
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


def match_bracket(st1:Stack, string:str) -> Exception:
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

def validate(string:str) -> bool:
    """ function that calls all valiadation functions back to back"""
    # NOTE: this does not say there are multiple
    # errors in the expression if there are
    # this approach was choosen to prioritize readability and expandability
    # also streamlines the interface of all the validation functions
    s1 = Stack()
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
    """ save to a save.txt file in the same directory as the .py file"""
    with open(name, mode="a", encoding="utf-8") as file:
        file.write(string + "\n")

def load(name:str="save.txt"):
    """ load from save.txt file, in the same directory as the .py file"""
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
                    t1 = _ExpressionTree(usr_in)
                    print(t1)

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
                try:
                    entries = load()
                except Exception:
                    print("error while loading, check if save.txt exists")
                else:
                    entries = [e for e in entries if validate(e) == True]
                    print(entries)
                    input_string = input("Do You want to print a saved tree? (Y/n)")
                    input_string = input_string.replace(" ", "")[:1]
                    if input_string == "Y" or input_string == "y":
                        for e in entries:
                            print(e + "\n")
                            t = _ExpressionTree(e)
                            print(t)
                    else:
                        print("no trees were printed")

if __name__ == '__main__':
    # calling menu to run the program, ideally this would be compiled into a .exe or .deb
    # to not have to run the source code manually, this would make it more portable
    # packages would not need to be installed by the end user


    # unittest.main()
    menu()
