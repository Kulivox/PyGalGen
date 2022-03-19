import os
from typing import Any, List
from pluggability.plugin import Plugin
from argparse import ArgumentParser
from functools import reduce
from operator import add
from generator.common.macros.macros import MacrosFactory
import xml.dom.minidom as minidom
from os import walk
import lxml.etree as ET
import logging
import copy

class PipelineExecutor:
    def __init__(self, default_arg_parser: ArgumentParser):
        self.args_parser = default_arg_parser

    def execute_pipeline(self, plugins: List[Plugin]) -> \
            int:
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
        macros.write_xml("macros.xml")

        strategies = list(
            reduce(add, map(lambda x: x.get_strategies(parsed_args, macros),
                            plugins)))

        # strategies are than sorted and can be iteratively applied
        strategies.sort()
        result = []

        for path, tool_name in self._provide_file_and_tool_names(parsed_args):
            current_tree = copy.deepcopy(xml_tree)
            for strategy in strategies:
                current_tree = strategy.apply_strategy(current_tree, path,
                                                       tool_name)
            result.append((current_tree, tool_name))

        self._write_output(result)

        return 0

    @staticmethod
    def _provide_file_and_tool_names(args: Any) -> (str, str):
        if not args.bundle:
            yield args.path, args.package_name
            return

        file_to_name_map = {}
        for file, name in [item.split(":") for item in args.tool_name_map.split(",")]:
            file_to_name_map[file] = name

        for path, dirs, files in os.walk(args.path):
            for file in files:
                if file in file_to_name_map:
                    yield os.path.join(path, file), file_to_name_map[file]





    def _parse_args(self, plugins):
        for plugin in plugins:
            plugin.add_custom_params(self.args_parser)

        return self.args_parser.parse_args()

    @staticmethod
    def _write_output(trees: List[ET.ElementTree]):
        for tree, tool_name in trees:
            xml_string = ET.tostring(tree.getroot())

            dom = minidom.parseString(xml_string)
            xml_string = dom.toprettyxml()

            with open(f"{tool_name}.xml", "w", encoding="utf-8") as result_file:
                result_file.write(xml_string)

