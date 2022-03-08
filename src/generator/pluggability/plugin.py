from typing import List, Any
from abc import ABC, abstractmethod
from generator.pluggability.strategy import Strategy

class Plugin(ABC):
    def get_strategies(self) -> List[Strategy]:
        return []

    def add_custom_params(self, params: Any):
        return
