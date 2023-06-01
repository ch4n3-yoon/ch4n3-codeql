#!/usr/bin/env python3

import ast
import sys


class ReDoS_Checker(ast.NodeVisitor):
    def __init__(self):
        self.suspicious_patterns = []

    def visit_Call(self, node):
        # Check if it's a call to re.compile, re.match, re.search or re.fullmatch
        if isinstance(node.func, ast.Attribute) and node.func.attr in {'compile', 'match', 'search', 'fullmatch'}:
            if isinstance(node.func.value, ast.Name) and node.func.value.id == 're':
                if node.args:
                    regex_pattern = node.args[0]
                    if isinstance(regex_pattern, ast.Str):
                        pattern = regex_pattern.s
                        if self.is_suspicious(pattern):
                            self.suspicious_patterns.append((node.lineno, pattern))
        self.generic_visit(node)

    def is_suspicious(self, pattern):
        # A very simple heuristic to identify suspicious patterns.
        # This might give some false positives and false negatives.
        return '.*' in pattern or '.+' in pattern or '{.,}' in pattern or '.*?' in pattern


def check_file(filename):
    with open(filename, 'r') as f:
        tree = ast.parse(f.read())
    checker = ReDoS_Checker()
    checker.visit(tree)
    return checker.suspicious_patterns


def main():
    filename = sys.argv[1]
    suspicious_patterns = check_file(filename)
    if suspicious_patterns:
        print(f"Suspicious patterns found in {filename}:")
        for lineno, pattern in suspicious_patterns:
            print(f"Line {lineno}: {pattern}")
    else:
        print(f"No suspicious patterns found in {filename}.")


if __name__ == "__main__":
    main()
