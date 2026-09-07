# DIY-Calculator

## Overview

This project is a simple calculator built around a custom python math interpreter. Instead of relying on Python's built-in `eval`, it breaks mathematical input into tokens, organizes those tokens into a node tree, and then evaluates the tree step by step.

This pattern is common in calculators, scripting languages, formula engines, and domain-specific languages. It makes it easier to support arithmetic precedence, parentheses, unary operations, and validation of invalid input.

List of functions:
- Operators:
    - `^`: Exponential
    - `/`: Divison
    - `*`: Multiplication
    - `-`: Subtraction
    - `+`: Addition
- `Ans`: Inserts last equation's evaluation
- `Del`: Deletes last input
- `C`: Deletes all inputs

The calculator does **not** support parenthesis multiplication *yet*. For example: `4(2)` will raise an `invalid syntax` error and return `None`. 

## Tkinter Calculator UI

The project uses Python's built-in `tkinter` package to build a lightweight calculator interface. The UI is designed to build expressions with the number and operator buttons, then pass them into the interpreter pipeline. The GUI is pretty simple at the moment and more focused on demonstrating how a front-end input can connect to a back-end evaluator.

## How the Interpreter Works

### Lexer

The lexer is responsible for reading raw input text and turning it into meaningful tokens. It scans each character and groups them into recognized pieces such as numbers, operators, parentheses, and whitespace. For example, the input `3 + 4 * (2 - 1)` is converted into a sequence of token objects representing numbers and operators.

```
[(NUMBER: 3), (PLUS), (NUMBER: 4), (MULTIPLY), (LPAREN), (NUMBER: 2), (MINUS), (NUMBER: 1), (RPAREN)]
```

### Parser

The parser takes the token stream produced by the lexer and builds an expression tree. It applies PEMDAS precedence so that multiplication and division are handled before addition and subtraction, and parentheses override normal ordering.

This stage is where the structure of an expression becomes explicit. For example, the parser can turn:

```
3 + 4 * (2 - 1)
```

into a tree of nodes representing the correct math structure, and correctly evaluate it as:

```
(3.0 + (4.0 * (2.0 - 1.0)))
```

### Interpreter

The interpreter walks the generated parse tree and evaluates it recursively. Each node type has a corresponding visit method that performs its operation, such as addition, subtraction, multiplication, division, or exponentiation.

Once evaluation is complete, the interpreter returns the final numeric result, which the calculator UI can display to the user.

## Unit Testing

The project includes unit tests for both the lexer and parser behavior. These tests were especially valuable because they helped reveal subtle bugs that were easy to miss during manual testing.

The lexer tests helped confirm that numbers, whitespace handling, and token generation were behaving correctly. The parser tests helped verify that arithmetic expressions were being constructed with the right precedence and structure, including nested expressions and multi-step operations.

The payoff from these tests were almost instant. While testing my assertions I discovered a couple bugs in the parser and lexer that completely went over my head during manual testing.

## Verbose Logging

You can configure the logging in `src/logger.py`. This may help with gaining a better understanding of how the interpreter works, certainly helped me further my understanding.

`logging` is enabled by default and shows the minimal steps the interpreter took to solve the given expression. Enable `verbose` to see more detail on the interpreter's process.

## Requirements

To run this project, you need:

- Python ^3.8

## Running the Program

From the project root, run:

```bash
cd src
python calc.py
```

You can also run the automated tests with

```bash
cd src
python -m unittest discover -s test -p "*_test.py"
```

## Summary

This project demonstrates a practical way to build a calculator using a custom interpreter architecture: the user enters math, the lexer tokenizes it, the parser structures it, and the interpreter evaluates it. With a simple `tkinter` UI layered on top, the project becomes a clear, hands-on example of how interpreters and calculators work together.

Thanks to [@davidcallanan](https://github.com/davidcallanan) for the great [math interpreter tutorial](https://www.youtube.com/watch?v=88lmIMHhYNs&list=PLJp-g8uP8qlaZZiJ2gy-DiVbqXlWglrnP)
