from dataclasses import dataclass

@dataclass
class Number:
    value: float

    def __repr__(self):
        return f'{self.value}'

    def is_integer(self):
        return self.value.is_integer()

    def int(self):
        self.value = int(self.value)
