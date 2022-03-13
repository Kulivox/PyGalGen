import ast
import astunparse
from generator.common.source_file_parsing.parsing_commons \
    import create_module_tree
from generator.common.source_file_parsing.parser_discovery_and_init \
    import get_parser_init_and_actions
from generator.common.source_file_parsing.unknown_names_discovery \
    import initialize_variables_in_module
from generator.common.source_file_parsing.local_module_parsing import \
    handle_local_module_names
from generator.common.source_file_parsing.parsing_exceptions import \
    ArgumentParsingDiscoveryError


def obtain_and_convert_parser(path: str):
    tree = create_module_tree(path)
    try:
        actions, name, parser_names, section_names = \
            get_parser_init_and_actions(tree)

        actions, unknown_names = \
            initialize_variables_in_module(tree, parser_names,
                                           section_names, actions)

        result_module = handle_local_module_names(actions, unknown_names)
    except ArgumentParsingDiscoveryError:
        print("Parsing failed")
        return

    ast.fix_missing_locations(result_module)
    print(astunparse.unparse(result_module))
    compiled_module = compile(result_module, filename="<parser>", mode="exec")

    variables = {}
    exec(compiled_module, globals(), variables)
    print(variables[name])
    return variables[name]
