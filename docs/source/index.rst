Pogger documentation
====================

Setup
-----

Installation
............

To install pogger using the python package index, run,

.. code:: bash

   <enter-virtual-environment-by-method-of-choice>
   pip install pogger


Building
........

To build `pogger`, from the repository, one can use poetry, which can be
pip-installed,

.. code:: bash

   git clone <repository-url> pogger-repo
   cd pogger-repo
   <enter-virtual-environment-by-method-of-choice>
   pip install poetry


One can then build the module using poetry,

.. code:: bash

   poetry build


and the (pip-installable) python wheel files should be in the `dist` directory,

.. code:: bash

   pip install dist/<wheel-file>


Archive paths
.............

By default, `pogger` will save all archive files to the directory
`~/pogger_archives`, where `~` is the user's home directory.
This path can be changed by using a configuration file.
Pogger will look for said configuration file under the path,
`~/.config/pogger/pogger.conf`.
The config file should have the following format,

.. code:: ini

   [path]
   archive= <path-to-archive-directory>


with the default config file's format being,

.. code:: ini

   [path]
   archive= ~/pogger_archives


API
---

.. automodule:: pogger
   :members:
   :undoc-members:
