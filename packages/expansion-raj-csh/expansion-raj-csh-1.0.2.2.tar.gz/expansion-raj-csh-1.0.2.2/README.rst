Expansion
=========

.. image:: https://raw.githubusercontent.com/Raj-CSH/expansion/master/examples/500x500_single_point_full.png
   :width: 500
   :alt: Full Example 1

.. image:: https://raw.githubusercontent.com/Raj-CSH/expansion/master/examples/500x500_random_single_point_full.png
   :width: 500
   :alt: Full Example 2

What started out as a simple generative art project and experiment,
built off of numpy, has now become an API, specifically pertaining to a
point(s) reproducing in an image, with changing colors, and even
environment-sensitive reproduction, with obstacles.

Quick start
~~~~~~~~~~~

Use the command ``$ pip install expansion-raj-csh`` to install. If this
fails, you might have to prefix the command with ``python3 -m`` on
MacOS/Linux, or ``python -m`` on Windows. If that fails, try changing
``pip`` to ``pip3``, or use the ``--user`` argument just before ``expansion_raj_csh``.

Docs
~~~~

Documentation can be found at the `Github Pages <https://raj-csh.github.io/expansion>`__
for this repository.

Examples
~~~~~~~~

See the `examples <https://github.com/Raj-CSH/expansion/tree/master/examples/>`__ directory
to see some examples, as well as an example script.

Prerequisites
~~~~~~~~~~~~~

It is recommended to create a virtual environment before installing, to
ensure that there are no conflicts with the system-wide python
installation, or if administrator permissions are unavailable. This can
be done with the ``$ python3 -m venv <ENVIRONMENT_NAME>`` or
``$ python -m venv <ENVIRONMENT_NAME>``\ commands, depending on the OS,
where ``<ENVIRONMENT_NAME>`` is the name of the virtual environment.
This can be activated with the
``$ source <ENVIRONMENT_NAME>/bin/activate`` command on Unix, or the
``<ENVIRONMENT_NAME>\Scripts\activate.bat`` command on Windows.

Installing from source
~~~~~~~~~~~~~~~~~~~~~~

1. Ensure that you have Python 3 installed on your system.

You can test this by running ``$ python3 --version`` on the command
line. If this fails, try running ``$ python --version`` and seeing if
you get a version number that begins with a 3, e.g. ``Python 3.8.2``.

If that fails, it most likely means that Python 3 is not installed on
your system.

To install Python 3, go to the Downloads page of the
`Python <https://www.python.org/downloads/>`__ website, and make sure
you install Python 3.

2. Check that pip is installed.

You can test this by running ``$ pip --version`` on the command line. If
this fails, you might have to prefix the command with ``python3 -m`` on
MacOS/Linux, or ``python -m`` on Windows. If that fails, try changing
``pip`` to ``pip3``.

If that fails, it most likely means that pip is not installed on your
system.

To install pip, follow the guide on the `Python Packaging Authority
(PyPA) <https://pip.pypa.io/en/stable/installing/>`__ website.

3. Clone the git repository.

This can be done via the
``git clone https://github.com/Raj-CSH/Expansion.git`` command, if git
is installed on your system. This can be checked via the
``$ git --version`` command.

If that fails, it most likely means git is not installed on your system.

To install git, follow the guide on the
`Git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`__
website.

4. Install pipenv.

Run the command `$ pip install pipenv` to install pipenv If this fails,
you might have to prefix the command with ``python3 -m`` on MacOS/Linux,
or ``python -m`` on Windows. If that fails, try changing ``pip`` to ``pip3``.

If you're still having problems, consult the official
`Python Packaging Authority (PyPA) <https://pip.pypa.io/en/stable/installing/>`__ website.

5. Install dependencies.

Move into the directory of the cloned git repository via the `$ cd Expansion` command.
Install the dependencies via the `$ pipenv install` command. If this fails,
you might have to prefix the command with ``python3 -m`` on MacOS/Linux,
or ``python -m`` on Windows.

6. Activate the virtual environment.

Activate the virtual environment via the `$ pipenv shell` command. If this fails,
you might have to prefix the command with ``python3 -m`` on MacOS/Linux,
or ``python -m`` on Windows. To deactivate the virtual environment once you're done,
run the `$ exit` command.


7. Update setuptools.

Run the command ``$ pip install --upgrade setuptools`` to update setuptools.

7. Build via setuptools.

In the same directory as ``setup.py``, run the
``$ python3 setup.py sdist bdist_wheel`` or the
``$ python setup.py sdist bdist_wheel`` commands, depending on your OS.
This will generate a 'dist' folder, containing the '.whl' file that can
be installed via pip.

8. Install the wheel.

Navigate into the dist folder via the command ``$ cd dist``. Then run
``$ pip install expansion_raj_csh-<VERSION_NUMBER>-py3-none-any.whl``,
where ``<VERSION_NUMBER>`` is the version of the expansion package. This
can be checked by looking at the version number in the filename of the
wheel.

Author
------

-  **Rajarshi Mandal** - `Raj-CSH <https://github.com/Raj-CSH>`__

License
-------

This project is licensed under the MIT License - see the
`LICENSE <https://raw.githubusercontent.com/Raj-CSH/expansion/master/LICENSE>`__ file for details.

Acknowledgments
---------------

-  Inspired by the
   `r/generative <https://www.reddit.com/r/generative/>`__ subreddit.

.. |Full Example| image:: https://raw.githubusercontent.com/Raj-CSH/expansion/master/examples/500x500_single_point_full.png
.. |Full Example 2| image:: https://raw.githubusercontent.com/Raj-CSH/expansion/master/examples/500x500_random_single_point_full.png
