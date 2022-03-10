from argparse import ArgumentParser
from pipeline import PipelineExecutor
from plugins.custom import CustomPlugin
from default_plugins.default import DefaultPlugin
from generator.plugin_discovery import discover_plugins

import generator.plugins


def define_default_params(arg_parser: ArgumentParser):
    arg_parser.add_argument("verbose", action="store-true",
                            help="The program will output more console info")


def main():
    parser = ArgumentParser("Command parser")
    pipeline = PipelineExecutor(parser)

    discovered_plugins = discover_plugins(generator.plugins)
    default_plugins = [DefaultPlugin()]
    print(pipeline.execute_pipeline(default_plugins +
                                    discovered_plugins, "input", "xml"))


if __name__ == '__main__':
    main()
