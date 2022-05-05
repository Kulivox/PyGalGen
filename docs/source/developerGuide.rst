Developer guide
===============
The program was implemented knowing that not every situation can be solved with a one-size-fits-all solution.
Thus, it was built to be as pluggable as possible, providing developers with the option to extend the basic
functionality depending on their specific needs by creating custom plugins.
The main functionality of the program is contained within the Default plugin.

Plugin options
--------------
Each plugin can define custom command-line arguments. It is recommended for these to be in their specific argument group.
The program also defines arguments outside of its default plugin.
Program arguments mainly define debug options and paths needed for plugin discovery.

Data setup
----------
Plugins are also able to define DataSetup class. Methods in this can class initialise macros file initial wrapper XML.
Example of data setup class:

.. code-block:: python

    class DefaultDataSetup(DataSetup):
    """
    Defines data setup of the default plugin. During data setup,
    macros are created and default xml is initialized
    """
    def __init__(self, args: Any, assets: str):
        super().__init__(args)
        self.assets_path = assets

    def initialize_xml_tree(self, xml_tree: ET.ElementTree) -> ET.ElementTree:
        return ET.parse(os.path.join(self.assets_path, "template.xml"))

    def initialize_macros(self, macros_factory: MacrosFactory) -> MacrosFactory:
        macros_factory.add_token("tool_version",
                                           self.args.tool_version)
        for name, version in parse_argument_comma_sep_list(self.args.requirements):
            macros_factory.add_requirement(name, version)

        return macros_factory

Strategies
----------
The last and the most important part of the plugin are the plugin strategies. Strategies define wrapper creation steps performed
in the order specified by their stage and order parameters. The creation of the wrapper file is divided into eight consecutive
stages; HEADER defines the overall structure of the wrapper and possibly imports macros, PARAMS, OUTPUTS, COMMAND, TESTS, HELP,
CITATIONS and POST_PROCESSING adds elements that don’t fit into any of the previous actions or require data created in the previous stages.
Plugins can define multiple strategies for each stage, and the order of their execution depends on their order parameters.

Example strategy: 

.. code-block:: python

    class DefaultOutputs(Strategy):
    """
    This is a very basic Output strategy, that generates outputs for
    stdout and stderr redirects
    """
    def __init__(self, args: Any, macros: Macros):
        super().__init__(args, macros, StrategyStage.OUTPUTS)

    def apply_strategy(self, xml_output: ET.ElementTree) -> Any:
        if self.args.dont_redirect_output:
            return xml_output
        outputs = xml_output.find(".//outputs")
        create_element(outputs, "data", {"name": "stdout",
                                           "label": "STD out output",
                                           "format": "txt"})
        create_element(outputs, "data", {"name": "stderr",
                                         "label": "STD err output",
                                         "format": "txt"})

        return xml_output


Plugin configuration and discovery
----------
If the user provides a path to the directory containing custom plugins, they will be loaded by the program and used during the wrapper generation process.
The path is set by the command-line argument ‘--plugins path’. The plugin discovery python module traverses this directory,
looking for YAML files containing the plugin configuration metadata.
This configuration file contains the plugin's name, a list of requirements,
a path from the configuration file to the python file containing the Plugin class, execution order and a path to the plugin's assets.

Example configuration file:

.. code-block:: yaml

    plugin:
        name: Default Plugin
        # order of plugin is by default 0, this definition is here is just for clarity
        order: 0
        requirements:
            - lxml
        path: default.py
        assets: assets

