from typing import Any

from lxml.etree import ElementTree
import lxml.etree as ET

from pygalgen.generator.common.macros.macros import Macros
from pygalgen.generator.pluggability.strategy import Strategy, StrategyStage


class Citations(Strategy):
    STAGE = StrategyStage.CITATIONS

    def __init__(self, args: Any, macros: Macros):
        super().__init__(args, macros, self.STAGE)

    def apply_strategy(self, xml_output: ElementTree) -> Any:
        citations = xml_output.find(".//citations")
        if citations is None:
            citations = ET.SubElement(xml_output.getroot(), "citations")

        citation = ET.SubElement(citations, "citation", {"type": "bibtex"})
        with open(self.args.citations, "r", encoding="utf-8") as file:
            citation.text = file.read()

        return xml_output
