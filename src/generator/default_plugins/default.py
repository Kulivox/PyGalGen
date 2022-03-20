from generator.default_plugins.strategies.help import HelpStrategy
from generator.pluggability.data_setup import DataSetup
from generator.pluggability.plugin import Plugin
from generator.default_plugins.strategies.params import DefaultParams
from generator.default_plugins.strategies.commands import CommandsStrategy
from generator.default_plugins.data_setup import DefaultDataSetup
from generator.default_plugins.strategies.header import HeaderStrategy

from argparse import ArgumentParser
from typing import Any


class DefaultPlugin(Plugin):
    def get_data_setup(self, args: Any) -> DataSetup:
        return DefaultDataSetup(args)

    def get_strategies(self, args, macros):
        return [HeaderStrategy(args, macros),
                DefaultParams(args, macros),
                CommandsStrategy(args, macros),
                HelpStrategy(args, macros)]

    def add_custom_params(self, params: ArgumentParser):
        default_plugin = params.add_argument_group("Default plugin")
        default_plugin.add_argument("--dont-redirect-output", default=False,
                                    action="store_true",
                                    help="If this argument is present, tool "
                                         "will not redirect its output to "
                                         "output files during execution in "
                                         "galaxy")

        default_plugin.add_argument("--galaxy-profile", required=False,
                                    type=str, help="Version of galaxy profile")
