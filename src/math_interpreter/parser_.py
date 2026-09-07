from .tokens import TokenType
from .nodes import *
from logger import verbose_log, log

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.advance()

    def raise_error(self):
        raise Exception('Invalid syntax')

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None
    
    def parse(self):
        if self.current_token == None: # Safety check: No inputted tokens
            return None

        result = self.expr()

        if self.current_token != None: # Safety check: If there are still tokens left after parsing, raise an error
            self.raise_error()

        log(f'Post-parse expression: {result}')
        return result
    
    def expr(self):
        '''Groups addition and subtraction tokens into Add and Subtract nodes'''
        result = self.term() # Execute the term() method to handle multiplication and division first

        while self.current_token != None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                result = AddNode(result, self.term())
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                result = SubtractNode(result, self.term())
        
        return result
    
    def term(self):
        '''Groups term tokens into their respective nodes'''
        result = self.factor() # Execute the factor() method to handle parentheses and numbers first

        while self.current_token != None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.POWER):
            if self.current_token.type == TokenType.MULTIPLY:
                self.advance()
                result = MultiplyNode(result, self.factor())
            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                result = DivideNode(result, self.factor())
            elif self.current_token.type == TokenType.POWER:
                self.advance()
                result = PowerNode(result, self.factor())
        
        return result
    
    def factor(self): # PEMDAS
        token = self.current_token
        verbose_log(f"Current token: {token}")

        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()

            if self.current_token.type != TokenType.RPAREN:
                self.raise_error()
            
            self.advance()
            return result

        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)
        
        elif token.type == TokenType.PLUS:
            self.advance()
            return PlusNode(self.factor())
        
        elif token.type == TokenType.MINUS:
            self.advance()
            return MinusNode(self.factor())
        
        self.raise_error() # Catch-all error if none of the above conditions are met
