Installation
============

It is recommended to work out of a `VirtualENV <http://pypi.python.org/pypi/virtualenv>`_ 
during development of your application, which is reference throughout this 
documentation.  VirtualENV is easily installed on most platforms either with 
via pip or by your OS distributions packaging system (yum, apt, brew, etc).

Installation
------------

*Installing Stable Versions from PyPI:*

.. code-block:: text

    $ pip install cement
    

*Installing Development Versions from Git:*

.. code-block:: text

    $ pip install -e git+git://github.com/cement/cement.git#egg=cement    


Running Tests
-------------

To run tests, do the following from the root of the source:

.. code-block:: text
    
    $ pip install nose coverage
    
    $ python setup.py nosetests
    
    
Building Documentation
----------------------

To build this documentation, do the following from the root of the source:

.. code-block:: text

    $ pip install sphinx
    
    $ python setup.py build_sphinx
