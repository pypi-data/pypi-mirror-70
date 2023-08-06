Lattice Explorer
================

This is an application to interactively visualize MADX lattices by tweaking corresponding lattice parameters
and observing the effect on lattice functions such as Beta functions or the resulting orbit.


Installation
------------

The application can be installed from the Python Package Index (PyPI):

.. code-block:: text

   pip install lattice-explorer


Usage
-----

The application can be started by invoking the installed package from the command line:

.. code-block:: text

   python -m lattice_explorer <path-to-madx-file>

It requires a single argument which is a file path to the MADX file containing the lattice definition.

The application then spawns two windows, one containing the lattice plots and general control elements and
the other containing specific control elements for the lattice parameters (e.g. kicker and quadrupole strength).
Changing a lattice parameter in the controls window, automatically updates the plots in the other window.

The plot window contains options for toggling usage of `BETA0` command, or activating aperture or envelope
elements in the plot orbit canvas.

The option "Freeze" copies the current plots in either the Twiss or the Orbit canvas and diplays them as
dashed lines. When lattice parameters are changed now, only the continuous lines change, and the dashed lines
remain to indicate the previous lattice functions which helps to compare two settings.


Customization
~~~~~~~~~~~~~

The application can be customized by providing various parameters, an overview of which can be obtained via

.. code-block:: text

   python -m lattice_explorer --help

These parameters can be provided as optional arguments like the following:

.. code-block:: text

   python -m lattice_explorer <path-to-madx-file> --canvas-figsize-inches 9.6 4.8


Example Screenshots
~~~~~~~~~~~~~~~~~~~

The Plots Window:

.. image:: https://gitlab.com/Dominik1123/lattice-explorer/-/raw/master/screenshot_plot_window.png?inline=false

The Controls Window:

.. image:: https://gitlab.com/Dominik1123/lattice-explorer/-/raw/master/screenshot_controls_window.png?inline=false
