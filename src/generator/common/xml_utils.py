from typing import List, Tuple, Dict, Optional
import lxml.etree as ET

def create_param(parent: ET.Element, argument_attr: str, type_attr: str,
                 optional_attr: bool, label_attr: str,
                 help_attr: Optional[str] = None,
                 format_attr: Optional[None] = None) -> ET.Element:
    attributes = {
        "argument": argument_attr,
        "type": type_attr,
        "optional": str(optional_attr).lower(),
        "label": label_attr
    }

    if help_attr is not None:
        attributes["help"] = help_attr

    if format_attr is not None:
        attributes["format"] = format_attr

    return ET.SubElement(parent, "param", attributes)

def create_section(parent: ET.Element, title: str, expanded: bool,
                   help_: Optional[str] = None):
    attributes = {
        "name": title.lower().replace(" ", "_"),
        "title": title,
        "expanded": str(expanded).lower()
    }

    if help_ is not None:
        attributes["help"] = help_

    return ET.SubElement(parent, "section", attributes)


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

    return ET.SubElement(parent, "repeat", attributes)

def create_option(parent: ET.Element, value: str, text: str):
    attrs = {
        "value": value
    }

    element = ET.SubElement(parent, "option", attrs)
    element.text = text
    return element
