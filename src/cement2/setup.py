
from setuptools import setup, find_packages
import sys, os

VERSION = '1.9.9'

LONG = """
Cement2 is an advanced CLI Application Framework for Python. This package 
provides the core framework required to run an application built on top of 
Cement.  Note that this is only part of 'cement' as a whole.  The entire
source is available from:

    http://builtoncement.org/cement/1.9/download/
    

The Cement CLI Application Framework is Open Source and is distributed under 
The BSD "three-clause" License.  


MORE INFORMATION:

All documentation is available from the official website:

    http://builtoncement.org
    
    
GETTING STARTED:

Stable versions can be installed via the cheeze shop:
::
    $ easy_install cement2


Development versions can be checked out of Git:
::
    $ git clone git://github.com/derks/cement.git
    
    $ git checkout --track -b portland origin/portland
    
    $ cd cement/src/cement2/
    
    $ python setup.py install


For development, and actually building applications on Cement, please see the
cement2.devtools package.

"""


setup(name='cement2',
    version=VERSION,
    description="CLI Application Framework for Python",
    long_description=LONG,
    classifiers=[], 
    keywords='cli framework',
    author='BJ Dierkes',
    author_email='wdierkes@5dollarwhitebox.org',
    url='http://builtoncement.org',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        ### Required to build documentation
        # "Sphinx >= 1.0",
        ### Required for testing
        # "nose",
        # "coverage",
        ],
    setup_requires=[
        ],
    entry_points="""
    """,
    namespace_packages=[
        'cement2',
        'cement2.ext',
        'cement2.lib',
        ],
    )
