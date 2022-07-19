import unittest

from pygalgen.generator.common.params.argument_parser_conversion import \
    obtain_and_convert_parser_from_str, extract_useful_info_from_parser

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

GETTING_RETARDED = """
import argparse


class TestParser(argparse.ArgumentParser):
    def hah(self):
        print("woof")
"""



class SingleArgumentEachAction(unittest.TestCase):
    def test_store(self):
        STORE = SINGLE_ARGUMENT_2.format(action="store")
        parser = obtain_and_convert_parser_from_str(STORE)
        info = extract_useful_info_from_parser(parser, dict(), set())
        print(info)


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

