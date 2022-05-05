"""
Defines header strategy of default plugin
"""
from typing import Any

import lxml.etree as ET

from pygalgen.generator.common.xml_utils import create_element
from pygalgen.generator.pluggability.strategy import Strategy, StrategyStage
from pygalgen.generator.common.macros.macros import Macros


class HeaderStrategy(Strategy):
    """
    Defines default strategy for headers. Headers are things
    like the root tool element, description, generally things that appear at
    the top of the document, if developer follows best practices of tool
    development
    """
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

    def apply_strategy(self, xml_output: ET.ElementTree) -> Any:
        root = xml_output.getroot()
        root.attrib["id"] = self.args.tool_name
        root.attrib["name"] = self.args.tool_name[0].upper() +\
                              self.args.tool_name[1:]
        root.attrib["version"] = self. \
            macros.get_real_token_name("tool_version")

        requirements = root.find(".//requirements")
        requirements.getparent().remove(requirements)

        create_element(root, "description", dict(), self.args.descr, pos=0)
        root.insert(1, self.create_macros_import())

        root.insert(2, self.expand_requirements())



        return xml_output
