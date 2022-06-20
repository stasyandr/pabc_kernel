pabc_kernel
===========

``pabc_kernel`` is a simple example of a Jupyter kernel for PascalABC.NET. This repository
complements the documentation on wrapper kernels here:

http://jupyter-client.readthedocs.io/en/latest/wrapperkernels.html

Installation
------------
Copy folders "pabc_kernel" and "pabc_kernel.egg-info" in folder with Python packages
	(usually it's C:\Users\User\AppData\Local\Programs\Python\Python_Version\Lib\site-packages\)
	
    python -m pabc_kernel.install

Using the pabc kernel
---------------------
**Notebook**: The *New* menu in the notebook should show an option for an pabc notebook.

**Console frontends**: To use it with the console frontends, add ``--kernel pabc`` to
their command line arguments.
