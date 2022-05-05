"""
The module contains class definition of DataSetup
"""
import abc
from pygalgen.generator.common.macros.macros import MacrosFactory
from lxml.etree import ElementTree
from pygalgen.generator.pluggability.strategy import ProcessingOrder
from typing import Any

class DataSetup(abc.ABC):
    """
    DataSetup is an abstract class which should be extended by Plugin specific
    classes.
    This class defines the macros initialization and the default starting xml
    tree
    """
    def __init__(self, args: Any):
        self.args = args

    @abc.abstractmethod
    def initialize_macros(self, macros_factory: MacrosFactory)\
            -> MacrosFactory:
        pass

    @abc.abstractmethod
    def initialize_xml_tree(self, xml_tree: ElementTree) -> ElementTree:
        pass


