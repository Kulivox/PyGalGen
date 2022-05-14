import argparse
import lxml.etree as ET
from typing import IO
from pygalgen.common.utils import LINTER_MAGIC


def report_problems(file: IO) -> bool:
    """
    This function goes through the input file line by line and
    outputs line numbers along with the text surrounding the magic tag.
    If no such lines are found, it returns True to signify the file is
    MAGIC-less

    Parameters
    ----------
    file: IO
     file object representing the wrapper that is being verified

    Returns
    --------
    magicless:bool
        a boolean which is true if no problems were found,
         or False if lines with magic tag were found
    """
    magicless = True
    line_number = 0
    for line in file.readlines():
        line_number += 1
        index = line.find(LINTER_MAGIC)
        if index != -1:
            magicless = False
            print(f"{line_number}: {line.strip()}")

    return magicless


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help="Path to input file",
                        required=True)
    args = parser.parse_args()

    try:
        with open(args.path, "r") as file:
            magicless = report_problems(file)
    except FileNotFoundError:
        print("File not found")
        exit(2)

    if not magicless:
        exit(1)


if __name__ == '__main__':
    run()
