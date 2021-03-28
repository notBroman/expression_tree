""" 52093080 """

import re
import json
import importlib

class Expr():
    """ look into oparator overloading """
    pass

class Operator(Expr):
    """ parent of every operator (+,-,*,/) """
    """ defines abstract methods """

    def __init__(self):
        pass

    def __str__(self):
        raise NotImplemtedError

    def calc(self):
        raise NotImplementedError

class Const(Expr):
    """ constant value """
    def __init__(self, val:int):
        self.val:int = val

    def __str__(self):
        return str(self.val)

    def calc(self):
        return self.val

class Add(Operator):
    """ Addition Operator """
    def __init__(self, expr1:Expr, expr2:Expr):
        self.ex1:Expr = expr1
        self.ex2:Expr = expr2
        self.result:int = None

class Sub(Operator):
    """ Subtraction Operator """
    def __init__(self, expr1:Expr, expr2:Expr):
        self.ex1:Expr = expr1
        self.ex2:Expr = expr2
        self.result:int = None

class Mul(Operator):
    """ Multiplication Operator"""
    def __int__(self, expr1:Expr, expr2:Expr):
        self.ex1:Expr = expr1
        self.ex2:Expr = expr2
        self.result:int = None

    def __str__(self):
        return str(self.ex1) + '*' + str(self.ex2)

    def calc(self):
        self.result = self.ex1.calc() * self.ex2.calc()
        return self.result

class Div(Operator):
    """ Division Operator """
    def __init__(self, expr1:Expr, expr2:Expr):
        self.ex1:Expr = expr1
        self.ex2:Expr = expr2
        self.result = None

