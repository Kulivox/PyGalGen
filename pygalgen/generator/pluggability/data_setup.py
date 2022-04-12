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

    def __lt__(self, other):
        other: DataSetup

        if self.order != other.order:
            return self.order < other.order

        raise RuntimeError(f"{self.__class__.__name__} and"
                           f" {other.__class__.__name__} have"
                           f" the same sort order"
                           f" {self.order}\n"
                           f"This is not allowed.")
