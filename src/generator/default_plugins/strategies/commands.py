from typing import Any
import xml.etree.ElementTree as ET
from generator.pluggability.strategy import Strategy, StrategyStage
import generator.common.commands.command_utils as cmd
class CommandsStrategy(Strategy):
    STAGE = StrategyStage.COMMAND

    def __init__(self, args: Any):
        super().__init__(args, self.STAGE)

    def apply_strategy(self, xml_output: ET.ElementTree) -> ET.ElementTree:
        tool_name = f"{self.args.tool_name}\n"
        inputs_body = xml_output.getroot().findall(".//inputs/*")
        results = [tool_name]
        results += self.extract_command(inputs_body)

        if not self.args.dont_redirect_output:
            results.append("1> stdout.txt 2>stderr.txt\n")

        command = "".join(results)

        command_elem = xml_output.getroot().find(".//command")
        command_elem.text = f"<![CDATA[{command}]]"

        return xml_output

    def extract_command(self, body, section_name: str = ""):
        result = []
        for element in body:
            if element.tag == "section":
                new_section_name = f"{section_name}." if section_name else ""
                new_section_name += element.attrib['name']

                result += self.extract_command(list(element),
                                               new_section_name)
            elif element.tag == "repeat":
                result.append(cmd.transform_repeat(element, section_name, 0))
            elif element.tag == "param":
                result.append(cmd.transform_basic_param(element, section_name, 0))

        return result


