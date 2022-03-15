from typing import Any, Iterable
import xml.etree.ElementTree as ET
from generator.pluggability.strategy import Strategy
from generator.common.stages import StrategyStage
from generator.common.params.argument_parser_conversion import \
    obtain_and_convert_parser, extract_useful_info_from_parser

import generator.common.xml_utils as xu


class DefaultParams(Strategy):
    STAGE = StrategyStage.PARAMS

    def __init__(self, args: Any):
        super(DefaultParams, self).__init__(args, self.STAGE)

    def apply_strategy(self, tool_input: Any, xml_output: ET.ElementTree) \
            -> ET.ElementTree:
        root = xml_output.getroot()
        inputs = root.find("/tool/inputs")

        parser = obtain_and_convert_parser(self.args.path)
        data_inputs = set(item for item in self.args.inputs.split(","))
        param_info = extract_useful_info_from_parser(parser, data_inputs)

        sections = {}
        for param in param_info:
            if param.section not in sections:
                sections[param.section] = \
                    xu.create_section(inputs, param.section, False)

            curr_root = sections[param.section]

            if param.is_repeat:
                curr_root = xu.create_repeat(curr_root, param.name + "_repeat")

            curr_root = xu.create_param(curr_root, param.attribute,
                                        param.type, param.optional,
                                        param.label, param.help)

            if param.is_select:
                for choice in param.choices:
                    xu.create_option(curr_root, str(choice),
                                     str(choice).capitalize())

        return xml_output
