# PyGalGen
Toolkit used for generation and validation of Galaxy tool
definition files of python programs

## Installation
The tool can be installed by pip using this command:
```
pip install pygalgen
```

## Restrictions
PyGalGen is restricted to python programs because of the way it extracts the necessary information. It is further restricted to programs that use the argparse built-in python module and initialise a single argument parser in one location.
