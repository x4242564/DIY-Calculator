from .nodes import *
from .values import Number
from logger import verbose_log, log

class Interpreter:

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)
    
    def visit_NumberNode(self, node):
        return Number(node.value)
    
    def visit_AddNode(self, node):
        a = self.visit(node.node_a).value
        b = self.visit(node.node_b).value
        verbose_log(f"{a} + {b} = {a + b}")
        return Number(a + b)

    def visit_SubtractNode(self, node):
        a = self.visit(node.node_a).value
        b = self.visit(node.node_b).value
        verbose_log(f"{a} - {b} = {a - b}")
        return Number(a - b)
    
    def visit_MultiplyNode(self, node):
        a = self.visit(node.node_a).value
        b = self.visit(node.node_b).value
        verbose_log(f"{a} * {b} = {a * b}")
        return Number(a * b)
    
    def visit_DivideNode(self, node):
        try:
            a = self.visit(node.node_a).value
            b = self.visit(node.node_b).value
            verbose_log(f"{a} / {b} = {a / b}")
            return Number(a / b)
        except: # If dividing by zero
            raise Exception('Runtime math error')
    
    def visit_PlusNode(self, node):
        a = self.visit(node.node).value
        verbose_log(f"+{a} = {+ a}")
        return Number(+ a)

    def visit_MinusNode(self, node):
        a = self.visit(node.node).value
        verbose_log(f"-{a} = {0 - a}")
        return Number(0 - a)
    
    def visit_PowerNode(self, node):
        a = self.visit(node.node_a).value
        b = self.visit(node.node_b).value
        verbose_log(f"{a} ** {b} = {a ** b}")
        return Number(a ** b)