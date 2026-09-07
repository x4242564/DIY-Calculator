from math_interpreter import lexer, parser_, interpreter

from logger import log, error_log, verbose_log
import traceback
import os

def evaluate(text):
    try:
        lex = lexer.Lexer(text)
        tokens = lex.generate_tokens()
        parser = parser_.Parser(tokens)
        tree = parser.parse()
        interp = interpreter.Interpreter()
        value = interp.visit(tree)
        log(f"calculated result: {value}")
        if value.is_integer():
            value.int()  # Removes decimal point if the value is an integer
        return value
    except Exception as e: # catch errors and point to their origin
        tb = e.__traceback__
        while tb.tb_next: # find the frame of origin (inner-most)
            tb = tb.tb_next
        
        frame = tb.tb_frame
        code = frame.f_code
        filename = os.path.basename(code.co_filename)
        line_number = tb.tb_lineno
        function_name = code.co_name
        error_log(f"{e} ({os.path.splitext(filename)[0]})")
        verbose_log(f"Error origin: {filename} {function_name}() Line: {line_number}")

def main():
    print("-----------Terminal Calculator-----------")
    while True:
        equation = input("enter equation (\"q\" to quit): ")
        if equation == "q": break
        eval = evaluate(equation)
        if eval: print(f'{equation} = {eval}\n')

if __name__ == "__main__":
    main()
