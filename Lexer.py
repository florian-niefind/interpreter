#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  florian
# @date: 2017-06-14

"""
Contains the lexer class for our interpreter
"""
from Token import Token, INTEGER, OPERATOR1, OPERATOR2, EOF, \
        operator_set_pref1, operator_set_pref2, grouping_set


class Lexer(object):

    """Lexer class for a compiler. Reads a string of inputs and returns the
    corresponding tokens"""

    def __init__(self, text):
        """Stores text to be tokenized and the position that the parser is on

        :text: The text to be parsed
        """
        # strip whitespace
        self.text = text.replace(' ', '')
        self._pos = 0
        self.current_char = self.text[self._pos]

    def advance(self):
        """
        Advance the cursor one character
        """
        self._pos += 1
        if self._pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self._pos]

    def integer(self):
        """
        Move integer logic into separate function

        :returns: A fully parsed integer token
        """
        token = self.current_char
        self.advance()
        # check for subsequent digits
        while self.current_char is not None and self.current_char.isdigit():
            token += self.current_char
            self.advance()
        print ('Parsed Integer %s, pos is %i' % (token, self._pos))
        return int(token)

    def get_next_token(self):
        """
        Reads the next token from the input

        :returns: A token object

        """
        if self.current_char is None:
            print ('Parsed EOF, pos is %i' % (self._pos))
            return Token(EOF, None)

        elif self.current_char.isdigit():
            return Token(INTEGER, self.integer())

        elif self.current_char in grouping_set:
            token = Token('GROUP', self.current_char)
            self.advance()
            print ('Parsed %s, pos is %i' % (self.current_char, self._pos))
            return token

        elif self.current_char in operator_set_pref1.keys():
            token = Token(OPERATOR1, self.current_char)
            self.advance()
            print ('Parsed Operator %s, pos is %i' % (token.value, self._pos))
            return token

        elif self.current_char in operator_set_pref2.keys():
            token = Token(OPERATOR2, self.current_char)
            self.advance()
            print ('Parsed Operator %s, pos is %i' % (token.value, self._pos))
            return token

        else:
            raise Exception('Parsing Error at pos %i, character %s' %
                            (self._pos, self.text[self._pos]))
