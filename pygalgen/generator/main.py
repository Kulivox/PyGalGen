import argparse
import sys
from pygalgen.generator.pipeline import PipelineExecutor
from pygalgen.generator.plugin_discovery import discover_plugins
import logging


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

    plugins = parser.add_argument_group("Plugin discovery")
    plugins.add_argument("--plugins-path", type=str, default="plugins",
                         help="Path to directory containing plugins you want "
                              "to use")
    return parser


# using this function kind of goes against the idea of the argparse,
# but it's necessary
# to load plugins, plugin directory path has to be known, argument parsing of
# argparse object happens after plugin loading. Because of this problem,
def obtain_plugins_path(args):
    for i, item in enumerate(args):
        if item == "--plugins-path" and i + 1 < len(args):
            return args[i + 1]

    return "plugins"


def main(args):
    logging.basicConfig(level=logging.DEBUG)

    parser = define_default_params()
    pipeline = PipelineExecutor(parser)
    logging.info("Created pipeline executor")

    default_plugins = discover_plugins("default_plugins")
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
    main(sys.argv)


if __name__ == '__main__':
    run()
