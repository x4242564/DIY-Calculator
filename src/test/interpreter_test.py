import unittest
from math_interpreter.nodes import *
from math_interpreter.interpreter import Interpreter
from math_interpreter.values import Number


class TestInterpreter(unittest.TestCase):

    def __int__(self):
        pass

    def test_number_node(self):
        value = Interpreter().visit(NumberNode(42.42))
        self.assertEqual(value, Number(42.42))

    def test_individual_operations(self):
        value = Interpreter().visit(AddNode(NumberNode(4), NumberNode(2)))
        self.assertEqual(value, Number(6))

        value = Interpreter().visit(PlusNode(NumberNode(42)))
        self.assertEqual(value, Number(42))

        value = Interpreter().visit(SubtractNode(NumberNode(4), NumberNode(2)))
        self.assertEqual(value, Number(2))

        value = Interpreter().visit(MinusNode(NumberNode(42)))
        self.assertEqual(value, Number(-42))

        value = Interpreter().visit(MultiplyNode(NumberNode(4), NumberNode(2)))
        self.assertEqual(value, Number(8))

        value = Interpreter().visit(PowerNode(NumberNode(4), NumberNode(2)))
        self.assertEqual(value, Number(16))

        value = Interpreter().visit(DivideNode(NumberNode(4), NumberNode(242)))
        self.assertAlmostEqual(value.value, 0.01653, 5)

        with self.assertRaises(Exception): # assert that dividing by zero raises an exception
            Interpreter().visit(DivideNode(NumberNode(42), NumberNode(0)))

    def test_full_expression(self): # tests a full expression with multiple operations
        # 3 + 4 * (7 - 1) / 3
        tree = AddNode(
                NumberNode(3),
                DivideNode(
                    MultiplyNode(NumberNode(4), SubtractNode(NumberNode(7), NumberNode(1))),
                    NumberNode(3)
                )
            )

        result = Interpreter().visit(tree)
        self.assertEqual(result, Number(11))
