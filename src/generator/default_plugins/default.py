from generator.pluggability.plugin import Plugin
from generator.default_plugins.strategies.params import DefaultParams
from generator.default_plugins.strategies.setup import SetupStrategy
from generator.default_plugins.strategies.commands import CommandsStrategy

from argparse import ArgumentParser
from typing import Any

class DefaultPlugin(Plugin):
    def get_strategies(self, args):
        return [SetupStrategy(args), DefaultParams(args),
                CommandsStrategy(args)]

    def add_custom_params(self, params: ArgumentParser):
        params.add_argument("--tool-name", required=True, type=str)
        params.add_argument("--dont-redirect-output", default=False,
                            action="store_true")