##############################################################################
#### THIS MODULE IS CURRENTLY WORK IN PROGRESS ###############################
##############################################################################

from copy import deepcopy

import lxml.etree as ET
from typing import Optional, List, Tuple
from pygalgen.common.utils import LINTER_MAGIC


def _update_description(old_description: Optional[ET.Element],
                        new_description: ET.Element) -> ET.Element:
    if old_description is None:
        return new_description

    if old_description.text != new_description.text:
        new_description.text = LINTER_MAGIC + " Updated descr: " + new_description.text
        return new_description

    return old_description


def _elem_names(inputs: ET.Element, path: List[Tuple[str, str]]):
    for item in inputs:
        name = _get_input_name(item)

        yield name, item.tag, path, item
        yield from _elem_names(item, path + [(name, item.tag)])


def _get_input_name(item: ET.Element) -> str:
    if "name" in item.attrib:
        name = item.attrib["name"]
    else:
        name = item.attrib["argument"].lstrip("-")
    return name


def _shallow_equality(left: ET.Element, right: ET.Element):
    return left.tag == right.tag and left.text == right.text and left.attrib == right.attrib


def _get_element_by_path(root: ET.Element, path: List[Tuple[str, str]]):
    def _recursive_element_by_path(current_elem: ET.Element, path_index: int):
        if path_index == len(path):
            return current_elem

        name, tag = path[path_index]
        for item in current_elem:
            item_name = _get_input_name(item)
            if item_name == name and item.tag == tag:
                result = _recursive_element_by_path(item, path_index + 1)
                if result is not None:
                    return result

    return _recursive_element_by_path(root, 0)


def _update_inputs(old_inputs: ET.Element, new_inputs: ET.Element):
    updated_inputs = deepcopy(new_inputs)
    old_elems = dict(((name, tag), (path, item)) for name, tag, path, item in
                     _elem_names(old_inputs, []))
    new_elems = dict(((name, tag), (path, item)) for name, tag, path, item in
                     _elem_names(updated_inputs, []))

    # In this loop, all of the new params and elements are looked up in the
    # set of old ones. If they existed before, user is notified through new
    # attribute
    for name, tag, path, new_item in _elem_names(updated_inputs, []):
        if (name, tag) not in old_elems:
            continue

        old_path, old_item = old_elems[(name, tag)]
        if path == old_path:
            if _shallow_equality(old_item, new_item):
                new_item.attrib[
                    "dev-notification"] = f"{LINTER_MAGIC} Updated element"
        else:
            new_item.attrib[
                "dev-notification"] = f"{LINTER_MAGIC} Moved element"
    # This loop will copy elements that existed in old file but don't exist
    # in the new one This ensures that additions done by user are kept in place
    for name, tag, path, old_item in _elem_names(old_inputs, []):
        if (name, tag) in new_elems:
            continue
        parent = _get_element_by_path(updated_inputs, path)
        if parent is None:
            parent = updated_inputs

        old_item_copy = old_item.copy()
        old_item_copy.children = []
        parent.append(old_item_copy)

    return updated_inputs


def _update_command():
    pass


def _update_outputs():
    pass


def _update_tests():
    pass


def _update_citations(old_citations: Optional[ET.Element],
                      new_citations: ET.Element) -> ET.Element:
    if old_citations is None:
        return new_citations

    for citation in new_citations:
        citation.text = LINTER_MAGIC + " Possibly updated citation " \
                        + citation.text

    return new_citations


def update_file(old_xml: ET.ElementTree,
                new_xml: ET.ElementTree) -> ET.ElementTree:
    pass
