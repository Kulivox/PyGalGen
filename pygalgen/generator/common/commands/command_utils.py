"""
Module used for creation and manipulation of template elements
are parts of template, separated from the rest by comments
with specific structure
Example of the comments:
    ## foo definition
    ... block itself ...
    ## end foo definition

Elements can be nested
"""
from typing import List
import lxml.etree as ET

SPACE = " "

class DefinitionNotFoundException(Exception):
    """
    Exception raised if part of template definition cannot be found
    """
    pass

def create_element_with_body(kind: str, head: str,
                             body: List[str], comment: str,
                             depth: int,
                             indent: int = 3) -> str:
    """
    Function used to create block of template, like if or loop

    Parameters
    ----------
    kind : str
     string defining what kind of element is created, for example if or for
     (loop)
    head : str
     body of block header, for example predicate of condition, or the
     body of loop
    body : str
     body of the block, can be another element
    comment : str
     comment, used to set the start and end of the block
    depth : int
     integer, used to set the depth of the current element.
     This value is used to indent the block properly
    indent : int
      default value for size of the block indent

    Returns
    -------
    string containing the created template element
    """
    result = (f"{depth * indent * SPACE}## {comment}\n"
              f"{depth * indent * SPACE}#{kind} {head}:\n{indent * SPACE}")

    result += ("\n" + indent * SPACE).join(body) + "\n"

    result += f"{depth * indent * SPACE}#end {kind}\n"
    result += f"{depth * indent * SPACE}## end {comment}\n"
    return result


def extract_variable_name(attribute_name: str):
    """
    Function used to transform attribute names into cheetah variables

    attribute names look like standard shell arguments (--attr-a),
    so they need to be converted to look more like python variables (attr_a)
    Parameters
    ----------
    attribute_name : str
     name of the attribute

    Returns
    -------
    transformed name
    """
    return attribute_name.lstrip("-").replace("-", "_")

def transform_basic_param(element: ET.Element, section: str, depth: int) \
        -> str:
    """
    Utility function used to transform parameter xml element into command
    element

    Parameters
    ----------
    element : lxml Element
     param element to be used as template
    section : str
     section of the element. Sections serve as namespaces,
      they have to be used to create proper names
    depth : int
     depth of current param (level of nesting)

    Returns
    -------
    Transformed param into template element
    """
    assert element.tag == "param"

    attributes = element.attrib

    body_expression = f"{attributes['argument']}"
    name = extract_variable_name(attributes['argument'])
    variable = f"${section}.{name}"

    if attributes["type"] != "boolean":
        body_expression += f" {variable}"

    return create_element_with_body("if", variable, [body_expression],
                                    f"{name} definition", depth)


def transform_repeat(element: ET.Element, section: str, depth: int):
    """
       Utility function used to transform repeat xml element into command
       element, a for loop

       Parameters
       ----------
       element : lxml Element
        repeat  element to be used as template
       section : str
        section of the element. Sections serve as namespaces,
         they have to be used to create proper names
       depth : int
        depth of current param (level of nesting)

       Returns
       -------
       Transformed repeat into template element
       """
    assert element.tag == "repeat"

    attributes = element.attrib

    param = element.find(".//param")
    iteration_var = "$item"

    head_expression = (f"{iteration_var}"
                       f" in ${section}."
                       f"{extract_variable_name(attributes['name'])}")

    return create_element_with_body("for", head_expression,
                                    [transform_basic_param(param,
                                                           iteration_var.lstrip("$"), 1)],
                                    f"{attributes['name']} definition", depth)


def update_definition(command_template: str, param_name: str,
                      new_definition: str) -> str:
    """
    Utility function used to look up command elements and update them

    Parameters
    ----------
    command_template : str
     string containing the command template
    param_name : str
     name of the command element to look for
    new_definition : str
     new definition of the command element

    Returns
    -------
    Updated command template
    """
    old_text = command_template
    start_line = f"## {param_name} definition\n"
    start = old_text.find(start_line)

    if start == -1:
        raise DefinitionNotFoundException

    start = start + len(start_line)

    end_line = f"## end {param_name} definition\n"
    end = old_text.find(end_line, start=start)
    return old_text[0:start] + new_definition + old_text[end:]

