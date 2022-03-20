from typing import List, Any
from abc import ABC, abstractmethod
from pygalgen.generator.pluggability.strategy import Strategy
from pygalgen.generator.pluggability.data_setup import DataSetup
from pygalgen.generator.common.macros.macros import Macros

class Plugin(ABC):
    def __init__(self, assets_path: str):
        self.assets_path = assets_path

    def get_strategies(self, args: Any, macros: Macros) -> List[Strategy]:
        return []

    @abstractmethod
    def get_data_setup(self, args: Any) -> DataSetup:
        pass

    def add_custom_params(self, params: Any):
        return
