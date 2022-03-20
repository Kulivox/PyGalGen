import lxml.etree as ET
from dataclasses import dataclass
from typing import Union


def _transform_name_to_token_name(name: str):
    return f"@{name}@"


class MacrosFactory:
    def __init__(self):
        self.tokens = {}

        self.imports = {}
        self.requirements: {}

    def load_from_file(self, path: str):
        pass

    def add_token(self, name: str, value: str) -> str:
        token_name = _transform_name_to_token_name(name)
        self.tokens[token_name] = value
        return token_name

    def add_xml_import(self, name: str, value: ET.Element):
        self.imports[name] = value

    def add_requirement(self, name: str, version: str, type_: str = "package"):
        node = \
            self.imports.setdefault("requirements",
                                    ET.Element("requirements"))

        elem = ET.SubElement(node, "requirement",
                             {"type": type_, "version": version})
        elem.text = name

    def create_macros(self) -> "Macros":
        return Macros(self.tokens, self.imports)


@dataclass
class Macros:
    tokens: dict[str, str]
    xml_imports: dict[str, ET.Element]

    def generate_xml(self) -> ET.Element:
        root = ET.Element("macros")
        for name, value in self.tokens.items():
            sub_element = ET.SubElement(root, "token", {"name": name})
            sub_element.text = value

        for name, element in self.xml_imports.items():
            sub_element = ET.SubElement(root, "xml", {"name": name})
            sub_element.append(element)

        return root

    def write_xml(self, path: str):
        root = self.generate_xml()
        tree = ET.ElementTree(root)

        tree.write(path, pretty_print=True)

    def get_real_token_name(self, name: str):
        transformed_name = _transform_name_to_token_name(name)
        if transformed_name not in self.tokens:
            raise AttributeError("Token attribute not found")

        return transformed_name

    # TODO add docs that say it works like this
    def __getattr__(self, key: str) -> Union[str, ET.Element]:
        # tokens are stored in transformed format
        transformed_key = _transform_name_to_token_name(key)
        if transformed_key in self.tokens:
            return self.tokens[transformed_key]

        if key in self.xml_imports:
            return self.xml_imports[key]

        if key in self.__dict__.keys():
            return self.__dict__[key]
