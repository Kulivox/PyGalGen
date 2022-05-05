from os import path

from pygalgen.generator.default_plugins.strategies.help import HelpStrategy
from pygalgen.generator.default_plugins.strategies.outputs import \
    DefaultOutputs
from pygalgen.generator.pluggability.data_setup import DataSetup
from pygalgen.generator.pluggability.plugin import Plugin
from pygalgen.generator.default_plugins.strategies.params import DefaultParams
from pygalgen.generator.default_plugins.strategies.commands import \
    CommandsStrategy
from pygalgen.generator.default_plugins.data_setup import DefaultDataSetup
from pygalgen.generator.default_plugins.strategies.header import HeaderStrategy

from argparse import ArgumentParser
from typing import Any


class DefaultPlugin(Plugin):
    def __init__(self, order: int, name: str, assets_path: str):
        super().__init__(order, name, assets_path)

    def get_data_setup(self, args: Any) -> DataSetup:
        return DefaultDataSetup(args, self.assets_path)

    def get_strategies(self, args, macros):
        """
        Method initializes all strategies of
        Default plugin with provided parameters and initialized macros
        """
        with open(path.join(self.assets_path, "reserved_var_names.txt")) as f:
            reserved_names = set((name for name in f.readlines()))

        return [HeaderStrategy(args, macros),
                DefaultParams(args, macros,
                              reserved_names),
                CommandsStrategy(args, macros),
                HelpStrategy(args, macros), DefaultOutputs(args, macros)]

    def add_custom_params(self, params: ArgumentParser):
        """
        Defines custom params of Default plugin
        """
        default_plugin = params.add_argument_group("Default plugin")
        default_plugin.add_argument("--dont-redirect-output", default=False,
                                    action="store_true",
                                    help="If this argument is present, tool "
                                         "will not redirect its output to "
                                         "output files during execution in "
                                         "galaxy")

        default_plugin.add_argument("--galaxy-profile", required=False,
                                    type=str, help="Version of galaxy profile")

        default_plugin.add_argument("--descr", required=True,
                                    type=str, help="Description of the tool")


        default_plugin.add_argument("--requirements", required=True, type=str,
                                    help="Comma separated list of "
                                         "package:version pairs")

        default_plugin.add_argument("--tool-version", type=str,
                                    required=True,
                                    help="Version of the tool")

        default_plugin.add_argument("--inputs", type=str,
                                    help="Comma separated list of names and "
                                         "format types "
                                         "of program arguments that define "
                                         "inputs. "
                                         "(name:format,name:format) For "
                                         "example, "
                                         "if your program accepts path to vcf "
                                         "file in argument called input, "
                                         "enter "
                                         "'input:vcf'",
                                    default="")

