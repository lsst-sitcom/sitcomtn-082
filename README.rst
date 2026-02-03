.. image:: https://img.shields.io/badge/sitcomtn--082-lsst.io-brightgreen.svg
   :target: https://sitcomtn-082.lsst.io/
.. image:: https://github.com/lsst-sitcom/sitcomtn-082/workflows/CI/badge.svg
   :target: https://github.com/lsst-sitcom/sitcomtn-082/actions/

#############################
Hard Point Breakaway Analysis
#############################

SITCOMTN-082
============

This is a technote for the description of results from Individual Hardpoint Breakaway Test. 

**Links:**

- Publication URL: https://sitcomtn-082.lsst.io/
- Alternative editions: https://sitcomtn-082.lsst.io/v
- GitHub repository: https://github.com/lsst-sitcom/sitcomtn-082
- Build system: https://github.com/lsst-sitcom/sitcomtn-082/actions/

Build this technical note
=========================

You can clone this repository and build the technote locally if your system has Python 3.11 or later:

.. code-block:: bash

   git clone https://github.com/lsst-sitcom/sitcomtn-082
   cd sitcomtn-082
   make init
   make html

Repeat the ``make html`` command to rebuild the technote after making changes.
If you need to delete any intermediate files for a clean build, run ``make clean``.

The built technote is located at ``_build/html/index.html``.

Publishing changes to the web
=============================

This technote is published to https://sitcomtn-082.lsst.io/ whenever you push changes to the ``main`` branch on GitHub.
When you push changes to a another branch, a preview of the technote is published to https://sitcomtn-082.lsst.io/v.

Editing this technical note
===========================

The main content of this technote is in ``index.rst`` (a reStructuredText file).
Metadata and configuration is in the ``technote.toml`` file.
For guidance on creating content and information about specifying metadata and configuration, see the Documenteer documentation: https://documenteer.lsst.io/technotes.

Setting up the LSST Stack
=========================

Make sure the LSST Stack is initialized before declaring the package. 
The easiest way is to add the following function to your ``.bashrc`` or equivalent shell startup file:

.. code-block:: bash

   # generic LSST Stack -- remember to setup the desired obs package!
   function setup_lsst () {
      unset PYTHONPATH
      source /sdf/group/rubin/sw/w_latest/loadLSST.bash
      setup lsst_distrib
      echo "Current weekly stack initialized:"
      eups list -s | grep lsst_distrib
      echo "Use the following to change to different tagged version: setup -t <tag> lsst_distrib"
   }

Make sure you run ``setup_lsst`` in each new terminal session before moving on to the next step.


Installing as a Python Package
==============================

The notebooks in the ``./notebooks`` folder use the code in the ``./python`` folder as a package.
You will need to install this package using EUPS. Here are the steps:

.. code-block:: bash

   # Declare the package
   eups declare lsst_sitcom_tn082 v1 -r $PATH_TO_THIS_REPO/sitcomtn-082

   # Install it
   setup lsst_sitcom_tn082

   # Test it
   python -c "import lsst.sitcom.tn082; print(lsst.sitcom.tn082.__version__)"

The last command line should print the package version. It is OK if it prints ``?``, since versioning might not be fully implemented yet.

If you are running the notebooks in Nublado, 
you will have to update the ``$HOME/notebooks/.user_setups`` file with the same lines above. 
This will ensure the package is available in your Nublado environment and 
you can perform the import in a Jupyter Notebook.
You can test your installation by running the same test command in a Jupyter Notebook cell:

.. code-block:: python

   import lsst.sitcom.tn082
   print(lsst.sitcom.tn082.__version__)
