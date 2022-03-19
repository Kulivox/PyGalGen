import argparse

from generator.common.constants import LOGGER_NAME
from pipeline import PipelineExecutor
from default_plugins.default import DefaultPlugin
from generator.plugin_discovery import discover_plugins
from typing import Optional
import generator.plugins
import logging


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

    result.write("result.xml")


if __name__ == '__main__':
    main()
