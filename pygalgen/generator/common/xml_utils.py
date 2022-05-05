"""
Module containing utility function for manipulation of wrapper XML files
"""
from typing import List, Tuple, Dict, Optional
import lxml.etree as ET
import re


def create_param(parent: ET.Element, argument_attr: str, type_attr: str,
                 optional_attr: bool, label_attr: str,
                 help_attr: Optional[str] = None,
                 format_attr: Optional[None] = None) -> ET.Element:
    """
    Creates param element, used in inputs. Valid parents are 'inputs',
    'section' and 'repeat'

    Parameters
    ----------
    parent : ET.Element
     parent of the param, can be inputs element or section
    argument_attr : str
     value of 'argument' attribute of resulting param element
    type_attr : str
     value of 'type' attribute
    optional_attr : bool
     attribute signifying whether param is optional
    label_attr : str
     label attr of resulting param element
    help_attr : Optional[str], help_attr = None
     optional help attr
    format_attr : Optional[None], format_attr = None 
     optional format attr

    Returns
    -------
    
    created param element
    
    """
    attributes = {
        "argument": argument_attr,
        "type": type_attr,
        "format": format_attr,
        "optional": str(optional_attr).lower(),
        "label": label_attr
    }

    if help_attr is not None:
        attributes["help"] = help_attr
    # this might seem weird but it is done like this for correct order
    # of attributes
    if format_attr is None:
        attributes.pop("format")

    return create_element(parent, "param", attributes)


def create_section(parent: ET.Element, name: str, title: str, expanded: bool,
                   help_: Optional[str] = None) -> ET.Element:
    """
    Creates section element, used in inputs

    Parameters
    ----------
    parent : ET.Element
     parent of new section
    name : str
     name attr of section
    title : str
     title of section
    expanded : bool
     parameter defining whether the section is open in Galaxy UI by default
    help_ : Optional[str]
     optional help attr

    Returns
    -------
    element : ET.Element
     resulting section
    """
    attributes = {
        "name": re.sub("[/\\-* ()]", "_", name).lower(),
        "title": title,
        "expanded": str(expanded).lower()
    }

    if help_ is not None:
        attributes["help"] = help_

    return create_element(parent, "section", attributes)


def create_repeat(parent: ET.Element, title: str,
                  min_reps: Optional[int] = None,
                  max_reps: Optional[int] = None,
                  default_reps: Optional[int] = None,
                  help_: Optional[str] = None) -> ET.Element:
    """
    Creates repeat element

    Parameters
    ----------
    parent : ET.Element
     parent of repeat
    title : str
     title attr of repeat
    min_reps : Optional[int]
     optional minimal repetitions
    max_reps : Optional[int]
     optional max repetitions
    default_reps : Optional[int]
     optional default amount of repetitions
    help_ : Optional[str]
     optional help attr

    Returns
    -------

    Repeat element

    """
    attributes = {
        "name": title,
        "title": title,
        "min_reps": min_reps,
        "max_reps": max_reps,
        "default_reps": default_reps,
        "help": help_,
    }

    names = list(attributes.keys())
    for name in names:
        if attributes[name] is None:
            attributes.pop(name)

    return create_element(parent, "repeat", attributes)


def create_option(parent: ET.Element, value: str, text: str) -> ET.Element:
    """
    Creates option element for select parameters

    Parameters
    ----------
    parent : ET.Element
    parent xml element
    value : str
     value of option element
    text : str
     visible text of the option element

    Returns
    -------
     option element
    """
    attrs = {
        "value": value
    }

    return create_element(parent, "option", attrs, text)


def create_element(parent: ET.Element, tag: str, attribs: dict[str, str],
                   body: Optional[str] = None, pos: int = -1):
    """
    Creates child element, wrapper function for ET.SubElement
    User can set optional position, which defines position in child elements
    of a parent

    Parameters
    ----------
    parent : ET.Element
     parent of the attribute
    tag : str
     tag of the attribute
    attribs : dict[str, str]
     dictionary of element attributes
    body : Optional[str]
     text in the body of the element
    pos : int
     position in the child elements of parent.
     By default, the value is -1, so it is inserted at the end of the list
     of children

    Returns
    -------
    lxml element initialized by provided parameters
    """
    if pos == -1:
        elem = ET.SubElement(parent, tag, attribs)
    else:
        elem = ET.Element(tag, attribs)
        parent.insert(pos, elem)

    elem.text = body
    return elem


def find_elements_by_name_attrib(tag: str, name: str, root: ET.Element) \
        -> List[ET.Element]:
    """
    Utility function used to look up elements based on their tag and 'name'
    or 'argument' attributes

    Parameters
    ----------
    tag : str
     tag of the element
    name : str
     substring of values of argument or name attributes
    root : ET.Element
     root element of the search

    Returns
    -------
    List of elements with tag 'tag', whose name or argument attribs contain
    'name'
    """
    return root.xpath(f'.//{tag}[contains(@name, "{name}")] |'
                      f'.//{tag}[contains(@argument, "{name}")]')
