#!/usr/bin/env python3
import ast
from pprint import pprint


class SymbolTable(ast.NodeVisitor):
    """
    Example of Imperative Symbol Table
    """

    def __init__(self):
        self.table = [{}]

    def push(self):
        self.table.append({})

    def pop(self) -> dict:
        return self.table.pop()

    def declare(self, var_name, var_type):
        self.table[-1][var_name] = var_type

    def visit_FunctionDef(self, node):
        self.push()
        for arg in node.args.args:
            self.declare(arg.arg, 'unknown')  # don't care about arg type
        self.generic_visit(node)
        self.pop()

    def visit_If(self, node):
        self.push()
        self.generic_visit(node)
        self.pop()

    def visit_For(self, node):
        self.push()
        self.declare(node.target.id, 'unknown')  # don't care about iter type
        self.generic_visit(node)
        self.pop()

    def visit_While(self, node):
        self.push()
        self.generic_visit(node)
        self.pop()

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Num):
            var_type = type(node.value.n).__name__
        elif isinstance(node.value, ast.Str):
            var_type = type(node.value.s).__name__
        elif isinstance(node.value, ast.List):
            var_type = 'list'
        elif isinstance(node.value, ast.Dict):
            var_type = 'dict'
        else:
            var_type = 'unknown'
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.declare(target.id, var_type)
        self.generic_visit(node)

    def generic_visit(self, node):
        super().generic_visit(node)

        print(node.__class__.__name__)
        pprint(self.table)


def build_symbol_table(code: str) -> None:
    tree = ast.parse(code)
    symbol_table = SymbolTable()
    symbol_table.visit(tree)


code = """
def func():
    x = 5
    y = 'hello'

z = [1, 2, 3]
a = {'a': 1, 'b': 2}

if True:
    i = 10

for j in range(10):
    pass

while False:
    k = 20
"""

build_symbol_table(code)
