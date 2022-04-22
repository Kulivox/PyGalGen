from typing import Set, Any
import lxml.etree as ET

import pygalgen.generator.common.xml_utils as xu
from pygalgen.generator.pluggability.strategy import Strategy, StrategyStage


class TRToolsParams(Strategy):
    STAGE = StrategyStage.PARAMS

    def __init__(self, args: Any, macros):
        super(TRToolsParams, self).__init__(args, macros, self.STAGE)

    def apply_strategy(self, xml_output: ET.ElementTree) -> ET.ElementTree:
        inputs = xml_output.find(".//inputs")

        for param in xu.find_elements_by_name_attrib("param", "vcftype", inputs):
            param.attrib["help"] = "Genotyper that was used to create this VCF input"
            param.attrib["type"] = "select"
            ET.SubElement(param, "expand", {"macro": "vcfTypes"})
        return xml_output
