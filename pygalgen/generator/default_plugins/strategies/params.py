from typing import Any, Iterable, Set
import lxml.etree as ET

from pygalgen.generator.common.utils import parse_argument_comma_sep_list
from pygalgen.generator.pluggability.strategy import Strategy, StrategyStage
from pygalgen.generator.common.params.argument_parser_conversion import \
    obtain_and_convert_parser, extract_useful_info_from_parser

import pygalgen.generator.common.xml_utils as xu


class DefaultParams(Strategy):
    STAGE = StrategyStage.PARAMS

    def __init__(self, args: Any, macros, reserved_names: Set[str]):
        super(DefaultParams, self).__init__(args, macros, self.STAGE)
        self.reserved_names = reserved_names

    def apply_strategy(self, xml_output: ET.ElementTree) -> ET.ElementTree:
        inputs = xml_output.find(".//inputs")

        parser = obtain_and_convert_parser(self.args.path)
        data_inputs = {prm: fmt for prm, fmt in
                       parse_argument_comma_sep_list(self.args.inputs)}

        param_info, name_map = extract_useful_info_from_parser(parser,
                                                               data_inputs,
                                                               self.reserved_names)

        sections = {}
        for param in param_info:
            if param.section not in sections:
                sections[param.section] = \
                    xu.create_section(inputs, param.section,
                                      param.section_label, False)

            curr_root = sections[param.section]

            if param.is_repeat:
                curr_root = xu.create_repeat(curr_root, param.name + "_repeat")

            if name_map[param.name] in data_inputs:
                curr_root = xu.create_param(curr_root, param.argument,
                                            param.type, param.optional,
                                            param.label, param.help,
                                            format_attr=data_inputs[
                                                name_map[param.name]])
            else:
                curr_root = xu.create_param(curr_root, param.argument,
                                            param.type, param.optional,
                                            param.label, param.help)

            if param.is_select:
                for choice in param.choices:
                    xu.create_option(curr_root, str(choice),
                                     str(choice).capitalize())

        return xml_output
