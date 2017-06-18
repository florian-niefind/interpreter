#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  florian
# @date: 2017-06-15

"""
Interpreter
"""
from Token import operator_set_pref1, operator_set_pref2
from Lexer import Lexer


class Interpreter(object):

    """Interpreter for simple calculator arithmetics"""

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
        Rule for handling factors

        :return: value of the integer
        """
        print 'FACTOR'
        if self.current_token.value == '(':
            self.eat('GROUP')
            result = self.expr()
            self.eat('GROUP')
        elif self.current_token.type == 'INTEGER':
            result = self.current_token.value
            self.eat('INTEGER')
        return result

    def operator_pref1(self):
        """
        Rule for handling operators MUL and DIV

        :returns: the operator function to be used

        """
        op = self.current_token.value
        self.eat('OPERATOR1')
        return operator_set_pref1[op]

    def operator_pref2(self):
        """
        Rule for handling operators ADD and SUB

        :returns: the operator function to be used

        """
        op = self.current_token.value
        self.eat('OPERATOR2')
        return operator_set_pref2[op]

    def term(self):
        """Rule for handling terms

        :returns: Terms to be added
        """
        print 'TERM'
        result = self.factor()

        while self.current_token.type == 'OPERATOR1':

            op = self.operator_pref1()
            result = op(result, self.factor())

        if self.current_token.type in ['EOF', 'OPERATOR2', 'GROUP']:
            return result

    def expr(self):
        """
        Expr rule: Factor (Operator Factor)+ EOF

        :returns: TODO

        """
        print 'EXPR'

        result = self.term()

        while self.current_token.type == 'OPERATOR2':

            op = self.operator_pref2()
            result = op(result, self.term())

        if self.current_token.type in ['EOF', 'GROUP']:
            return result
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
        print 'Result is %i' % Interpreter(text).expr()
