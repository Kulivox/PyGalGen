import argparse

from pipeline import PipelineExecutor
from default_plugins.default import DefaultPlugin
from generator.plugin_discovery import discover_plugins
import generator.plugins
import logging

import xml.dom.minidom as minidom
import lxml.etree as ET


# TODO create complex type for inputs
# def well_formed_inputs_type(inputs: Optional[str]):
#     if inputs is None:
#         return inputs
#
#     try:


def define_default_params():
    parser = argparse.ArgumentParser("Command parser")

    parser.add_argument("--path",
                        help="Path to the source file", required=True)
    parser.add_argument("--inputs", type=str,
                        help="Comma separated list of names and format types"
                             " of arguments that contain paths to input files",
                        default="")

    parser.add_argument("--verbose",  action="store_true", default=False,
                        help="Prints out info logs")
    parser.add_argument("--debug", action="store_true", default=False,
                        help="Print out debug text")

    return parser


def main():
    logging.basicConfig(level=logging.INFO)

    parser = define_default_params()
    pipeline = PipelineExecutor(parser)

    logging.info("Created pipeline executor")

    discovered_plugins = discover_plugins(generator.plugins)

    logging.info(f"Discovered {len(discovered_plugins)} plugins")

    default_plugins = [DefaultPlugin()]

    result = pipeline.execute_pipeline(default_plugins +
                                       discovered_plugins)

    xml_string = ET.tostring(result.getroot())

    dom = minidom.parseString(xml_string)
    xml_string = dom.toprettyxml()

    with open("result.xml", "w", encoding="utf-8") as result_file:
        result_file.write(xml_string)

if __name__ == '__main__':
    main()
