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
INTEGER, OPERATOR1, OPERATOR2, GROUP, EOF = ('INTEGER', 'OPERATOR1',
    'OPERATOR2', 'GROUP', 'EOF')
grouping_set = ['(', ')']
operator_set_pref1 = {'*': operator.mul, '/': operator.div}
operator_set_pref2 = {'+': operator.add, '-': operator.sub}


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
