from typing import Any, List
import argparse
from pygalgen.generator.common.macros.macros import Macros
from pygalgen.generator.pluggability.data_setup import DataSetup
from pygalgen.generator.pluggability.plugin import Plugin
from pygalgen.generator.pluggability.strategy import Strategy
from Strategies.citations import Citations
from Strategies.params import TRToolsParams
from macros_setup import MacrosSetup


class TRToolsPlugin(Plugin):
    def __init__(self, order: int, name: str, assets_path: str):
        super().__init__(order, name, assets_path)

    def add_custom_params(self, params: argparse.ArgumentParser):
        group = params.add_argument_group("TRTools plugin")
        group.add_argument("--citations", required=True, type=str,
                           help="Path to file containing tool citation in "
                                "bibtex format")

    def get_strategies(self, args: Any, macros: Macros) -> List[Strategy]:
        return [Citations(args, macros), TRToolsParams(args, macros)]

    def get_data_setup(self, args: Any) -> DataSetup:
        return MacrosSetup(args, self.assets_path)

