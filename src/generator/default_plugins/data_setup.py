import lxml.etree as ET

from generator.common.macros.macros import MacrosFactory
from generator.pluggability.data_setup import DataSetup
from typing import Any
class DefaultDataSetup(DataSetup):

    def __init__(self, args: Any):
        super().__init__(args)

    def initialize_xml_tree(self, xml_tree: ET.ElementTree) -> ET.ElementTree:
        # TODO define relative path
        return ET.parse(r"C:\Users\Michal\PycharmProjects"
                        r"\TRToolsTDFGenerator\src\generator\default_plugins"
                        r"\strategies\assets\template.xml")

    def initialize_macros(self, macros_factory: MacrosFactory) -> MacrosFactory:
        version = macros_factory.add_token("tool_version",
                                           self.args.package_version)
        macros_factory.add_requirement(self.args.package_name, version)

        return macros_factory
