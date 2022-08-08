import unittest

from pygalgen.generator.common.params.argument_parser_conversion import \
    obtain_and_convert_parser_from_str, extract_useful_info_from_parser, \
    ParamInfo

SINGLE_ARGUMENT = """
from argparse import ArgumentParser

def arg_parser():
    parser = ArgumentParser()
    parser.add_argument("-f", "--foo", action="{action}")
    return parser
"""

SINGLE_ARGUMENT_2 = """
import argparse

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--foo", action="{action}")
    default = parser.add_argument_group("Default program parameters")

    default.add_argument("--path",
                         help="Path to the source file",
                         required=True)
    return parser
"""


class SingleArgumentEachAction(unittest.TestCase):
    def test_store(self):
        STORE = SINGLE_ARGUMENT.format(action="store")
        parser = obtain_and_convert_parser_from_str(STORE)
        info, _ = extract_useful_info_from_parser(parser, dict(), set())

        self.assertEqual(info[1], ParamInfo(
            type="text",
            name="foo",
            argument="--foo",
            label="foo",
            section="default",
            section_label="default",
            default_val=None,
            custom_attributes=[],
            nargs=0,
            help=None,
            optional=False,
            is_repeat=False,
            is_select=False,
            choices=None,
            is_flag=False
        ))

    def test_const(self):
        pass

    def test_true(self):
        pass

    def append(self):
        pass

    def count(self):
        pass

    def extend(self):
        pass


class MultipleArgumentsSimple(unittest.TestCase):
    def test_something_else(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
