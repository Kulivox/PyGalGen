"""
Module contains definition of help strategy
"""
from lxml.etree import ElementTree
from pygalgen.generator.common.params.argument_parser_conversion import \
    obtain_and_convert_parser
from pygalgen.generator.common.macros.macros import Macros
from pygalgen.generator.pluggability.strategy import Strategy, StrategyStage
from typing import Any

import io


class HelpStrategy(Strategy):
    """
    This strategy extracts argument parser from target source code,
    and uses it to generate help section
    """
    STAGE = StrategyStage.HELP

    def __init__(self, args: Any, macros: Macros):
        super().__init__(args, macros, self.STAGE)

    def apply_strategy(self, xml_output: ElementTree) -> Any:
        parser = obtain_and_convert_parser(self.args.path)

        file_like = io.StringIO()

        parser.print_help(file_like)
        help_ = xml_output.find(".//help")

        file_like.seek(0)

        help_.text = file_like.read()

        return xml_output
