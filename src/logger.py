import logging
import os
import sys

logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(tag)s] %(message)s")

terminal_handler = logging.StreamHandler(sys.stdout)
terminal_handler.setFormatter(formatter)

logger.addHandler(terminal_handler)

isLogging = True
isVerbose = True

ansi = {
    "RED" : "\033[31m",
    "GREEN" : "\033[32m",
    "YELLOW" : "\033[33m",
    "BLUE" : "\033[34m",
    "RESET" : "\033[0m" # resets color to default
}

color = {
    "main.py" : ansi["RED"],
    "calc.py" : ansi["RED"],
    "lexer.py" : ansi["GREEN"],
    "tokens.py" : ansi["GREEN"],
    "parser_.py" : ansi["YELLOW"],
    "nodes.py" : ansi["YELLOW"],
    "interpreter.py" : ansi["BLUE"],
}

def log(text):
    '''For making INFO logs'''
    if isLogging:
        logger.info(text, extra={"tag": "LOG"})

def verbose_log(text):
    '''For making verbose INFO logs'''
    if isVerbose and isLogging:
        filename = os.path.basename(sys._getframe(1).f_code.co_filename)
        tag_color = color.get(filename, ansi["RESET"])
        tag = f"-v LOG {tag_color}{filename}{ansi['RESET']}"
        logger.info(text, extra={"tag": tag})

def error_log(text):
    '''For making ERROR logs'''
    if isLogging:
        logger.error(text, extra={"tag": f"{ansi['RED']}ERROR{ansi['RESET']}"})

_log_view = None

def register_log_view(add_log_fn):
    '''Gets the add_log method from the LogViewer widget'''
    global _log_view
    _log_view = add_log_fn

def update_log_view(text):
    '''Calls LogViewer method to append logs into the text field'''
    if _log_view is not None:
        _log_view(text)

class TkLogHandler(logging.Handler):
    '''Mirrors log records into LogViewer widget'''

    def emit(self, record):
        update_log_view(self.format(record) + "\n")

tk_handler = TkLogHandler()
tk_handler.setFormatter(formatter)
logger.addHandler(tk_handler)
