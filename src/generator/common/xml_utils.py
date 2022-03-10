from typing import List, Tuple, Dict, Optional
import xml.etree.ElementTree as ET

def create_param_element(parent: ET.Element,
                         argument_attr: str,
                         type_attr: str,
                         optional_attr: bool,
                         label_attr: str,
                         help_attr: Optional[str] = None) -> ET.Element:
    arguments = {
        "argument": argument_attr,
        "type": type_attr,
        "optional": str(optional_attr).lower(),
        "label": label_attr
    }

    if help_attr is not None:
        arguments["help"] = help_attr

    return ET.SubElement(parent, "param", arguments)


