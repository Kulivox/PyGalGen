from typing import List
import lxml.etree as ET

SPACE = " "


def create_element_with_body(kind: str, head: str,
                             body: List[str], comment: str,
                             depth: int,
                             indent: int = 3) -> str:
    result = (f"{depth * indent * SPACE}## {comment}\n"
              f"{depth * indent * SPACE}#{kind} {head}:\n{indent * SPACE}")

    result += ("\n" + indent * SPACE).join(body) + "\n"

    result += f"{depth * indent * SPACE}#end {kind}\n"
    return result

# attribute names look like standard shell arguments,
# so they need to be converted to look more like python variables
def extract_variable_name(attribute_name: str):
    return attribute_name.lstrip("-").replace("-", "_")

def transform_basic_param(element: ET.Element, section: str, depth: int):
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

