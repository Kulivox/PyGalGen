from typing import List, Tuple, Dict, Optional
import lxml.etree as ET
import re


def create_param(parent: ET.Element, argument_attr: str, type_attr: str,
                 optional_attr: bool, label_attr: str,
                 help_attr: Optional[str] = None,
                 format_attr: Optional[None] = None) -> ET.Element:
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
                   help_: Optional[str] = None):
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
                  help_: Optional[str] = None):
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


def create_option(parent: ET.Element, value: str, text: str):
    attrs = {
        "value": value
    }

    return create_element(parent, "option", attrs, text)


def create_element(parent: ET.Element, tag: str, attribs: dict[str, str],
                   body: Optional[str] = None, pos: int = -1):
    if pos == -1:
        elem = ET.SubElement(parent, tag, attribs)
    else:
        elem = ET.Element(tag, attribs)
        parent.insert(pos, elem)

    elem.text = body
    return elem
