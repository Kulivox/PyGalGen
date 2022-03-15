from enum import Enum
from typing import List, Tuple, Any
from abc import ABC, abstractmethod


class Strategy(ABC):
    def __init__(self, args: Any, stage: StrategyStage,
                 stage_order: StageOrder = StageOrder.AFTER_DEFAULT,
                 manual_order: int = 0):
        self.args = args
        self.stage = stage
        self.stage_order = stage_order
        self.manual_order = manual_order

    # applies strategy to xml_output and than returns this modified output
    @abstractmethod
    def apply_strategy(self, tool_input: Any, xml_output: Any) -> Any:
        pass

    # necessary to correctly sort strategies during execution
    def __lt__(self, other):
        other: Strategy

        if self.stage != other.stage:
            return self.stage < other.stage

        if self.stage_order != other.stage_order:
            return self.stage_order < other.stage_order

        if self.manual_order != other.manual_order:
            return self.manual_order < other.manual_order

        raise RuntimeError(f"{self.__class__.__name__} and"
                           f" {other.__class__.__name__} have"
                           f" the same sort order"
                           f" {self.stage_order}:{self.stage_order}"
                           f":{self.manual_order}\n"
                           f"This is not allowed.")


class StageOrder(Enum):
    BEFORE_DEFAULT = -1
    DEFAULT = 0
    AFTER_DEFAULT = 1

    def __lt__(self, other):
        return self.value < other.value


class StrategyStage(Enum):
    SETUP_AND_MACROS = 0
    HEADER = 1
    PARAMS = 2
    OUTPUTS = 3
    COMMAND = 4
    TESTS = 5
    HELP = 6
    CITATIONS = 7

    def __lt__(self, other):
        return self.value < other.value