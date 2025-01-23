class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, value):
        if name in self.symbols:
            raise ValueError(f"Variable '{name}' already declared.")
        self.symbols[name] = value

    def assign(self, name, value):
        if name not in self.symbols:
            raise ValueError(f"Variable '{name}' not declared.")
        self.symbols[name] = value

    def lookup(self, name):
        if name not in self.symbols:
            raise ValueError(f"Variable '{name}' not declared.")
        return self.symbols[name]