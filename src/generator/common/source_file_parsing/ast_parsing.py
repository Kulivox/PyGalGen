import ast
from typing import Tuple, Optional, Any, Set, List
from exceptions import ArgParseImportNotFound, ArgParserNotUsed
import abc


class Discovery(ast.NodeVisitor, abc.ABC):
    def __init__(self, actions: List[ast.AST]):
        self.actions = actions

    @abc.abstractmethod
    def report_findings(self) -> Tuple:
        pass


class ImportDiscovery(Discovery):
    def __init__(self, actions: List[ast.AST]):
        super(ImportDiscovery, self).__init__(actions)
        self.argparse_module_alias: Optional[str] = None
        self.argument_parser_alias: Optional[str] = None

    def visit_Import(self, node: ast.Import) -> Any:
        for item in node.names:
            if item.name == "argparse":
                alias = item.asname if item.asname is not None else "argparse"
                self.argparse_module_alias = alias
                self.actions.append(node)
                return

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        if "argparse" not in node.module:
            return

        for item in node.names:
            if item.name == "ArgumentParser":
                alias = item.asname if item.asname is not None \
                    else "ArgumentParser"
                self.argument_parser_alias = alias
                self.actions.append(node)

    def report_findings(self) -> Tuple:
        if self.argparse_module_alias is None and self.argument_parser_alias is None:
            raise ArgParseImportNotFound

        return (self.actions, self.argparse_module_alias,
                self.argument_parser_alias)


class ParserDiscovery(Discovery):

    def __init__(self, actions: List[ast.AST], argparse_alias: Optional[str],
                 argument_parser_alias: Optional[str]):
        self.argument_parser_alias = argument_parser_alias
        self.argparse_module_alias = argparse_alias
        self.main_parser_name: Optional[str] = None

        super(ParserDiscovery, self).__init__(actions)

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
            return True, name

        # ArgumentParser is created using attribute call on imported module
        if (isinstance(node.value, ast.Call) and
                isinstance(node.value.func, ast.Attribute) and
                node.value.func.attr == "ArgumentParser" and
                node.value.func.value.id == self.argparse_module_alias):
            return True, name

        return False, None

    def visit_Assign(self, node: ast.Assign):
        # visit into children of this node is not necessary
        is_argparse, name = self.is_this_argparse(node)
        if is_argparse:
            self.main_parser_name = name
            self.actions.append(node)

        self.generic_visit(node)

    def report_findings(self) -> Tuple:
        if self.main_parser_name is None:
            raise ArgParserNotUsed

        return self.actions, self.main_parser_name


class GroupDiscovery(Discovery):
    def __init__(self, actions: List[ast.AST], main_name: str):
        self.main_name = main_name
        self.parser_names: Set[str] = {self.main_name}
        self.groups = set()
        super(GroupDiscovery, self).__init__(actions)

    def is_this_group_creation(self, node: ast.Assign):
        if not (len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name)):
            return False, None

        name = node.targets[0].id
        if not (isinstance(node.value, ast.Call) and
                isinstance(node.value.func, ast.Attribute) and
                node.value.func.attr == "add_argument_group"):
            return False, None

        if node.value.func.value.id not in self.parser_names:
            print(
                f"Cant ensure that '{self.main_name}'"
                f" is the only argument parser"
                f" because of use of this parser variable:"
                f" {node.value.func.value.id}")
            self.parser_names.add(node.value.func.value.id)
            node.value.func.value.id = self.main_name

        return True, name

    def visit_Assign(self, node: ast.Assign):
        is_group_creation, name = self.is_this_group_creation(node)
        if is_group_creation:
            self.groups.add(name)
            self.actions.append(node)

    def report_findings(self) -> Tuple:
        return self.actions, self.main_name, self.parser_names, self.groups


class ArgumentCreationDiscovery(Discovery):
    def __init__(self, actions: List[ast.AST], main_name: str,
                 parser_names: Set[str], groups: Set[str]):
        self.main_name = main_name
        self.sections = groups
        self.parser_names = parser_names
        super(ArgumentCreationDiscovery, self).__init__(actions)

    def is_call_on_parser_or_group(self, node: ast.Call):
        return isinstance(node.func, ast.Attribute) and \
               node.func.attr == "add_argument" and \
               (node.func.value.id in self.sections or
                node.func.value.id in self.parser_names)

    def visit_Call(self, node: ast.Call) -> Any:
        if self.is_call_on_parser_or_group(node):
            assert isinstance(node.func, ast.Attribute)
            if node.func.value.id != self.main_name:
                node.func.value.id = self.main_name

            self.actions.append(ast.Expr(node))

        self.generic_visit(node)

    def report_findings(self) -> Tuple:
        return self.actions, self.main_name


def obtain_prepared_parser(path):
    with open(path, "r", encoding="utf-8") as source:
        target = ast.parse(source.read())

    discovery_classes = [ImportDiscovery, ParserDiscovery,
                         GroupDiscovery, ArgumentCreationDiscovery]

    findings = [],
    for cls in discovery_classes:
        discovery = cls(*findings)
        discovery.visit(target)
        findings = discovery.report_findings()

    actions, main_name = findings
    module = ast.Module(body=actions, type_ignores=[])
    ast.fix_missing_locations(module)
    variables = {}

    compiled_module = compile(module, filename="<parser>", mode="exec")
    exec(compiled_module, globals(), variables)

    print(variables[main_name]._actions)


if __name__ == "__main__":
    obtain_prepared_parser("../../TRTools/trtools/qcSTR/qcSTR.py")
