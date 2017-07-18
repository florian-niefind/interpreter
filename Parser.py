#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  florian
# @date: 2017-06-15

"""
Parser
"""
from Token import (INTEGER, OPERATOR1, OPERATOR2, GROUP, EOF,
                   BEGIN, END, DOT, ASSIGN, SEMI, ID,
                   operator_set_pref1, operator_set_pref2)
from Lexer import Lexer


#######################################
# Abstract syntax tree
#######################################

class AST(object):

    """Abstract Syntax Tree"""

    def __init__(self):
        pass


class Compound(AST):

    """AST node for compound statements"""

    def __init__(self):
        """Constructor"""
        self.children = []


class Assign(AST):

    """AST node for assign statements"""

    def __init__(self, left, token, right):
        """Constructor"""
        self._token = token
        self.left = left
        self.right = right


class Var(AST):

    """AST node for variables"""

    def __init__(self, token):
        """Constructor

        :token: TODO

        """
        self._token = token
        self.id = token.value


class BinOp(AST):

    """AST node for binary operators"""

    def __init__(self, left, token, right):
        """Constructor

        :left: left child
        :token: operator token
        :right: right child
        """
        self.left = left
        self._token = token
        if token.type == OPERATOR1:
            self.op = operator_set_pref1[token.value]
        elif token.type == OPERATOR2:
            self.op = operator_set_pref2[token.value]
        self.right = right


class UnOp(AST):

    """AST node for unary operators"""

    def __init__(self, token, expr):
        """Constructor

        :token: operator token
        :expr: another expression to be modified
        """
        self._token = token
        self.op = token.value
        self.expr = expr


class NoOp(AST):

    """AST node for empty operator"""

    def __init__(self):
        """TODO: to be defined1. """
        pass


class Num(AST):

    """AST node for a number"""

    def __init__(self, token):
        """Constructor

        :token: value
        """
        self._token = token
        self.value = token.value


#######################################
# Parser
#######################################

class Parser(object):

    """Parser for simple arithmetics. Builds and AST"""

    def __init__(self, text):
        self.lexer = Lexer(text)

    def eat(self, type):
        """Consume a token if it is of the correct type

        :type: Required type for the token
        """
        if self.current_token.type == type:
            print 'Consumed %s' % self.current_token
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception('ParsingError: %s is not of type %s' % (
                self.current_token,
                type))

    def program(self):
        """
        Program rule: compound DOT

        :returns: the full AST with a compound node as root
        """
        print 'PROGRAM'
        node = self.compound()
        self.eat(DOT)
        return node

    def compound(self):
        """
        Compound rule: BEGIN statement+ END

        :returns: compound AST node
        """
        print 'COMPOUND'
        self.eat(BEGIN)
        node = Compound()

        node.children.append(self.statement())

        while self.current_token.type != END:
            node.children.append(self.statement())

        self.eat(END)
        return node

    def statement(self):
        """
        Statement rule: (compound | assign | empty) SEMI

        :returns: AST node
        """
        print 'STATEMENT'
        if self.current_token.type == BEGIN:
            node = self.compound()
        elif self.current_token.type == ID:
            node = self.assign()
        else:
            node = self.empty()

        if self.current_token.type == SEMI:
            self.eat(SEMI)
            return node
        elif self.current_token.type == END:
            return node
        else:
            raise Exception(
                'No SEMI or END at end of statement, something went wrong')

    def assign(self):
        """
        Assign rule: ID ASSIGN expr

        :returns: AST node
        """
        print 'ASSIGN'
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        node = Assign(left, token, self.expr())
        return node

    def variable(self):
        """
        variable rule: ID

        :returns: AST node
        """
        print 'VARIABLE'
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        """
        empty rule: NoOp

        :returns: NoOp AST node
        """
        print 'EMPTY'
        return NoOp()

    def factor(self):
        """
        Factor rule: (UnOp factor | variable | INTEGER | (LPAREN expr RPAREN))

        :returns: Num AST node
        """
        print 'FACTOR'
        if self.current_token.value == '(':
            self.eat(GROUP)
            node = self.expr()
            self.eat(GROUP)
        elif self.current_token.type == OPERATOR2:
            unop_token = self.current_token
            self.eat(OPERATOR2)
            node = UnOp(unop_token, self.factor())
        elif self.current_token.type == INTEGER:
            num_token = self.current_token
            self.eat(INTEGER)
            node = Num(num_token)
        elif self.current_token.type == ID:
            node = self.variable()
        return node

    def term(self):
        """
        Term rule: factor ((MUL|DIV) factor)+

        :returns: AST node
        """
        print 'TERM'
        node = self.factor()

        while self.current_token.type == OPERATOR1:
            op_token = self.current_token
            self.eat(OPERATOR1)
            node = BinOp(node, op_token, self.factor())

        return node

    def expr(self):
        """
        Expr rule: term ((ADD|SUB) term)+

        :returns: AST node

        """
        print 'EXPR'

        node = self.term()

        while self.current_token.type == OPERATOR2:
            op_token = self.current_token
            self.eat(OPERATOR2)
            node = BinOp(node, op_token, self.term())

        return node

    def parse(self):

        # read first token
        self.current_token = self.lexer.get_next_token()
        node = self.program()
        if self.current_token.type == EOF:
            return node
        else:
            raise Exception('No EOF at end of input, something went wrong')


if __name__ == "__main__":
    while True:
        try:
            text = raw_input('Enter>')
        except EOFError:
            break
        if not text:
            continue
        a = Parser(text)
        a.parse()
        print ''
