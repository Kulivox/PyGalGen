import ast
from typing import Tuple, Optional, Any, Set, List
import astunparse
import abc


class Discovery(ast.NodeVisitor, abc.ABC):
    def __init__(self, actions: List[ast.AST]):
        self.actions = actions

    @abc.abstractmethod
    def report_findings(self) -> Any:
        pass

class ImportDiscovery(Discovery):
    def __init__(self, actions: List[ast.AST]):
        super(ImportDiscovery, self).__init__(actions)
        self.argparse_alias: Optional[str] = None
        self.argument_parser_alias: Optional[str] = None

    def visit_Import(self, node: ast.Import) -> Any:
        pass

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        pass

    def report_findings(self) -> Any:
        if self.argparse_alias is None and self.argument_parser_alias is None:
            raise NotF


class ParserDiscovery(ast.NodeVisitor):
    def __init__(self):
        self.main_parser_name = ""
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
            self.main_parser_name = name
            self.parser_names.add(name)
            self.parser_actions.append(node)
        self.generic_visit(node)


class GroupDiscovery(ast.NodeVisitor):
    def __init__(self, parser_names: Set[str], main_name: str):
        self.main_name = main_name
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
            print(
                f"Cant ensure that '{list(self.parser_names)[0]}' is the only parser"
                f" because of use of this parser:"
                f" {node.value.func.value.id}")
            self.parser_names.add(node.value.func.value.id)
            node.value.func.value.id = self.main_name

        return True, name

    def visit_Assign(self, node: ast.Assign) -> Any:
        is_group_creation, name = self.is_this_group_creation(node)
        if is_group_creation:
            self.sections.add(name)
            self.parser_actions.append(node)



class ArgumentCreationDiscovery(ast.NodeVisitor):
    def __init__(self, sections: Set[str], parser_names: Set[str],
                 main_name: str):
        self.main_name = main_name
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
            if node.func.value.id != self.main_name:
                node.func.value.id = self.main_name

            self.parser_actions.append(ast.Expr(node))

        self.generic_visit(node)


class OffsetRemoval(ast.NodeTransformer):
    def generic_visit(self, node: ast.AST) -> ast.AST:
        if hasattr(node, "lineno"):
            del node.lineno

        if hasattr(node, "col_offset"):
            del node.col_offset

        return super().generic_visit(node)


def obtain_prepared_parser(path):
    with open(path, "r", encoding="utf-8") as source:
        tree = ast.parse(source.read())

    ## TODO find this import in code - not everyone might be using the import like this
    actions = [ast.ImportFrom(
        module="argparse",
        names=[ast.alias(name="ArgumentParser")]
    )]
    analyzer = ParserDiscovery()
    analyzer.visit(tree)
    actions += analyzer.parser_actions

    main_name = analyzer.main_parser_name
    parser_names = analyzer.parser_names

    analyzer = GroupDiscovery(parser_names, main_name)
    analyzer.visit(tree)
    actions += analyzer.parser_actions

    analyzer = ArgumentCreationDiscovery(analyzer.sections, parser_names,
                                         main_name)
    analyzer.visit(tree)
    actions += analyzer.parser_actions

    module = ast.Module(body=actions, type_ignores=[])
    module = ast.fix_missing_locations(module)
    compiled_module = compile(module, filename="", mode="exec")

    variables = {}
    exec(compiled_module, globals(), variables)
    print(variables[main_name]._actions)


if __name__ == "__main__":
    obtain_prepared_parser("../../main.py")
