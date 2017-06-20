#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  florian
# @date: 2017-06-15

"""
Interpreter
"""
from Parser import Parser


class NodeVisitor(object):

    """Docstring for NodeVisitor. """

    def __init__(self):
        """TODO: to be defined1. """


class Interpreter(NodeVisitor):

    """Interpreter"""

    def __init__(self, text):
        """TODO: to be defined1. """
        self.parser = Parser(text)
        NodeVisitor.__init__(self)


if __name__ == "__main__":
    while True:
        try:
            text = raw_input('Enter>')
        except EOFError:
            break
        if not text:
            continue
        print 'Result is %i' % Interpreter(text).expr()
