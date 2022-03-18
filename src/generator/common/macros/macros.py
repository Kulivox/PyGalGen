import lxml.etree as ET
from dataclasses import dataclass
from typing import Union

class MacrosFactory:
    def __init__(self):

        self.tokens = {}
        self.imports = {}
        self.requirements: {}

    def load_from_file(self, path: str):
        pass

    def add_token(self, name: str, value: str) -> str:
        token_name = f"@{name}@"
        self.tokens[name] = value
        return token_name

    def add_xml_import(self, name: str, value: ET.Element):
        self.imports[name] = value

    def add_requirement(self, name: str, version: str, type_: str = "package"):
        node =\
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

    def generate_xml(self):
        root = ET.Element("macros")
        for name, value in self.tokens.items():
            sub_element = ET.SubElement(root, "token", {"name": name})
            sub_element.text = value

        for name, element in self.xml_imports.items():
            sub_element = ET.SubElement(root, "xml", {"name": name})
            sub_element.append(element)

    # TODO add docs that say it works like this
    def __getattr__(self, key) -> Union[str, ET.Element]:
        if key in self.tokens:
            return self.tokens[key]

        if key in self.xml_imports:
            return self.xml_imports[key]

        if key in self.__dict__.keys():
            return self.__dict__[key]
