from typing import Any

import lxml.etree as ET

from pygalgen.generator.pluggability.strategy import Strategy, StrategyStage
from pygalgen.generator.common.macros.macros import Macros


class HeaderStrategy(Strategy):
    STAGE = StrategyStage.HEADER

    def __init__(self, args: Any, macros: Macros):
        super().__init__(args, macros, self.STAGE)

    @staticmethod
    def create_macros_import():
        mcs = ET.Element("macros")
        import_ = ET.SubElement(mcs, "import")
        import_.text = "macros.xml"
        return mcs

    @staticmethod
    def expand_requirements():
        expand = ET.Element("expand", {"macro": "requirements"})
        return expand

    def apply_strategy(self, xml_output: ET.ElementTree,
                       file_path: str, module_name: str) -> Any:
        root = xml_output.getroot()
        root.attrib["id"] = module_name
        root.attrib["name"] = module_name
        root.attrib["version"] = self. \
            macros.get_real_token_name("tool_version")

        requirements = root.find(".//requirements")
        requirements.getparent().remove(requirements)

        root.insert(0, self.create_macros_import())
        root.insert(1, self.expand_requirements())
        return xml_output
