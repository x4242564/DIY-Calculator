import unittest

from math_interpreter.tokens import Token, TokenType
from math_interpreter.lexer import Lexer

class TestLexer(unittest.TestCase):

    def test_empty(self): # tests when a user inputs nothing
        tokens = list(Lexer("").generate_tokens())
        self.assertEqual(tokens, [])

    def test_whitespace_ignored(self): # tests that whitespaces aren't counted as tokens
        tokens = list(Lexer(" \t\n \t\t\n  ").generate_tokens())
        self.assertEqual(tokens, [])

    def test_numbers(self): # tests that numbers are correctly tokenized
        tokens = list(Lexer("98. .89 987.654 123 .").generate_tokens())
        self.assertEqual(tokens, [
            Token(TokenType.NUMBER, 98.0),
            Token(TokenType.NUMBER, 0.89),
            Token(TokenType.NUMBER, 987.654),
            Token(TokenType.NUMBER, 123.0),
            Token(TokenType.NUMBER, 0.0)
        ])

    def test_operators(self): # tests that operators are correctly tokenized
        tokens = list(Lexer("+-*/^").generate_tokens())
        self.assertEqual(tokens, [
            Token(TokenType.PLUS),
            Token(TokenType.MINUS),
            Token(TokenType.MULTIPLY),
            Token(TokenType.DIVIDE),
            Token(TokenType.POWER)
        ])

    def test_parentheses(self): # tests that parentheses are correctly tokenized
        tokens = list(Lexer("()").generate_tokens())
        self.assertEqual(tokens, [
            Token(TokenType.LPAREN),
            Token(TokenType.RPAREN)
        ])

    def test_all(self): # tests a combination of numbers, operators, and parentheses
        tokens = list(Lexer("3 ^ 2 + 4.5 * (2 - 1)").generate_tokens())
        self.assertEqual(tokens, [
            Token(TokenType.NUMBER, 3.0),
            Token(TokenType.POWER),
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.PLUS),
            Token(TokenType.NUMBER, 4.5),
            Token(TokenType.MULTIPLY),
            Token(TokenType.LPAREN),
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.MINUS),
            Token(TokenType.NUMBER, 1.0),
            Token(TokenType.RPAREN)
        ])