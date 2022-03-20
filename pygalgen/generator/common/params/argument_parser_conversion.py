import ast
import logging

from pygalgen.generator.common.source_file_parsing.parsing_commons \
    import create_module_tree
from pygalgen.generator.common.source_file_parsing.parser_discovery_and_init \
    import get_parser_init_and_actions
from pygalgen.generator.common.source_file_parsing.unknown_names_discovery \
    import initialize_variables_in_module
from pygalgen.generator.common.source_file_parsing.local_module_parsing import \
    handle_local_module_names
from pygalgen.generator.common.source_file_parsing.parsing_exceptions import \
    ArgumentParsingDiscoveryError

from typing import Optional, Set, Any, List
from argparse import ArgumentParser
import dataclasses

from pygalgen.common.utils import LINTER_MAGIC


@dataclasses.dataclass
class ParamInfo:
    type: str
    name: str
    attribute: str
    label: str
    section: str
    default_val: Any
    help: Optional[str] = None
    optional: bool = False
    is_repeat: bool = False
    is_select: bool = False
    choices: Optional[List[Any]] = None
    is_flag: bool = False


def obtain_and_convert_parser(path: str) -> Optional[ArgumentParser]:
    tree = create_module_tree(path)
    try:
        actions, name, section_names = \
            get_parser_init_and_actions(tree)

        actions, unknown_names = \
            initialize_variables_in_module(tree, name,
                                           section_names, actions)

        result_module = handle_local_module_names(actions, unknown_names)
    except ArgumentParsingDiscoveryError as e:
        logging.error(e)
        return None

    ast.fix_missing_locations(result_module)
    compiled_module = compile(result_module, filename="<parser>", mode="exec")
    variables = {}
    try:
        exec(compiled_module, globals(), variables)
    except Exception as e:
        logging.error("Parser couldn't be extracted")
        return None
    return variables[name]


def extract_useful_info_from_parser(parser: ArgumentParser,
                                    data_inputs: Set[str]) -> List[ParamInfo]:
    params = []
    for action in parser._actions:
        name = action.dest
        type_ = _determine_type(data_inputs, name, action.type)
        argument = action.option_strings[0]

        # these actions are of hidden type, and they contain the container
        # field. This field contains the information about their groups.
        section = action.container.title

        default_val = action.default

        help_ = action.help
        optional = not action.required
        is_repeat = type(action).__name__ == "_AppendAction"
        is_select = action.choices is not None
        choices = action.choices
        is_flag = action.type is None

        params.append(ParamInfo(type_, name, argument, name, section,
                                default_val, help_,
                                optional, is_repeat, is_select, choices,
                                is_flag))

    return params


def _determine_type(data_inputs, name, type_):
    if type_ is None or type_ == bool:
        type_ = "boolean"
    elif type_ == int:
        type_ = "integer"
    elif type_ == float:
        type_ = "float"
    elif type_ == str:
        if name in data_inputs:
            type_ = "data"
        else:
            type_ = "text"
    else:
        type_ = f"{LINTER_MAGIC} argument uses complex type," \
                f" it's type cannot be determined"
    return type_
