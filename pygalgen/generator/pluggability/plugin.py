from typing import List, Any, Optional
from abc import ABC, abstractmethod
from pygalgen.generator.pluggability.strategy import Strategy
from pygalgen.generator.pluggability.data_setup import DataSetup
from pygalgen.generator.common.macros.macros import Macros


class Plugin(ABC):
    def __init__(self, order: int, name: str, assets_path: Optional[str]):
        self.assets_path = assets_path
        self.name = name
        self.order = order

    @abstractmethod
    def get_strategies(self, args: Any, macros: Macros) -> List[Strategy]:
        return []

    @abstractmethod
    def get_data_setup(self, args: Any) -> DataSetup:
        pass

    @abstractmethod
    def add_custom_params(self, params: Any):
        return

    def __lt__(self, other):
        if not isinstance(other, Plugin):
            raise RuntimeError("Cannot sort Plugins with other objects")
        if self.order != other.order:
            return self.order < other.order

        raise RuntimeError(f"{self.__class__.__name__} and"
                           f" {other.__class__.__name__} have"
                           f" sort order"
                           f" {self.order}\n"
                           f"Plugin execution pipeline is not able to sort "
                           f"plugins correctly, exiting...")