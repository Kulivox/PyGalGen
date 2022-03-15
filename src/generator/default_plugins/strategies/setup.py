from typing import Any
import ast
from generator.pluggability.strategy import Strategy, StrategyStage
import xml.etree.ElementTree as ET


class SetupStrategy(Strategy):
    STAGE = StrategyStage.SETUP_AND_MACROS

    def __init__(self, args: Any):
        super().__init__(args, self.STAGE)

    def apply_strategy(self, xml_output: ET.ElementTree) \
            -> ET.ElementTree:
        return ET.parse(r"C:\Users\Michal\PycharmProjects\TRToolsTDFGenerator\src\generator\default_plugins\strategies\assets\template.xml")
