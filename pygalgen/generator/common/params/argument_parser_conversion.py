import ast
import logging
import uuid

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
    section_label:str
    default_val: Any
    help: Optional[str] = None
    optional: bool = False
    is_repeat: bool = False
    is_select: bool = False
    choices: Optional[List[Any]] = None
    is_flag: bool = False


def obtain_and_convert_parser(path: str) -> Optional[ArgumentParser]:
    try:
        tree = create_module_tree(path)
    except FileNotFoundError:
        logging.error("Input file not found")
        return None

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
                                    data_inputs: Set[str], reserved_names: Set[str]) -> List[ParamInfo]:
    params = []
    name_map = dict()
    section_map = dict()
    for action in parser._actions:

        name = action.dest
        type_ = _determine_type(data_inputs, name, action.type)
        argument = action.option_strings[0]

        update_name_map(name, name_map, reserved_names)
        # these actions are of hidden type, and they contain the container
        # field. This field contains the information about their groups.
        # currently, only two level hierarchies are supported
        section = action.container.title
        update_name_map(section, section_map, reserved_names)
        default_val = action.default

        help_ = action.help
        optional = not action.required
        is_repeat = type(action).__name__ == "_AppendAction"
        is_select = action.choices is not None
        choices = action.choices
        is_flag = action.type is None

        params.append(ParamInfo(type_, name_map[name], argument, name,
                                section_map[section], section,
                                default_val, help_,
                                optional, is_repeat, is_select, choices,
                                is_flag))

    return params


def update_name_map(name, name_map, reserved_names):
    name_map[name] = name
    # very unlikely name match will happen for the generated string,
    # but it can happen,
    # easily fixable by loop
    if name.lower() in reserved_names:
        name_map[name] = name + str(uuid.uuid4())[:4]


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
