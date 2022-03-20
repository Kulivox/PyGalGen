import argparse

from pipeline import PipelineExecutor
from default_plugins.default import DefaultPlugin
from generator.plugin_discovery import discover_plugins
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
    default = parser.add_argument_group("Default program parameters")
    default.add_argument("--package-name", required=True, type=str,
                         help="Name of the package for which you are "
                              "creating the tool definition file")

    default.add_argument("--package-version", type=str, required=True,
                         help="Version of the package")

    default.add_argument("--bundle", action="store_true", default=False,
                         help="If this argument is set, argument '--path' "
                              "will point to root directory of tool bundle "
                              "you want to parse")
    default.add_argument("--path",
                         help="Path to the source file / directory",
                         required=True)

    default.add_argument("--tool-name-map", required=False, type=str,
                         default="",
                         help="Comma separated list of file names and tool "
                              "names, used in tool discovery if '--bundle' "
                              "param is set. Format: file_name:tool_name,...")

    default.add_argument("--inputs", type=str,
                         help="Comma separated list of names and format types"
                              " of arguments that contain paths to input files",
                         default="")

    logging_grp = parser.add_argument_group("Logging arguments")

    logging_grp.add_argument("--verbose", action="store_true", default=False,
                             help="Prints out info logs")
    logging_grp.add_argument("--debug", action="store_true", default=False,
                             help="Print out debug text")

    return parser


def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = define_default_params()
    pipeline = PipelineExecutor(parser)

    logging.info("Created pipeline executor")

    discovered_plugins = discover_plugins(generator.plugins)

    logging.info(f"Discovered {len(discovered_plugins)} plugins")

    default_plugins = [DefaultPlugin()]

    result = pipeline.execute_pipeline(default_plugins +
                                       discovered_plugins)

    return result


if __name__ == '__main__':
    main()
