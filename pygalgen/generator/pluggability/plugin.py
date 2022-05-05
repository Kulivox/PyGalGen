"""
Module contains Plugin class definition
"""
import argparse
from typing import List, Any, Optional
from abc import ABC, abstractmethod
from pygalgen.generator.pluggability.strategy import Strategy
from pygalgen.generator.pluggability.data_setup import DataSetup
from pygalgen.generator.common.macros.macros import Macros


class Plugin(ABC):
    """
    This class encapsulates the plugin itself.
    Each plugin should extend the bae Plugin class,
    and define the initialization of strategies,
    data setup and Plugin specific arguments

    Attributes
    ---------
    assets_path : str
     path to plugin assets, a directory containing static data used for
     generating wrappers
    name : str
     name of the plugin, used to properly log actions
    order :
     parameter defining the order of this plugin. Plugins are sorted at the
      start of execution, and the order argument defines in
      which order data is set up and plugins are applied

    """
    def __init__(self, order: int, name: str, assets_path: Optional[str]):
        self.assets_path = assets_path
        self.name = name
        self.order = order

    @abstractmethod
    def get_strategies(self, args: Any, macros: Macros) -> List[Strategy]:
        """
        Function initializes Strategies and returns a list of them,
        in any order, as they should be sorted later

        Parameters
        ----------
        args : Any
         parsed out arguments
        macros : Macros
         initialized macros

        Returns
        -------

        """
        return []

    @abstractmethod
    def get_data_setup(self, args: Any) -> DataSetup:
        """
        Function initializes data setup of the plugin
        Data setup is performed in the order defined
        by the order parameter of parent plugin

        Parameters
        ----------
        args : Any
         parsed out program arguments
        """
        pass

    @abstractmethod
    def add_custom_params(self, params: argparse.ArgumentParser):
        """
        Function used to add custom, plugin specific command-line arguments
        These arguments should be encapsulated in their specific argument
        section

        Parameters
        ----------
        params : ArgumentParser
         argument parser to be initialized
        """
        return

    def __lt__(self, other):
        """
        Less than operation has to be defined, to ensure plugins are
        sorted properly
        """
        if not isinstance(other, Plugin):
            raise RuntimeError("Cannot sort Plugins with other objects")
        if self.order != other.order:
            return self.order < other.order

        raise RuntimeError(f"{self.__class__.__name__} and"
                           f" {other.__class__.__name__} have"
                           f" sort order"
                           f" {self.order}\n"
                           f"Plugin execution pipeline is not able to sort "
                           f"plugins correctly, exiting...")