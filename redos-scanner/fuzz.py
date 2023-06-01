#!/usr/bin/env python3
import re
import ast
import sys
import time
import atheris

with atheris.instrument_imports():
    import re
    import ast
    import sys
    import time


class RegexExtractor(ast.NodeVisitor):
    def __init__(self):
        self.regexes = []

    def visit_Call(self, node):
        # Check if it's a call to re.compile, re.match, re.search or re.fullmatch
        if isinstance(node.func, ast.Attribute) and node.func.attr in {'compile', 'match', 'search', 'fullmatch'}:
            if isinstance(node.func.value, ast.Name) and node.func.value.id == 're':
                if node.args:
                    regex_pattern = node.args[0]
                    if isinstance(regex_pattern, ast.Str):
                        self.regexes.append(regex_pattern.s)

        self.generic_visit(node)


def extract_regexes_from_file(filename):
    with open(filename, 'r') as f:
        tree = ast.parse(f.read())
    extractor = RegexExtractor()
    extractor.visit(tree)
    return extractor.regexes


def fuzz_with_timeout(pattern, data):
    if isinstance(data, bytes):
        data = data.decode("utf-8")

    start = time.time()
    try:
        atheris.enabled_hooks.add("RegEx")
        re.match(pattern, data)
    except re.error:
        pass
    duration = time.time() - start
    return duration


@atheris.instrument_func
def test_one_input(data):
    fdp = atheris.FuzzedDataProvider(data)
    random_input = fdp.ConsumeUnicode(atheris.ALL_REMAINING)  # Consume all remaining bytes as Unicode
    for pattern in patterns:
        duration = fuzz_with_timeout(pattern, random_input)
        if duration > 0.5:  # If it takes more than 0.5 seconds, print it out
            print(f"Suspicious pattern: {pattern}")


def main():
    global patterns
    filename = 'target.py'
    patterns = extract_regexes_from_file(filename)
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
