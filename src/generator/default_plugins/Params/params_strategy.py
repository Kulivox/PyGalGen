from typing import Any
from generator.common.stages import StrategyStage
from generator.common.stage_order import StageOrder
from generator.pluggability.strategy import Strategy


class ParamsStrategy(Strategy):
    STAGE = StrategyStage.PARAMS
    STAGE_ORDER = StageOrder.DEFAULT

    def __init__(self):
        super(ParamsStrategy, self).__init__(self.STAGE, self.STAGE_ORDER)

    def apply_strategy(self, tool_input: Any, xml_output: Any) -> Any:
        return xml_output + "PARAMS"
