from typing import List, Any
from abc import ABC, abstractmethod
from generator.pluggability.strategy import Strategy
from generator.pluggability.data_setup import DataSetup
from generator.common.macros.macros import Macros

class Plugin(ABC):
    def get_strategies(self, args: Any, macros: Macros) -> List[Strategy]:
        return []

    @abstractmethod
    def get_data_setup(self, args: Any) -> DataSetup:
        pass

    def add_custom_params(self, params: Any):
        return
