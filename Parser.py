#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  florian
# @date: 2017-06-15

"""
Parser
"""
from Token import operator_set_pref1, operator_set_pref2
from Lexer import Lexer


class AST(object):

    """Abstract Syntax Tree"""

    def __init__(self):
        pass


class OpNode(AST):

    """AST node for operators"""

    def __init__(self, left, token, right):
        """Constructor

        :left: left child
        :token: operator token
        :right: right child
        """
        self.left = left
        self._token = token
        if token.type == 'OPERATOR1':
            self.op = operator_set_pref1[token.value]
        elif token.type == 'OPERATOR2':
            self.op = operator_set_pref2[token.value]
        self.right = right


class Num(AST):

    """AST node for a number"""

    def __init__(self, token):
        """TODO: to be defined1.

        :token: value
        """
        self._token = token
        self.value = token.value


class Parser(object):

    """Parser for simple arithmetics. Builds and AST"""

    def __init__(self, text):
        self.lexer = Lexer(text)
        # read first token
        self.current_token = self.lexer.get_next_token()

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
        Factor rule: (integer| (LPAREN expr RPAREN))

        :return: value of the integer
        """
        print 'FACTOR'
        if self.current_token.value == '(':
            self.eat('GROUP')
            node = self.expr()
            self.eat('GROUP')
        elif self.current_token.type == 'INTEGER':
            node = Num(self.current_token)
            self.eat('INTEGER')
        return node

    def term(self):
        """
        Term rule: factor ((MUL|DIV) factor)+

        :returns: Terms to be added
        """
        print 'TERM'
        left = self.factor()

        while self.current_token.type == 'OPERATOR1':

            node = OpNode(left, self.current_token, self.factor())
            self.eat('OPERATOR1')

        if self.current_token.type in ['EOF', 'OPERATOR2', 'GROUP']:
            return node

    def expr(self):
        """
        Expr rule: term ((ADD|SUB) term)+ EOF

        :returns: TODO

        """
        print 'EXPR'

        left = self.term()

        while self.current_token.type == 'OPERATOR2':

            node = OpNode(left, self.current_token, self.term())
            self.eat('OPERATOR2')

        if self.current_token.type in ['EOF', 'GROUP']:
            return node
        else:
            raise Exception('No EOF at end of input, something went wrong')
