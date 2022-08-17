"""
Main module of PyGalGen generator, responsible for defining default program
 arguments and program execution
"""
from argparse import ArgumentParser
import sys
from typing import List

from pygalgen.generator.common.source_file_parsing.decoy_parser import \
    DecoyParser
from pygalgen.generator.pipeline import PipelineExecutor
from pygalgen.generator.plugin_discovery import discover_plugins
import logging
import pygalgen.generator.default_plugins
import importlib.resources as res

def define_default_params() -> ArgumentParser:
    """
    Function creates argument parser and initializes default arguments

    Returns
    -------
    parser : ArgumentParser
     parser object initialized with default program arguments
    """
    parser = DecoyParser()
    default = parser.add_argument_group("Default program parameters")

    default.add_argument("--path",
                         help="Path to the source file",
                         required=True)

    default.add_argument("--tool-name", required=True, type=str,
                                help="Name of the package for which you "
                                     "are "
                                     "creating the tool definition file")

    logging_grp = parser.add_argument_group("Logging arguments")

    logging_grp.add_argument("--verbose", action="store_true", default=False,
                             help="Prints out info logs")
    logging_grp.add_argument("--debug", action="store_true", default=False,
                             help="Print out debug text")

    argrp = logging_grp.add_argument_group("more specific logging")
    argrp.add_argument("--omfggg")

    plugins = parser.add_argument_group("Plugin discovery")
    plugins.add_argument("--plugins-path", type=str, default="plugins",
                         help="Path to directory containing plugins you want "
                              "to use")
    return parser


# using this function kind of goes against the idea of the argparse,
# but it's necessary
# to load plugins, plugin directory path has to be known, argument parsing of
# argparse object happens after plugin loading. Because of this problem,
def obtain_plugins_path(args: List[str]) -> str:
    """
    Manually extracts --plugins-path from arguments. The manual extraction is
    necessary, because this value is needed before argumenParser
    can parse arguments
    Parameters
    ----------
    args : List[str]

    Returns
    -------
    Path to plugins directory
    """
    for i, item in enumerate(args):
        if item == "--plugins-path" and i + 1 < len(args):
            return args[i + 1]

    return "plugins"


def main(args):
    """
    Main function of PyGalGen generator
    Parameters
    ----------
    args : list of command line arguments:

    Returns
    -------
    Error code
    """
    logging.basicConfig(level=logging.DEBUG)

    parser = define_default_params()
    parser.report_arguments_and_groups().recurse()
    pipeline = PipelineExecutor(parser)
    logging.info("Created pipeline executor")

    path_to_default = res.files(pygalgen.generator.default_plugins)
    default_plugins = discover_plugins(path_to_default)
    logging.info(f"Discovered {len(default_plugins)} default"
                 f" plugin{'' if len(default_plugins) == 1 else 's'}")

    plugin_path = obtain_plugins_path(args)

    custom_plugins = discover_plugins(plugin_path)

    logging.info(f"Discovered {len(custom_plugins)} custom"
                 f" plugin{'' if len(default_plugins) == 1 else 's'}")

    result = pipeline.execute_pipeline(default_plugins +
                                       custom_plugins)

    return result


def run():
    ret_code = main(sys.argv)
    exit(ret_code)


if __name__ == '__main__':
    run()