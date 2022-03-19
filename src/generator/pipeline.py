from typing import Any, List
from pluggability.plugin import Plugin
from argparse import ArgumentParser
from functools import reduce
from operator import add
from generator.common.macros.macros import MacrosFactory

import lxml.etree as ET
import logging


class PipelineExecutor:
    def __init__(self, default_arg_parser: ArgumentParser):
        self.args_parser = default_arg_parser

    def execute_pipeline(self, plugins: List[Plugin]) -> \
            ET.ElementTree:
        # initialize argument parser
        logging.basicConfig(level=logging.WARNING)
        parsed_args = self._parse_args(plugins)

        if parsed_args.verbose:
            logging.basicConfig(level=logging.INFO)

        if parsed_args.debug:
            logging.basicConfig(level=logging.DEBUG)

        data_init = list(plg.get_data_setup(parsed_args) for plg in plugins)
        data_init.sort()

        xml_tree = ET.ElementTree()
        mf = MacrosFactory()

        # xml tree of result is prepared in this step, together with macros
        for initializer in data_init:
            xml_tree = initializer.initialize_xml_tree(xml_tree)
            mf = initializer.initialize_macros(mf)

        macros = mf.create_macros()

        strategies = list(
            reduce(add, map(lambda x: x.get_strategies(parsed_args, macros),
                            plugins)))

        # strategies are than sorted and can be iteratively applied
        strategies.sort()

        for strategy in strategies:
            xml_tree = strategy.apply_strategy(xml_tree)

        return xml_tree

    @staticmethod
    def _provide_file_and_tool_names(args: Any) -> (str, str):
        if not args.bundle:
            return args.path, args.tool_name

        raise NotImplemented

    def _parse_args(self, plugins):
        for plugin in plugins:
            plugin.add_custom_params(self.args_parser)

        return self.args_parser.parse_args()
