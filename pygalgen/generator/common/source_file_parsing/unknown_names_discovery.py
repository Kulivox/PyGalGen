"""
Module containing discovery classes used to find names
(assignments to variables) that have not been extracted yet
"""
import ast
from .parsing_commons import Discovery
from typing import Tuple, List, Any, Set
import sys
import builtins


class UnknownNamesDiscovery(Discovery):
    """
    Discovery class used to find names that have not been initialized yet but
    are necessary for correct argument parser init
    """

    def __init__(self, actions: List[ast.AST], known_names: Set[str]):
        super().__init__(actions)
        self.known_names = known_names
        self.unknown_names = set()

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        return

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id not in self.known_names:
            self.unknown_names.add(node.id)

    def visit_For(self, node: ast.For) -> Any:
        for item in node.body:
            self.generic_visit(item)

    def visit_ListComp(self, node: ast.ListComp) -> Any:
        for comprehension in node.generators:
            if isinstance(comprehension.target, ast.Name):
                self.known_names.add(comprehension.target.id)

        self.generic_visit(node)

    def report_findings(self) -> Tuple:
        return self.unknown_names,


class UnknownNameInit(ast.NodeVisitor):
    """
    Class used to initialize unknown names
    """

    def __init__(self, unknown_names: Set[str]):
        self.unknown_names = unknown_names
        self.class_definitions = []
        self.variable_definitions = []
        self.new_known_names = set()

    # assignment of variables
    def visit_Assign(self, node: ast.Assign) -> Any:
        target, = node.targets

        if isinstance(target, ast.Name) and target.id in self.unknown_names:
            self.variable_definitions.append(node)
            self.new_known_names.add(target.id)

    # if members of class are used, class definition has to be a
    # part of actions
    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        if node.name in self.unknown_names:
            self.class_definitions.append(node)
            self.new_known_names.add(node.name)

    def report_findings(self) -> Tuple:
        return self.variable_definitions, self.class_definitions, \
               self.new_known_names


def _insert_into_actions(actions: List[ast.AST], assignments: List[ast.Assign],
                         class_defs: List[ast.ClassDef]):
    def find_end_of_imports():
        index = 0
        for item in actions:
            if not (isinstance(item, ast.Import) or
                    isinstance(item, ast.ImportFrom)):
                return index

            index += 1

        return index

    end_of_imports = find_end_of_imports()
    if assignments:
        actions.insert(end_of_imports, *assignments)

    if class_defs:
        actions.insert(end_of_imports, *class_defs)


def initialize_variables_in_module(module_tree: ast.Module,
                                   parser_name: str,
                                   sections: Set[str],
                                   actions: List[ast.AST]) ->\
        Tuple[List[ast.AST], Set[str]]:
    """
    Function used to initialize variables that have constant values

    Parameters
    ----------
    module_tree : ast.Module
     AST of the original source file
    parser_name : str
     default name of the parser
    sections : Set[str]
     set of section names
    actions : List[ast.AST]
     list of actions extracted so far

    Returns
    -------
    List containing newly extracted actions and new unknown names
    """
    builtin_names = [e for e in builtins.__dict__]
    lib_modules = sys.stdlib_module_names

    # this is a set of all known names, basically the things that are already
    # known and don't have to be added to the list of actions
    known_names = {parser_name, *sections,
                   *builtin_names, *lib_modules}

    unknown_names_discovery = UnknownNamesDiscovery(actions, known_names)
    module = ast.Module(body=actions, type_ignores=[])
    unknown_names_discovery.visit(module)

    unknown_names, = unknown_names_discovery.report_findings()

    unknown_names_loader = UnknownNameInit(unknown_names)
    unknown_names_loader.visit(module_tree)
    new_vars, new_classes, new_known_names = \
        unknown_names_loader.report_findings()

    # after unknown names initialization is complete, new known_names set is
    # created and new actions are added to the action list
    known_names = known_names.union(new_known_names)
    _insert_into_actions(actions, new_vars, new_classes)
    module.body = actions

    unknown_names_discovery = UnknownNamesDiscovery(actions, known_names)
    unknown_names_discovery.visit(module)
    unknown_names, = unknown_names_discovery.report_findings()
    return actions, unknown_names
