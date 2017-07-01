#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  florian
# @date: 2017-06-14

"""
Contains the lexer class for our interpreter
"""
from Token import (Token, INTEGER, OPERATOR1, OPERATOR2, EOF, GROUP,
                   BEGIN, END, DOT, ASSIGN, SEMI, ID,
                   operator_set_pref1, operator_set_pref2, grouping_set)

RESERVED_KEYWORDS = {'BEGIN': Token(BEGIN, 'BEGIN'),
                     'END': Token(END, 'END')}


class Lexer(object):

    """Lexer class for a compiler. Reads a string of inputs and returns the
    corresponding tokens"""

    def __init__(self, text):
        """Stores text to be tokenized and the position that the parser is on

        :text: The text to be parsed
        """
        # strip whitespace
        self.text = text
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

    def peek(self):
        """
        Look ahead in the input stream

        :return: The next character
        """
        self.peek_pos = self._pos + 1
        if self.peek_pos >= len(self.text):
            return None
        else:
            return self.text[self.peek_pos]

    def _id(self):
        """Check for reserved keywords

        :returns: A fully parsed ID token
        """
        token = self.current_char
        self.advance()

        while self.current_char is not None and self.current_char.isalnum():
            token += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(token, Token(ID, token))
        return token

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

        token = Token(INTEGER, int(token))
        return token

    def skip_whitespace(self):
        """
        Skips whitespace
        """
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        """
        Reads the next token from the input

        :returns: A token object

        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            elif self.current_char.isalpha():
                token = self._id()
                print ('Lexed %s, pos is %i' % (token, self._pos))
                return token

            elif self.current_char == ':' and self.peek() == '=':
                token = Token(ASSIGN, ':=')
                self.advance()
                self.advance()
                print ('Lexed %s, pos is %i' % (token, self._pos))
                return token

            elif self.current_char == ';':
                token = Token(SEMI, ';')
                self.advance()
                print ('Lexed %s, pos is %i' % (token, self._pos))
                return token

            elif self.current_char == '.':
                token = Token(DOT, '.')
                self.advance()
                print ('Lexed %s, pos is %i' % (token, self._pos))
                return token

            elif self.current_char.isdigit():
                token = self.integer()
                print ('Lexed %s, pos is %i' % (token, self._pos))
                return token

            elif self.current_char in grouping_set:
                token = Token(GROUP, self.current_char)
                self.advance()
                print ('Lexed %s, pos is %i' % (self.current_char, self._pos))
                return token

            elif self.current_char in operator_set_pref1.keys():
                token = Token(OPERATOR1, self.current_char)
                self.advance()
                print ('Lexed Operator %s, pos is %i' % (
                    token.value, self._pos))
                return token

            elif self.current_char in operator_set_pref2.keys():
                token = Token(OPERATOR2, self.current_char)
                self.advance()
                print ('Lexed Operator %s, pos is %i' % (
                    token.value, self._pos))
                return token

            else:
                raise Exception('Parsing Error at pos %i, character %s' %
                                (self._pos, self.text[self._pos]))

        print ('Lexed EOF, pos is %i' % (self._pos))
        return Token(EOF, None)


if __name__ == "__main__":
    while True:
        try:
            text = raw_input('Enter>')
        except EOFError:
            break
        if not text:
            continue
        a = Lexer(text)
        res = Token('DUMMY', 'DUMMY')
        while res is None or res.type != EOF:
            res = a.get_next_token()
        print ''
