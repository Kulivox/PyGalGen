import abc
from pygalgen.generator.common.macros.macros import MacrosFactory
from lxml.etree import ElementTree
from pygalgen.generator.pluggability.strategy import ProcessingOrder
from typing import Any

class DataSetup(abc.ABC):
    def __init__(self, args: Any,
                 order: ProcessingOrder = ProcessingOrder.DEFAULT):
        self.order = order
        self.args = args

    @abc.abstractmethod
    def initialize_macros(self, macros_factory: MacrosFactory)\
            -> MacrosFactory:
        pass

    @abc.abstractmethod
    def initialize_xml_tree(self, xml_tree: ElementTree) -> ElementTree:
        pass
