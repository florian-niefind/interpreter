#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  florian
# @date: 2017-06-15

"""
Parser
"""
from Token import INTEGER, OPERATOR1, OPERATOR2, GROUP, EOF, operator_set_pref1, operator_set_pref2
from Lexer import Lexer


class AST(object):

    """Abstract Syntax Tree"""

    def __init__(self):
        pass


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


class Num(AST):

    """AST node for a number"""

    def __init__(self, token):
        """Constructor

        :token: value
        """
        self._token = token
        self.value = token.value


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

    def factor(self):
        """
        Factor rule: (UnOp factor | integer| (LPAREN expr RPAREN))

        :return: value of the integer
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
        return node

    def term(self):
        """
        Term rule: factor ((MUL|DIV) factor)+

        :returns: Terms to be added
        """
        print 'TERM'
        node = self.factor()

        while self.current_token.type == OPERATOR1:
            op_token = self.current_token
            self.eat(OPERATOR1)
            node = BinOp(node, op_token, self.factor())

        if self.current_token.type in [EOF, OPERATOR2, GROUP]:
            return node

    def expr(self):
        """
        Expr rule: term ((ADD|SUB) term)+ EOF

        :returns: TODO

        """
        print 'EXPR'

        node = self.term()

        while self.current_token.type == OPERATOR2:
            op_token = self.current_token
            self.eat(OPERATOR2)
            node = BinOp(node, op_token, self.term())

        if self.current_token.type in [EOF, GROUP]:
            return node
        else:
            raise Exception('No EOF at end of input, something went wrong')

    def parse(self):

        # read first token
        self.current_token = self.lexer.get_next_token()
        return self.expr()
