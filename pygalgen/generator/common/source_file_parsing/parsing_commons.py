"""
Module containing the parent class of Dicovery classes
"""
import abc
import ast
from typing import List, Tuple

class Discovery(ast.NodeVisitor, abc.ABC):
    def __init__(self, actions: List[ast.AST]):
        self.actions = actions

    @abc.abstractmethod
    def report_findings(self) -> Tuple:
        pass

def add_parents(tree: ast.AST):
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

def create_module_tree(path: str) -> ast.Module:
    with open(path, mode="r", encoding="utf-8") as file:
        tree = ast.parse(file.read())
        add_parents(tree)
        return tree
