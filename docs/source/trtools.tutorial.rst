TRTools tutorial
=================
PyGalGen is really useful tool for creating TRTools wrappers, but some manual input is still required, even with TRTools plugin.
This page provides a list of useful sources, guides and a recommended workflow for creating and publishing TRTools wrappers.

Restrictions
-------------
The following guide assumes the developer uses Linux based OS, as Galaxy requires Unix based OS to run.

Useful sources
----------------
 - `Documentation and guides for Planemo <https://planemo.readthedocs.io/>`_ 
 - `Galaxy plugin for VSCode <https://marketplace.visualstudio.com/items?itemName=davelopez.galaxy-tools>`_ 
 - `Documentation of tool xml <https://docs.galaxyproject.org/en/latest/dev/schema.html>`_

Recommended workflow
---------------------
#. Install VSCode and install Galaxy plugin into it
#. Create and activate Python virtual enviroment
#. Install PyGalgen and Planemo
#. Clone repository containing TRTools
#. Generate most of the wrapper, along with the macros file using PyGalGen. Example command:

   .. code-block:: bash

       pygalgen
        --path TRTools\trtools\compareSTR\compareSTR.py
        --tool-name compareSTR
        --descr "CompareSTR"
        --requirements trtools:4.1.0
        --tool-version 4.1.0
        --verbose

   Usage of TRTools plugin is recommended. This plugin can generate citations and adds handy cheetah functions used in command elements to macros
#. Open the file in VSCode, add output and tests.
#. Verify the wrapper with bundled linter. Example command:

   .. code-block:: bash

       pygallint --path compareSTR.xml

   If anything is found, remove the problems.

#. Test the file using Planemo
#. Perform the previous steps on the rest of the source files you want to wrapped
#. Publish the results to the ToolShed

General tips
-------------
- Read the documentation on how to create outputs and tests. The parts about discover_datasets are the most important, because it's the only way to capture
  TRTools results. Use of basic 'data' elements is not possible, Galaxy needs to be able to choose the whole name of the output, which is something TRTools doesn't allow.
- Tests that check complete equality of PDF and VCF files are not reliable, PDF files can differ slightly, so there is no way to compare them correctly.
  VCF files contain information about the command that was used to create them, this command is different every time the test is run, so there is no way to create one static
  file that is used for testing
- PyGalGen generates inputs for all of the possible arguments, even for some that might not be that useful in galaxy UI, such as the version command. Check the command and input
  elements before publishing to the ToolShed
- Be careful when you define the format of 'data' input, as Galaxy might sometimes silently convert the input into the target format, which might break some things. For example, 
  if you set format of argument --vcf1 of compareSTR to 'vcf' and not to 'vcf_bgzip', the Galaxy will silently convert all of the input files that can be converted to basic VCF file.
  It will extract zipped vcfs and use the extracted value, which will cause compareSTR to crash.


CompareSTR tips
---------------
- CompareSTR inputs need a some pre-processing that is facilitated by functions in macros added by the TRToolls plugin. They need to be indexed, and the indices have to be 
  present in the working directory of the galaxy job executing TRTools wrapper. The following lines have to be present at the top of the command sections

  .. code-block:: python

        @INDEX_VCFS@
        #set $old_names = [$str($required_arguments.vcf1), $str($required_arguments.vcf2)]
        #set $new_names = $get_new_vcf_names($old_names)
        $index_vcfs($old_names, $new_names)

MergeSTR tips
----------------
- MergeSTR requires even more pre-processing and some change to the inputs. The --vcfs argument expects a list of comma separated path names, which is not Galaxy friendly.
  This argument needs to be replaced in the Inputs section, for example to something like this:

  .. code-block:: xml

        <repeat name="vcfs" title="VCF files to merge">
                <param argument="--vcf" type="data" format="vcf_bgzip" label="VCF file" help="VCF file to analyze"/>
        </repeat>
  
  The command has a lot of custom parts, for example the file names have to be extracted from the repeat and indexed:

  .. code-block:: python

    #set $inputs = [str(vcf['vcf']) for vcf in $required_arguments.vcfs]
    #set $temp_inputs = $get_new_vcf_names($inputs)
    #set $indexed_inputs_comma_separated = ",".join($temp_inputs)
    $index_vcfs($inputs, $temp_inputs)

  Afterwards, the extracted names can be used:

  .. code-block:: python

      #if $required_arguments.vcfs:
        --vcfs $indexed_inputs_comma_separated
      #end if
