"""
Module containing utilities used throughout PyGalGen generator
"""
from typing import Tuple


def parse_argument_comma_sep_list(argument: str) -> Tuple:
    """
    Parses command line arguments containing comma delimited data. The data
    can be further divided by colon (:)

    Parameters
    ----------
    argument : str
     comma delimited list of items

    Yields
    -------
    Tuple of sub-elements that are delimited by :, from comma separated list

    Examples
    --------
    Input: 'person:name,person:name'
    Result of single iteration: (person, name)
    """
    for item in argument.split(","):
        yield tuple(item.split(":"))