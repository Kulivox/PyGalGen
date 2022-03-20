import os
from typing import Any, List
from pygalgen.generator.pluggability.plugin import Plugin
from argparse import ArgumentParser
from pygalgen.generator.common.macros.macros import MacrosFactory
import xml.dom.minidom as minidom
import lxml.etree as ET
import logging
import copy

# because logging.basicConfig() doesn't reset the settings, but adds a
# logging handler to a list of handlers, this list of handlers has to be
# cleaned up before changing logging configuration
def set_logging_settings(fmt: str, level: int):
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(format=fmt, level=level)


class PipelineExecutor:
    def __init__(self, default_arg_parser: ArgumentParser):
        self.args_parser = default_arg_parser

    def execute_pipeline(self, plugins: List[Plugin]) -> int:

        # initialize argument parser
        parsed_args = self._parse_args(plugins)

        # initialize logger
        format_ = "%(levelname)s:%(module)s:%(message)s"
        set_logging_settings(format_, logging.WARNING)
        if parsed_args.verbose:
            set_logging_settings(format_, level=logging.INFO)

        if parsed_args.debug:
            set_logging_settings(format_, level=logging.DEBUG)

        # prepare data preparation plugins
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

        strategies = []
        for plugin_strategies in [plugin.get_strategies(parsed_args, macros)
                                  for plugin in plugins]:
            strategies += plugin_strategies

        # strategies are than sorted and can be iteratively applied
        strategies.sort()
        result = []

        if not strategies:
            logging.warning("No strategies were loaded")
            return 0

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

        if not args.tool_name_map:
            logging.warning("No mapping of file names to "
                            "tool names was provided")

        file_to_name_map = {}
        for file, name in [item.split(":") for item in
                           args.tool_name_map.split(",")]:
            file_to_name_map[file] = name

        if not os.path.exists(args.path):
            logging.error("Provided path doesn't lead to valid directory")
            exit(1)

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

            with open(f"{tool_name}.xml", "w",
                      encoding="utf-8") as result_file:
                result_file.write(xml_string)
                logging.info(f"Created tool def file for {tool_name}")
