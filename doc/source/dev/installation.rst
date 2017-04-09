Installation
============

It is recommended to work out of a
`VirtualENV <http://pypi.python.org/pypi/virtualenv>`_
during development of your application, which is reference throughout this
documentation.  VirtualENV is easily installed on most platforms either
via PIP or by your OS distributions packaging system (Yum, Apt, Brew, etc).


Installation
------------

*Installing Stable Versions from PyPI:*

.. code-block:: text

    $ pip install cement


*Installing Development Versions from Git:*

.. code-block:: text

    $ pip install -e git+git://github.com/datafolklabs/cement.git#egg=cement


Running Tests
-------------

Docker Compose
^^^^^^^^^^^^^^

.. code-block:: text

    ### build the development image
    $ docker-compose build

    ### start all required services for optional extensions
    $ docker-compose up

    ### get a bash shell for testing from a working environment
    $ docker-compose run cement
    
    ### execute tests
    root@cement:/usr/src/app# make test


Traditional Setup (Deprecated)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run tests, you will need to ensure any dependent services are running
(for example Memcached), and then do the following from the root of the
source:

.. code-block:: text

    ### start services
    $ memcached &
    $ redis-server &

    ### install all optional/development dependencies
    $ pip install -r requirements-dev.txt

    ### run tests
    $ make test


Building Documentation
----------------------

To build this documentation, do the following from the root of the source:

.. code-block:: text

    $ make doc
