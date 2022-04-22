import os
from typing import Any

import lxml.etree as ET

from pygalgen.generator.common.macros.macros import MacrosFactory
from pygalgen.generator.pluggability.data_setup import DataSetup
from pygalgen.generator.pluggability.strategy import ProcessingOrder


class MacrosSetup(DataSetup):
    def __init__(self, args: Any, assets: str):
        super().__init__(args)
        self.assets_path = assets

    def initialize_xml_tree(self, xml_tree: ET.ElementTree) -> ET.ElementTree:
        return xml_tree

    def initialize_macros(self,
                          macros_factory: MacrosFactory) -> MacrosFactory:
        with open(
                os.path.join(self.assets_path, "index_function.cheetah")) as f:
            macros_factory.add_token("INDEX_VCFS", str(f.read()), cdata=True)

        macros_factory.add_requirement("samtools", "1.14")

        options = ET.parse(os.path.join(self.assets_path, "genotypers.xml"))\
            .getroot()

        macros_factory.add_xml_import("vcfTypes", options[:])

        return macros_factory
