import ast
from typing import List, Tuple, Optional, Any, Dict
from common.utils import LINTER_MAGIC
from generator.common.source_file_parsing.parsing_commons import add_parents


class UnknownNamesRemoval(ast.NodeVisitor):
    def __init__(self, unknown: set[str]):
        self.unknown = unknown

    # currently able to resolve add_argument calls containing unknown names,
    # and list comprehension assignment
    def _reach_top(self, node: ast.Name) -> Tuple[ast.Call, ast.AST]:
        current = node
        parent = current.parent

        def _reach_add_argument():
            return (isinstance(parent, ast.Call) and
                    isinstance(parent.func, ast.Attribute) and
                    parent.func.attr != "add_argument")

        def _reach_assignment_as_list_comprehension():
            return (isinstance(parent, ast.Assign) and
                    isinstance(current, ast.ListComp))

        while not (_reach_add_argument() or
                   _reach_assignment_as_list_comprehension()):
            current = parent
            parent = current.parent

        return parent, current

    def _fix_name(self, node: ast.Name, name: str):
        parent, current = self._reach_top(node)
        not_found_const = ast.Constant(value=f"{LINTER_MAGIC} Name {name}"
                                                f" could not be loaded")
        # if top is assignment
        if isinstance(parent, ast.Assign):
            print(f"Problem with assignment to {parent.targets[0].id}")
            parent.value = ast.List(elts=[not_found_const],
                                    ctx=ast.Load())
            return

        # this name can be a part of normal args
        if current in parent.args:
            idx = parent.args.index(current)

            parent.args[idx] = not_found_const
            return

        # or a part of keyword args
        current: ast.keyword
        current.value = not_found_const

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id not in self.unknown:
            return

        self._fix_name(node, node.id)


def handle_local_module_names(actions: List[ast.AST],
                              unknown_names: set[str]) -> ast.Module:
    module = ast.Module(body=actions, type_ignores=[])
    add_parents(module)

    removal = UnknownNamesRemoval(unknown_names)
    removal.visit(module)

    return module