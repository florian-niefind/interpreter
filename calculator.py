#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  florian
# @date: 2017-06-12

"""
A simple interpreter for arithmetic expressions, as outlined here:
https://ruslanspivak.com/lsbasi-part1/
"""
import operator

# define tokens
INTEGER, OPERATOR, EOF = 'INTEGER', 'OPERATOR', 'EOF'
operator_set = {'+': operator.add, '-': operator.sub, '*': operator.mul,
                '/': operator.div}


class Token(object):

    """Single input token"""

    def __init__(self, type, value):
        """Set type and value"""
        self.type = type

        self.value = value

    def __str___(self):
        """TODO: Docstring for __str__.

        :f: TODO
        :returns: TODO

        """
        return 'Token {type}: {value}'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        """Turn into string
        :returns: TODO

        """
        return self.__str__()


class Interpreter(object):

    """Interpreter for the calculator"""

    def __init__(self, input_string):
        """Reads a string expression and interprets it. Finally returns the
        result.

        :input_string: A string of the form '%01i+%01i'

        """
        self.text = input_string.replace(' ', '')
        self.current_token = None
        self.pos = 0

    def get_next_token(self):
        """Parses the next token from the input
        :returns: Next token

        """
        if self.pos >= len(self.text):
            return Token(EOF, None)

        current_char = self.text[self.pos]

        if current_char.isdigit():

            while self.pos + 1 < len(self.text):
                next_input = self.text[self.pos+1]
                if next_input.isdigit():
                    current_char += next_input
                    self.pos += 1
                if next_input in operator_set.keys():
                    break

            self.pos += 1
            print 'Parsed %s, Pos is %i' % (current_char, self.pos)
            return Token(INTEGER, int(current_char))

        elif current_char in operator_set.keys():
            self.pos += 1
            print 'Parsed %s, Pos is %i' % (current_char, self.pos)
            return Token(OPERATOR, current_char)

        else:
            raise ValueError('%s is not a valid input', current_char)

    def consume_token(self, expected_type):
        """TODO: Docstring for eat_token.

        :arg1: TODO
        :returns: TODO

        """
        if self.current_token.type == expected_type:
            self.current_token = self.get_next_token()
        else:
            raise Exception("Parser expected a different token")

    def term(self):
        """
        Parse a term and return it\s value
        """
        token = self.current_token
        self.consume_token('INTEGER')
        return token.value

    def expr(self):
        """Expr: INTEGER PLUS INTEGER

        :f: TODO
        :returns: TODO

        """
        self.current_token = self.get_next_token()
        res = self.term()

        while self.current_token.type == OPERATOR:
            op = self.current_token
            self.consume_token(OPERATOR)
            res = operator_set[op.value](
                res,
                self.term())

        return res


if __name__ == "__main__":
    while True:
        try:
            text = raw_input('Enter>')
        except EOFError:
            break
        if not text:
            continue
        print Interpreter(text).expr()
