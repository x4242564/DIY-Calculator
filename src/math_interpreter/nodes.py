from dataclasses import dataclass
from logger import verbose_log, log

@dataclass
class NumberNode:
    value: float

    def __repr__(self):
        return f'{self.value}'

    def __post_init__(self):
        verbose_log(f"{self.__class__.__name__} generated: {self}")
    
@dataclass
class AddNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f'({self.node_a}+{self.node_b})'

    def __post_init__(self):
        verbose_log(f"{self.__class__.__name__} generated: {self}")
    
@dataclass
class SubtractNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f'({self.node_a}-{self.node_b})'
    
    def __post_init__(self):
        verbose_log(f"{self.__class__.__name__} generated: {self}")

@dataclass
class MultiplyNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f'({self.node_a}*{self.node_b})'

    def __post_init__(self):
        verbose_log(f"{self.__class__.__name__} generated: {self}")
    
@dataclass
class DivideNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f'({self.node_a}/{self.node_b})'

    def __post_init__(self):
        verbose_log(f"{self.__class__.__name__} generated: {self}")

@dataclass
class PowerNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f'({self.node_a}^{self.node_b})'

    def __post_init__(self):
        verbose_log(f"{self.__class__.__name__} generated: {self}")

@dataclass
class PlusNode:
    node: any

    def __repr__(self):
        return f'(+{self.node})'
    
    def __post_init__(self):
        verbose_log(f"{self.__class__.__name__} generated: {self}")

@dataclass
class MinusNode:
    node: any
    
    def __repr__(self):
        return f'(-{self.node})'

    def __post_init__(self):
        verbose_log(f"{self.__class__.__name__} generated: {self}")