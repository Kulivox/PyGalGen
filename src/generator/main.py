import argparse
from pipeline import PipelineExecutor
from default_plugins.default import DefaultPlugin
from generator.plugin_discovery import discover_plugins

import generator.plugins


def define_default_params():
    parser = argparse.ArgumentParser("Command parser")

    parser.add_argument("--path",
                            help="Path to the source file", required=True)
    parser.add_argument("--inputs", type=str, help="Comma separated list of names of arguments that contain paths to input files", default="")
    parser.add_argument("--debug", action="store_true", default=False, help="Print out debug text")

    return parser


def main():
    parser = define_default_params()
    pipeline = PipelineExecutor(parser)

    discovered_plugins = discover_plugins(generator.plugins)
    default_plugins = [DefaultPlugin()]
    result = pipeline.execute_pipeline(default_plugins +
                                    discovered_plugins, None)
    import xml.etree.ElementTree as ET
    ET.indent(result, "\t")
    print(ET.dump(result.getroot()))


if __name__ == '__main__':
    main()
