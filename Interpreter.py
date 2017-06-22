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

    """Generic way to visit nodes of an AST"""

    def visit(self, node):
        """Generic visit method. Chooses the appropriate concrete visit method

        :node: AST node to be interpreted
        :returns: result of all children

        """
        method_name = 'visit_' + type(node).__name__
        visitor_method = getattr(self, method_name,
                                 self.none_found)
        return visitor_method(node)

    def none_found(self, node):
        """
        Raises exception if no visitor is found
        """
        raise Exception("No visitor method defined for node {}".format(
            type(node).__name__))


class Interpreter(NodeVisitor):

    """Interpreter"""

    def __init__(self, text):
        self.parser = Parser(text)

    def visit_OpNode(self, node):
        """Visitor for operator node

        :node: AST node to be interpreted
        :returns: result of all children

        """
        print("("),
        print node._token.value,
        self.visit(node.left)
        self.visit(node.right)
        print(")"),

    def visit_Num(self, node):
        """Visitor for operator node

        :node: AST node to be interpreted
        :returns: result of all children

        """
        print node.value,

    def interpret(self):
        """
        Method to run the interpreter
        """
        self.tree = self.parser.parse()
        self.visit(self.tree)


if __name__ == "__main__":
    while True:
        try:
            text = raw_input('Enter>')
        except EOFError:
            break
        if not text:
            continue
        Interpreter(text).interpret()
        print ''
        # print 'Result is %i' % Interpreter(text).interpret()
