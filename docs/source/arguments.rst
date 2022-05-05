.. _arguments-label:
Main program and default plugin parameters
========

usage: Command parser [-h] --path PATH --tool-name TOOL_NAME [--verbose] [--debug] [--plugins-path PLUGINS_PATH] [--dont-redirect-output] [--galaxy-profile GALAXY_PROFILE] --descr DESCR --requirements REQUIREMENTS
                      --tool-version TOOL_VERSION [--inputs INPUTS]

options:
  -h, --help            show this help message and exit

Default program parameters:
  --path PATH           Path to the source file
  --tool-name TOOL_NAME
                        Name of the package for which you are creating the tool definition file

Logging arguments:
  --verbose             Prints out info logs
  --debug               Print out debug text

Plugin discovery:
  --plugins-path PLUGINS_PATH
                        Path to directory containing plugins you want to use

Default plugin:
  --dont-redirect-output
                        If this argument is present, tool will not redirect its output to output files during execution in galaxy
  --galaxy-profile GALAXY_PROFILE
                        Version of galaxy profile
  --descr DESCR         Description of the tool
  --requirements REQUIREMENTS
                        Comma separated list of package:version pairs
  --tool-version TOOL_VERSION
                        Version of the tool
  --inputs INPUTS       Comma separated list of names and format types of program arguments that define inputs. (name:format,name:format) For example, if your program accepts path to vcf file in argument called input, enter      
                        'input:vcf'

