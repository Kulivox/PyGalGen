from typing import Any

import lxml.etree as ET

from pygalgen.generator.common.macros.macros import Macros
from pygalgen.generator.common.xml_utils import create_element
from pygalgen.generator.pluggability.strategy import Strategy, StrategyStage


class DefaultOutputs(Strategy):
    """
    This is a very basic Output strategy, that generates outputs for
    stdout and stderr redirects
    """
    def __init__(self, args: Any, macros: Macros):
        super().__init__(args, macros, StrategyStage.OUTPUTS)

    def apply_strategy(self, xml_output: ET.ElementTree) -> Any:
        if self.args.dont_redirect_output:
            return xml_output
        outputs = xml_output.find(".//outputs")
        create_element(outputs, "data", {"name": "stdout",
                                           "label": "STD out output",
                                           "format": "txt"})
        create_element(outputs, "data", {"name": "stderr",
                                         "label": "STD err output",
                                         "format": "txt"})

        return xml_output