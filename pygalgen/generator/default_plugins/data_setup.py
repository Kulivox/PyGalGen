import os

import lxml.etree as ET

from pygalgen.generator.common.macros.macros import MacrosFactory
from pygalgen.generator.pluggability.data_setup import DataSetup
from typing import Any
class DefaultDataSetup(DataSetup):

    def __init__(self, args: Any, assets: str):
        super().__init__(args)
        self.assets_path = assets

    def initialize_xml_tree(self, xml_tree: ET.ElementTree) -> ET.ElementTree:
        # TODO define relative path
        return ET.parse(os.path.join(self.assets_path, "template.xml"))

    def initialize_macros(self, macros_factory: MacrosFactory) -> MacrosFactory:
        version = macros_factory.add_token("tool_version",
                                           self.args.package_version)
        macros_factory.add_requirement(self.args.package_name, version)

        return macros_factory
