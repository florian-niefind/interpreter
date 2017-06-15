#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  florian
# @date: 2017-06-15

"""
Interpreter
"""
from Token import operator_set
from Lexer import Lexer


class Interpreter(object):

    """Interpreter for simple calculator arithmetics"""

    def __init__(self, text):
        self.lexer = Lexer(text)
        self.current_token = None

    def eat(self, type):
        """Consume a token if it is of the correct type

        :type: Required type for the token
        """
        if self.current_token.type == type:
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
        result = self.current_token.value
        self.eat('INTEGER')
        return result

    def operator(self):
        """
        Rule for handling operators

        :returns: the operator function to be used

        """
        op = self.current_token.value
        self.eat('OPERATOR')
        return operator_set[op]

    def expr(self):
        """
        Expr rule: Factor (Operator Factor)+ EOF

        :returns: TODO

        """
        self.current_token = self.lexer.get_next_token()

        result = self.factor()

        while self.current_token.type == 'OPERATOR':

            op = self.operator()
            result = op(result, self.factor())

        if self.current_token.type == 'EOF':
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
