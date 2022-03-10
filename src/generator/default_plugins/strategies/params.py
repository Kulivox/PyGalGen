from typing import Any

from generator.pluggability.strategy import Strategy
from generator.common.stages import StrategyStage


class DefaultParams(Strategy):
    STAGE = StrategyStage.PARAMS

    def __init__(self, args: Any):
        super(DefaultParams, self).__init__(args, self.STAGE)

    def apply_strategy(self, tool_input: Any, xml_output: Any) -> Any:
        pass
