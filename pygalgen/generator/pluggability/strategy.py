"""
Module contains class definition of Strategy, and definitions of
enums used for ordering strategies
"""
from enum import Enum
from typing import List, Tuple, Any
from abc import ABC, abstractmethod

from lxml.etree import ElementTree
from pygalgen.generator.common.macros.macros import Macros

class ProcessingOrder(Enum):
    """
    Defines the Processing order of strategies, for more fine-grained ordering
    """
    BEFORE_DEFAULT = -1
    DEFAULT = 0
    AFTER_DEFAULT = 1

    def __lt__(self, other):
        return self.value < other.value


class StrategyStage(Enum):
    """
    Used to define the execution stage of strategy
    """
    HEADER = 1
    PARAMS = 2
    OUTPUTS = 3
    COMMAND = 4
    TESTS = 5
    HELP = 6
    CITATIONS = 7
    POST_PROCESSING = 8

    def __lt__(self, other):
        return self.value < other.value

class Strategy(ABC):
    """
    Defines strategy for creation of specific parts of the Galaxy wrappers
    """
    def __init__(self, args: Any, macros: Macros, stage: StrategyStage,
                 stage_order: ProcessingOrder = ProcessingOrder.DEFAULT,
                 manual_order: int = 0):
        self.args = args
        self.stage = stage
        self.macros = macros
        self.stage_order = stage_order
        self.manual_order = manual_order

    # applies strategy to xml_output and than returns this modified output
    @abstractmethod
    def apply_strategy(self, xml_output: ElementTree)\
            -> Any:
        """
        Used to apply strategy on the provided XML tree
        """
        pass

    # necessary to correctly sort strategies during execution
    def __lt__(self, other):
        other: Strategy

        if self.stage != other.stage:
            return self.stage < other.stage

        if self.stage_order != other.stage_order:
            return self.stage_order < other.stage_order

        if self.manual_order != other.manual_order:
            return self.manual_order < other.manual_order

        raise RuntimeError(f"{self.__class__.__name__} and"
                           f" {other.__class__.__name__} have"
                           f" the same sort order within plugin"
                           f" {self.stage_order}:{self.stage_order}"
                           f":{self.manual_order}\n"
                           f"This is not allowed.")


