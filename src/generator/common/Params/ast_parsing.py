import ast
from typing import Tuple, Optional, Any, Set


class ParserDiscovery(ast.NodeVisitor):
    def __init__(self):
        self.parser_names = set()
        self.parser_actions = []

    def is_this_argparse(self, node: ast.Assign) -> \
            Tuple[bool, Optional[str]]:

        if not (len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name)):
            return False, None

        name = node.targets[0].id

        if not (isinstance(node.value, ast.Call) and
                hasattr(node.value.func, "id") and
                node.value.func.id == "ArgumentParser"):
            return False, None

        return True, name

    def visit_Assign(self, node: ast.Assign):
        # visit into children of this node is not necessary
        is_argparse, name = self.is_this_argparse(node)
        if is_argparse:
            self.parser_names.add(name)
            self.parser_actions.append(node)
        self.generic_visit(node)


class SectionDiscovery(ast.NodeVisitor):
    def __init__(self, parser_names: Set[str]):
        self.parser_names = parser_names
        self.sections = set()
        self.parser_actions = []

    def is_this_group_creation(self, node: ast.Assign):
        if not (len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name)):
            return False, None

        name = node.targets[0].id
        if not (isinstance(node.value, ast.Call) and
                hasattr(node.value.func, "attr") and
                node.value.func.attr == "add_argument_group"):
            return False, None

        if node.value.func.value.id not in self.parser_names:
            print(f"Cant ensure that '{list(self.parser_names)[0]}' is the only parser"
                  f" because of use of this parser:"
                  f" {node.value.func.value.id}")
            self.parser_names.add(node.value.func.value.id)

        return True, name

    def visit_Assign(self, node: ast.Assign) -> Any:
        is_group_creation, name = self.is_this_group_creation(node)
        if is_group_creation:
            self.sections.add(name)
            self.parser_actions.append(node)


class ArgumentCreationDiscovery(ast.NodeVisitor):
    def __init__(self, sections: Set[str], parser_names: Set[str]):
        self.sections = sections
        self.parser_names = parser_names
        self.parser_actions = []

    def is_call_on_parser_or_group(self, node: ast.Call):
        return hasattr(node.func, "attr") and \
               node.func.attr == "add_argument" and \
               (node.func.value.id in self.sections or
                node.func.value.id in self.parser_names)

    def visit_Call(self, node: ast.Call) -> Any:
        if self.is_call_on_parser_or_group(node):
            self.parser_actions.append(ast.Expression(node))

        self.generic_visit(node)


def main():
    with open("../../main.py", "r") as source:
        tree = ast.parse(source.read())

    actions = []
    analyzer = ParserDiscovery()
    analyzer.visit(tree)
    actions += analyzer.parser_actions

    parser_names = analyzer.parser_names

    analyzer = SectionDiscovery(parser_names)
    analyzer.visit(tree)
    actions += analyzer.parser_actions

    analyzer = ArgumentCreationDiscovery(analyzer.sections, parser_names)
    analyzer.visit(tree)
    actions += analyzer.parser_actions



    print()


if __name__ == "__main__":
    main()
