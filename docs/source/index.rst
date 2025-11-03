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


Usage
-----

Suppose we have a python file which generates some data, or creates some plots
that we want to save.

.. code:: python

   import numpy as np
   from matplotlib import pyplot as plt

   def make_sine():
       time = np.linspace(0, 1)
       wave = np.sin(2*np.pi*10*time)

       plt.figure()
       plt.plot(time, wave)
       plt.draw()

       print("Done!")

       return time, wave

   make_sine()

   plt.show()


What we want to do is import the :class:`pogger.Pogger` class.

.. code:: python

   from pogger import Pogger


We then want to instantiate such a class for the duration of the code we want
to record.
This can be done either manually,

.. code:: python

   import numpy as np
   from matplotlib import pyplot as plt

   from pogger import Pogger

   logger = Pogger()

   def make_sine():
       time = np.linspace(0, 1)
       wave = np.sin(2*np.pi*10*time)

       plt.figure()
       plt.plot(time, wave)
       plt.draw()

       print("Done!")

       return time, wave

   make_sine()

   logger.exit()

   plt.show()


or automatically using python contexts,

.. code:: python

   import numpy as np
   from matplotlib import pyplot as plt

   from pogger import Pogger

   with logger as Pogger():
       def make_sine():
           time = np.linspace(0, 1)
           wave = np.sin(2*np.pi*10*time)

           plt.figure()
           plt.plot(time, wave)
           plt.draw()

           print("Done!")

           return time, wave

       make_sine()

   plt.show()


To make the results of a function are recorded, one can wrap it with
:meth:`pogger.Pogger.record()`.

.. code:: python

   import numpy as np
   from matplotlib import pyplot as plt

   from pogger import Pogger

   with logger as Pogger():
       @logger.record(["Time", "Waveform"])
       def make_sine():
           time = np.linspace(0, 1)
           wave = np.sin(2*np.pi*10*time)

           plt.figure()
           plt.plot(time, wave)
           plt.draw()

           print("Done!")

           return time, wave

       make_sine()

   plt.show()


Upon running the program, `pogger` will automatically create an archive of the
what happened.
This archive will be a folder/directory containing three things:

1.
    A plain text `.log` file that is a record of all console output.

2.
    An `hdf5` archive file of all values returned by any function.
    They will be saved under the names given in the first argument of the
    wrapper.
    In our example, they will be saved under "Time" and "Waveform"
    respectively.
    One can later read the archive file either using a reader like hdfview, or
    by using the :class:`pogger.Read` class.

3. 
   `.png` and `.pdf` files of all plots generated using
   :mod:`matplotlib.pyplot`.


The archive will be saved in either the directory `~/pogger_archives`, or the
one specified by the configuration file `~/.config/pogger/pogger.conf` file
(see above).
It will further be saved under the `/default` directory, and then under
directories labelled by the current year, month and day.
One can change the `/default` directory to something more meaningful (like the
name of the code/experiment being done) using the first argument in the
:class:`pogger.Pogger` constructor.

.. code:: python

   import numpy as np
   from matplotlib import pyplot as plt

   from pogger import Pogger

   with logger as Pogger("sine-example"):
       @logger.record(["Time", "Waveform"])
       def make_sine():
           time = np.linspace(0, 1)
           wave = np.sin(2*np.pi*10*time)

           plt.figure()
           plt.plot(time, wave)
           plt.draw()

           print("Done!")

           return time, wave

       make_sine()

   plt.show()


One can specify the name that the plots should be saved under by using the
`label` argument in :meth:`matplotlib.pyplot.figure`.

.. code:: python

   import numpy as np
   from matplotlib import pyplot as plt

   from pogger import Pogger

   with logger as Pogger("sine-example"):
       @logger.record(["Time", "Waveform"])
       def make_sine():
           time = np.linspace(0, 1)
           wave = np.sin(2*np.pi*10*time)

           plt.figure(label="sine_example")
           plt.plot(time, wave)
           plt.draw()

           print("Done!")

           return time, wave

       make_sine()

   plt.show()


Finally, one can choose subgroups within the hdf5 archive to save data by using
`pogger.Pogger.set_context`, and units of data by using the second argument of
`pogger.Pogger.record`.

.. code:: python

   import numpy as np
   from matplotlib import pyplot as plt

   from pogger import Pogger

   with logger as Pogger("sine-example"):
       @logger.record(["Time", "Waveform"], ["seconds", "Volts"])
       def make_sine():
           time = np.linspace(0, 1)
           wave = np.sin(2*np.pi*10*time)

           plt.figure(label="sine_example")
           plt.plot(time, wave)
           plt.draw()

           print("Done!")

           return time, wave

       logger.set_context("first_run")
       make_sine()

       logger.set_context("second_run")
       make_sine()

   plt.show()


`Pogger` supports the saving of numpy arrays, single values, and dictionaries
that contain the above.


API
---

.. automodule:: pogger
   :members:
   :undoc-members:
