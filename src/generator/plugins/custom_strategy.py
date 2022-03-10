from typing import Any
from generator.common.stages import StrategyStage
from generator.common.stage_order import StageOrder

from generator.pluggability.strategy import Strategy

class CustomStrategy(Strategy):
    STAGE = StrategyStage.HEADER_AND_STRUCTURE

    def __init__(self, args: Any):
        super(CustomStrategy, self).__init__(args, self.STAGE)

    def apply_strategy(self, tool_input: Any, xml_output: Any) -> Any:
        return xml_output + " CUSTOM SHIT "
