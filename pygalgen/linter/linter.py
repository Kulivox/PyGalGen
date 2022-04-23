import argparse
import lxml.etree as ET

from pygalgen.common.utils import LINTER_MAGIC


def magic_found(element: ET.Element) -> bool:
    """
    Function reports whether current element contains magic tag

    Parameters
    ----------
    element : current XML element

    Returns
    -------
    True if magic was found, otherwise False
    """
    if LINTER_MAGIC in element.tag:
        return True

    for name, value in element.attrib.items():
        if LINTER_MAGIC in name or LINTER_MAGIC in value:
            return True
    if element.text is not None:
        return LINTER_MAGIC in element.text

    return False


def report_problems(element: ET.Element):
    """
    This function recursively goes through entire xml tree
    and prints out lines of elements containing problems.
    Problematic elements contain magic strings

    Parameters
    ----------
    element: xml element that is currently being checked
    """
    if magic_found(element):
        print(f"Problem found at line {element.sourceline}")

    for child in element:
        report_problems(child)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help="Path to input file",
                        required=True)
    args = parser.parse_args()

    tree = ET.parse(args.path)
    report_problems(tree.getroot())


if __name__ == '__main__':
    run()
