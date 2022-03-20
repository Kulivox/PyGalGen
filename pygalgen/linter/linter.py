import argparse
import lxml.etree as ET

from common.utils import LINTER_MAGIC


def magic_found(element: ET.Element):
    if LINTER_MAGIC in element.tag:
        return True

    for name, value in element.attrib.items():
        if LINTER_MAGIC in name or LINTER_MAGIC in value:
            return True
    if element.text is not None:
        return LINTER_MAGIC in element.text

    return False


def report_problems(element: ET.Element):
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

    return 0


if __name__ == '__main__':
    run()
