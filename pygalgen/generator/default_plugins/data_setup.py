"""
Module defines data setup of Default plugin
"""
import os
import lxml.etree as ET
from pygalgen.generator.common.macros.macros import MacrosFactory
from pygalgen.generator.common.utils import parse_argument_comma_sep_list
from pygalgen.generator.pluggability.data_setup import DataSetup
from typing import Any


class DefaultDataSetup(DataSetup):
    """
    Defines data setup of this plugin. During data setup,
    macros are created and default xml is initialized
    """
    def __init__(self, args: Any, assets: str):
        super().__init__(args)
        self.assets_path = assets

    def initialize_xml_tree(self, xml_tree: ET.ElementTree) -> ET.ElementTree:
        return ET.parse(os.path.join(self.assets_path, "template.xml"))

    def initialize_macros(self, macros_factory: MacrosFactory) -> MacrosFactory:
        macros_factory.add_token("tool_version",
                                           self.args.tool_version)
        for name, version in parse_argument_comma_sep_list(self.args.requirements):
            macros_factory.add_requirement(name, version)

        return macros_factory
