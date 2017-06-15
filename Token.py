#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  florian
# @date: 2017-06-14

"""
Contains the token class
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
        """ """
        return self.__repr__()

    def __repr__(self):
        """ """
        return 'Token {type}: {value}'.format(
            type=self.type,
            value=repr(self.value)
        )
