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


class ImportDiscovery(Discovery):
    """
    Class responsible for discovery and extraction of import statements
    """
    def __init__(self, actions: List[ast.AST]):
        super(ImportDiscovery, self).__init__(actions)
        self.argparse_module_alias: Optional[str] = None
        self.argument_parser_alias: Optional[str] = None

    def visit_Import(self, node: ast.Import) -> Any:
        for item in node.names:
            if item.name == ARGPARSE_MODULE_NAME:
                alias = item.asname if item.asname is not None \
                    else ARGPARSE_MODULE_NAME
                self.argparse_module_alias = alias
                self.actions.append(node)
                return

            # stdlib modules should be also imported during this step
            if item.name in sys.stdlib_module_names:
                self.actions.append(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        if node.module is None:
            return

        for name in node.module.split("."):
            if name in sys.stdlib_module_names and name != \
                    ARGPARSE_MODULE_NAME:
                self.actions.append(node)
                return

        if ARGPARSE_MODULE_NAME not in node.module:
            return

        for item in node.names:
            if item.name == ARGUMENT_PARSER_CLASS_NAME:
                alias = item.asname if item.asname is not None \
                    else ARGUMENT_PARSER_CLASS_NAME
                self.argument_parser_alias = alias
                self.actions.append(node)
                return

        # stdlib modules should be also imported during this step

    def report_findings(self) -> Tuple:
        if self.argparse_module_alias is None and \
                self.argument_parser_alias is None:
            raise ArgParseImportNotFound

        return (self.actions, self.argparse_module_alias,
                self.argument_parser_alias)


class ParserDiscovery(Discovery):
    """
    Class responsible for discovery of ArgumentParser creation and assignment
    """
    class ParserRenameFinder(ast.NodeVisitor):
        def __init__(self, func_name: str):
            self.func_name = func_name
            self.arg_pos: Optional[int] = None
            self.keyword = Optional[str] = None

        def find_by_argument_pos(self, tree: ast.AST, n: int):
            self.arg_pos = n
            self.keyword = None
            self.visit(tree)

    def __init__(self, actions: List[ast.AST], argparse_alias: Optional[str],
                 argument_parser_alias: Optional[str]):
        self.argument_parser_alias = argument_parser_alias
        self.argparse_module_alias = argparse_alias
        self.main_parser_name: Optional[str] = None

        super(ParserDiscovery, self).__init__(actions)

    # checks whether this assignment creates argument parser,
    # and removes any arguments from the constructor,
    # because they should not be needed
    def is_this_argparse(self, node: ast.Assign) -> \
            Tuple[bool, Optional[str]]:

        if not (len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name)):
            return False, None

        name = node.targets[0].id

        # ArgumentParser was imported using from ... import
        if (isinstance(node.value, ast.Call) and
                isinstance(node.value.func, ast.Name) and
                node.value.func.id == self.argument_parser_alias):
            node.value.keywords = []
            node.value.args = []
            return True, name

        # ArgumentParser is created using attribute call on imported module
        if (isinstance(node.value, ast.Call) and
                isinstance(node.value.func, ast.Attribute) and
                node.value.func.attr == ARGUMENT_PARSER_CLASS_NAME and
                node.value.func.value.id == self.argparse_module_alias):
            node.value.args = []
            node.value.keywords = []
            return True, name

        return False, None

    def visit_Assign(self, node: ast.Assign):
        # visit into children of this node is not necessary
        is_argparse, name = self.is_this_argparse(node)
        if is_argparse:
            self.main_parser_name = name
            self.actions.append(node)

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

    @staticmethod
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

    def visit_Assign(self, node: ast.Assign):
        is_group_creation, name = self.is_this_group_creation(node)
        if is_group_creation:
            self.groups.add(name)
            self.actions.append(node)

    def report_findings(self) -> Tuple:
        return self.actions, self.main_name, self.groups


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
                node.func.value.id ==self.main_name)

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

    def report_findings(self) -> Tuple:
        return self.actions, self.main_name, self.sections


def get_parser_init_and_actions(source: ast.Module) -> \
        Tuple[List[ast.AST], str, Set[str]]:
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
    discovery_classes = [ImportDiscovery, ParserDiscovery,
                         GroupDiscovery, ArgumentCreationDiscovery]

    findings = [],
    for cls in discovery_classes:
        discovery = cls(*findings)
        discovery.visit(source)
        findings = discovery.report_findings()

    actions, main_name, sections = findings

    return actions, main_name, sections
