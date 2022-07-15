"""
Module responsible for discovery of import statements importing Argument parser
and discovery of the statements initializing the parser itself
"""
import ast
import sys
from typing import Tuple, Optional, Any, Set, List
from .parsing_exceptions import ArgParseImportNotFound, ArgParserNotUsed
from .parsing_commons import Discovery

ARGPARSE_MODULE_NAME = "argparse"
ARGUMENT_PARSER_CLASS_NAME = "ArgumentParser"


def is_this_argparse(argument_parser_alias: str, argparse_module_alias: str,
                     node: ast.Assign) -> \
        Tuple[bool, Optional[str]]:
    if not (len(node.targets) == 1 and
            isinstance(node.targets[0], ast.Name)):
        return False, None

    name = node.targets[0].id

    # ArgumentParser was imported using from ... import
    if (isinstance(node.value, ast.Call) and
            isinstance(node.value.func, ast.Name) and
            node.value.func.id == argument_parser_alias):
        return True, name

    # ArgumentParser is created using attribute call on imported module
    if (isinstance(node.value, ast.Call) and
            isinstance(node.value.func, ast.Attribute) and
            node.value.func.attr == ARGUMENT_PARSER_CLASS_NAME and
            node.value.func.value.id == argparse_module_alias):
        return True, name

    return False, None


def is_this_group_creation(node: ast.Assign):
    if not (len(node.targets) == 1 and
            isinstance(node.targets[0], ast.Name)):
        return False, None

    name = node.targets[0].id
    if not (isinstance(node.value, ast.Call) and
            isinstance(node.value.func, ast.Attribute) and
            node.value.func.attr == "add_argument_group"):
        return False, None

    return True, name


class ImportDiscovery(Discovery):
    """
    Class responsible for discovery and extraction of import statements
    """

    def __init__(self, actions: List[ast.AST]):
        super(ImportDiscovery, self).__init__(actions)
        self.argparse_module_alias: Optional[str] = None
        self.argument_parser_alias: Optional[str] = None
        self.imported_names: Set[str] = set()

    def visit_Import(self, node: ast.Import) -> Any:
        for item in node.names:
            if item.name == ARGPARSE_MODULE_NAME:
                alias = item.asname if item.asname is not None \
                    else ARGPARSE_MODULE_NAME
                self.argparse_module_alias = alias
                self.actions.append(node)
                self.imported_names.add(item.name)
                return

            # stdlib modules should be also imported during this step
            if item.name in sys.stdlib_module_names:
                self.actions.append(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        if node.module is None:
            return

        # look for argparse import (or any imports from stdlib) and import them
        for name in node.module.split("."):
            name_in_known_modules = name in sys.stdlib_module_names
            if name_in_known_modules:
                self.actions.append(node)
                for item in node.names:
                    alias = item.asname or item.name
                    self.imported_names.add(alias)
                    # in case argparse is being imported, determine the
                    # alias of the parser, if there is any
                    if name == ARGPARSE_MODULE_NAME and \
                            item.name == ARGUMENT_PARSER_CLASS_NAME:
                        self.argument_parser_alias = alias
                        self.actions.append(node)

    def report_findings(self) -> Tuple[List[ast.AST], str, str, Set[str]]:
        if self.argparse_module_alias is None and \
                self.argument_parser_alias is None:
            raise ArgParseImportNotFound

        return (self.actions, self.argparse_module_alias,
                self.argument_parser_alias, self.imported_names)


class SimpleParserDiscovery(Discovery):
    """
        Class responsible for discovery of ArgumentParser creation
        and assignment
    """

    def __init__(self, actions: List[ast.AST], argparse_alias: Optional[str],
                 argument_parser_alias: Optional[str]):
        self.argument_parser_alias = argument_parser_alias
        self.argparse_module_alias = argparse_alias
        self.main_parser_name: Optional[str] = None
        self.argparse_found = False

        super(SimpleParserDiscovery, self).__init__(actions)

    def visit_Assign(self, node: ast.Assign):
        if self.argparse_found:
            return
        # visit into children of this node is not necessary
        is_argparse, name = is_this_argparse(self.argument_parser_alias,
                                             self.argparse_module_alias, node)
        if is_argparse:
            self.main_parser_name = name
            self.actions.append(node)
            self.argparse_found = True

    def report_findings(self) -> Tuple:
        if self.main_parser_name is None:
            raise ArgParserNotUsed

        return self.actions, self.main_parser_name


# this visitor class goes through the tree and tries to find creation of
# all argument groups
# it works only if the group is assigned a name
# (is created as a normal variable)
class GroupDiscovery(Discovery):
    """
    Class responsible for discovery of statements that initialize argument
    groups
    """

    def __init__(self, actions: List[ast.AST], main_name: str):
        self.main_name = main_name
        self.groups = set()
        super(GroupDiscovery, self).__init__(actions)

    def visit_Assign(self, node: ast.Assign):
        is_group_creation, name = is_this_group_creation(node)
        if is_group_creation:
            self.groups.add(name)
            self.actions.append(node)

    def report_findings(self) -> Tuple:
        return self.actions, self.groups


# # this visitor goes through all calls and extracts those to argument
# parser and groups. IMPORTANT! it also renames parsers on which those calls
# are called to ensure everything can be interpreted correctly
class ArgumentCreationDiscovery(Discovery):
    """
    Class responsible for extraction of statements which initialize the input
    arguments. It is able to extract function calls on the original parser,
    and on the argument groups extracted by GroupDiscovery
    """

    def __init__(self, actions: List[ast.AST], main_name: str,
                 groups: Set[str]):
        self.main_name = main_name
        self.sections = groups
        super(ArgumentCreationDiscovery, self).__init__(actions)

    def is_call_on_parser_or_group(self, node: ast.Call):
        return isinstance(node.func, ast.Attribute) and \
               node.func.attr == "add_argument" and \
               (node.func.value.id in self.sections or
                node.func.value.id == self.main_name)

    def visit_Call(self, node: ast.Call) -> Any:
        if self.is_call_on_parser_or_group(node):
            assert isinstance(node.func, ast.Attribute)
            # name of the variable needs to be rewritten,
            # because we want to use only one parser
            if node.func.value.id != self.main_name and \
                    node.func.value.id not in self.sections:
                node.func.value.id = self.main_name

            self.actions.append(ast.Expr(node))

        self.generic_visit(node)

    def report_findings(self) -> List[ast.AST]:
        return self.actions


def get_parser_init_and_actions(source: ast.Module) -> \
        Tuple[List[ast.AST], str, Set[str], Set[str]]:
    """
    Function used to extract necessary imports, parser and argument creation
     function calls

    Parameters
    ----------
    source : ast.Module
     source file parsed into ATT

    Returns
    -------
    List of extracted AST nodes, the main name of the parser and a set of
    section names
    """
    discovery_classes = [ImportDiscovery, SimpleParserDiscovery,
                         GroupDiscovery, ArgumentCreationDiscovery]
    actions = []
    import_discovery = ImportDiscovery(actions)
    import_discovery.visit(source)
    actions, argparse_module_alias, argparse_class_alias, imported_names = \
        import_discovery.report_findings()

    parser_discovery = SimpleParserDiscovery(actions, argparse_module_alias,
                                             argparse_class_alias)
    parser_discovery.visit(source)
    actions, parser_name = parser_discovery.report_findings()

    group_discovery = GroupDiscovery(actions, parser_name)
    group_discovery.visit(source)
    actions, groups = group_discovery.report_findings()

    argument_creation = ArgumentCreationDiscovery(actions, parser_name, groups)
    argument_creation.visit(source)
    actions = argument_creation.report_findings()

    return actions, parser_name, groups, imported_names
