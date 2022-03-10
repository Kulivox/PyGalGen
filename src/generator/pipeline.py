from typing import Any, List
from pluggability.plugin import Plugin
from pluggability.strategy import Strategy
from argparse import ArgumentParser
from functools import reduce
from operator import add


class PipelineExecutor:
    def __init__(self, default_arg_parser: ArgumentParser):
        self.args_parser = default_arg_parser

    def execute_pipeline(self, plugins: List[Plugin], input_file, output_file):
        # initialize argument parser
        parsed_args = self._parse_args(plugins)
        strategies = list(
            reduce(add, map(lambda x: x.get_strategies(parsed_args), plugins)))

        # strategies are than sorted and can be iteratively applied
        strategies.sort()

        for strategy in strategies:
            output_file = strategy.apply_strategy(input_file, output_file)

        return output_file

    def _parse_args(self, plugins):
        for plugin in plugins:
            plugin.add_custom_params(self.args_parser)

        return self.args_parser.parse_args()
