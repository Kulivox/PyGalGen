from typing import Any, Iterable
import xml.etree.ElementTree as ET
from generator.pluggability.strategy import Strategy
from generator.common.stages import StrategyStage
from generator.common.params.argument_parser_conversion import\
    obtain_and_convert_parser

class DefaultParams(Strategy):
    STAGE = StrategyStage.PARAMS

    def __init__(self, args: Any):
        super(DefaultParams, self).__init__(args, self.STAGE)

    def apply_strategy(self, tool_input: Any, xml_output: ET.ElementTree)\
            -> ET.ElementTree:
        # root = xml_output.getroot()
        # inputs = root.find("/tool/inputs")

        obtain_and_convert_parser(self.args.path)

        return xml_output


