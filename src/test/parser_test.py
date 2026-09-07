import unittest
from math_interpreter.tokens import Token, TokenType
from math_interpreter.parser_ import Parser
from math_interpreter.nodes import *

class TestParser(unittest.TestCase):

    def test_empty(self): # tests when a user inputs nothing
        tokens = []
        node = Parser(tokens).parse()
        self.assertIsNone(node)

    def test_numbers(self): # tests when a user inputs nothing
        tokens = [Token(TokenType.NUMBER, 42.42)]
        node = Parser(tokens).parse()
        self.assertEqual(node.value, 42.42)

    def test_individual_operations(self): # tests individual operations
        tokens = [Token(TokenType.NUMBER, 4),
                  Token(TokenType.PLUS),
                  Token(TokenType.NUMBER, 2)]
        
        node = Parser(tokens).parse()
        self.assertEqual(node, AddNode(NumberNode(4), NumberNode(2)))

        tokens = [Token(TokenType.NUMBER, 4),
                  Token(TokenType.MINUS),
                  Token(TokenType.NUMBER, 2)]
        
        node = Parser(tokens).parse()
        self.assertEqual(node, SubtractNode(NumberNode(4), NumberNode(2)))

        tokens = [Token(TokenType.NUMBER, 4),
                  Token(TokenType.MULTIPLY),
                  Token(TokenType.NUMBER, 2)]
        
        node = Parser(tokens).parse()
        self.assertEqual(node, MultiplyNode(NumberNode(4), NumberNode(2)))

        tokens = [Token(TokenType.NUMBER, 4),
                  Token(TokenType.DIVIDE),
                  Token(TokenType.NUMBER, 2)]
        
        node = Parser(tokens).parse()
        self.assertEqual(node, DivideNode(NumberNode(4), NumberNode(2)))

    def test_full_expression(self): # tests a full expression with multiple operations
        tokens = [
            # 3 + 4 ^ 2 * (7 - 1) / 3
            Token(TokenType.NUMBER, 3),
            Token(TokenType.PLUS),
            Token(TokenType.NUMBER, 4),
            Token(TokenType.POWER),
            Token(TokenType.NUMBER, 2),
            Token(TokenType.MULTIPLY),
            Token(TokenType.LPAREN),
            Token(TokenType.NUMBER, 7),
            Token(TokenType.MINUS),
            Token(TokenType.NUMBER, 1),
            Token(TokenType.RPAREN),
            Token(TokenType.DIVIDE),
            Token(TokenType.NUMBER, 3)
        ]
        node = Parser(tokens).parse()
        self.assertEqual(
            node,
            AddNode(
                NumberNode(3),
                DivideNode(
                    MultiplyNode(
                        PowerNode(NumberNode(4), NumberNode(2)),
                        SubtractNode(NumberNode(7), NumberNode(1))
                    ),
                    NumberNode(3)
                )
            )
        )