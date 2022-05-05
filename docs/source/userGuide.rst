User guide
========
To use PyGalGen, you need two things:

- The tools source code
- Source code has to use argparse module to parse arguments

An example command for wrapper generation

.. code-block:: bash

    pygalgen --path tool.py --tool-name my_tool --galaxy-profile 16.01 --requirements tool:1.0 --descr "This is an example tool"

All of the programs and main plugins arguments are available at :doc:`arguments`

Recommended workflow
---------------------

In default configuration, PyGalGen is not a standalone tool. It is able to generate inputs, help and command element,
along with simple elements like description and citations. Parts of these elements might be generated incorrectly, and
some user input is still required. The recommended steps for wrapper development using PyGalGen are:

- Use PyGalGen to generate initial wrapper
- Use VSCode, along with `Galaxy plugin <https://marketplace.visualstudio.com/items?itemName=davelopez.galaxy-tools>`_ to finish the files.
  Output and Test sections have to be written manually.
- Verify the file with bundled PyGalGen linter, fix all parts which contain 'magic' tag
- Verify the file with `Planemo <https://planemo.readthedocs.io/en/latest/>`_
- Upload the file to toolshed using Planemo

