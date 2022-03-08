from typing import List, Tuple, Any
from abc import ABC, abstractmethod
from common.stages import StrategyStage
from common.stage_order import StageOrder


class Strategy(ABC):
    def __init__(self, params: Any,
                 stage: StrategyStage,
                 stage_order: StageOrder,
                 manual_order: int = 0):
        self.params = params
        self.stage = stage
        self.stage_order = stage_order
        self.manual_order = manual_order

    # applies strategy to xml_output and than returns this modified output
    @abstractmethod
    def apply_strategy(self, tool_input: Any, xml_output: Any) -> Any:
        pass


