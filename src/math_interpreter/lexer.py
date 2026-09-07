from .tokens import Token, TokenType
from logger import log, verbose_log

WHITESPACE = ' \n\t' # space, new line, and tab characters
DIGITS = '1234567890'

class Lexer:
    '''Writes and feeds tokens to the parser one by one'''
    def __init__(self, text):
        self.text = iter(text) # breaks text down into items in a list
        self.current_char = None
        self.advance() # advances to the first character in the text

    def advance(self):
        '''Advances to next character until the end of the text or an error occurs'''
        try:
            if self.current_char != None:
                verbose_log(f"Current char: {self.current_char}")
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_number(self):
            '''Handles defining number tokens with its numerical value'''
            decimal_count = 0
            number_str = self.current_char
            self.advance()

            while self.current_char != None and (self.current_char == '.' or self.current_char in DIGITS):
                if self.current_char == '.':
                    decimal_count += 1
                    if decimal_count > 1:
                        break

                number_str += self.current_char
                self.advance()

            if number_str.startswith('.'):
                number_str = '0' + number_str
            if number_str.endswith('.'):
                number_str = number_str + '0'
            return Token(TokenType.NUMBER, float(number_str))

    def generate_tokens(self):
        '''Iterates through text and defines tokens with their corresponding type'''
        while self.current_char != None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char == '.' or self.current_char in DIGITS:
                yield self.generate_number()
            elif self.current_char == '+':
                self.advance()
                yield Token(TokenType.PLUS)
            elif self.current_char == '-':
                self.advance()
                yield Token(TokenType.MINUS)
            elif self.current_char == '*':
                self.advance()
                yield Token(TokenType.MULTIPLY)
            elif self.current_char == '/':
                self.advance()
                yield Token(TokenType.DIVIDE)
            elif self.current_char == '^':
                self.advance()
                yield Token(TokenType.POWER)
            elif self.current_char == '(':
                self.advance()
                yield Token(TokenType.LPAREN)
            elif self.current_char == ')':
                self.advance()
                yield Token(TokenType.RPAREN)
            else:
                raise Exception(f'Illegal character: "{self.current_char}"')

        log(f"Tokens generated sucessfully")
