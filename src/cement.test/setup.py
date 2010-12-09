from setuptools import setup, find_packages
import sys, os

VERSION = '0.8.14'

LONG = """
Cement is an advanced CLI Application Framework for Python. The 'test' 
package provides an external application built on top of Cement, with 
additional nose tests to provide unit testing of the framework.  To fully 
test the framework, a running application is required to cover all bits of the
code.  The 'cement.test' application is simply an application created using
the paster utility (cement.devtools) with a bit of added code for testing.
It is only meant to be used in development, for testing.  Note that this is 
only part of 'cement' as a whole.  The entire source is available from:

    http://builtoncement.org/cement/0.8/download/
    

The Cement CLI Application Framework is Open Source and is distributed under 
The MIT License.  


MORE INFORMATION:

All documentation is available from the official website:

    http://builtoncement.org
    

GETTING STARTED:
    
Development versions can be checked out of Git:
::
    $ git clone git://github.com/derks/cement.git
    
    $ cd cement/src/cement.test/
    
    $ python setup.py install
    
    $ nosetests --verbosity 3
    
"""

setup(name='cement.test',
    version=VERSION,
    description='Comprehensive Testing of the Cement CLI Application Framework',
    long_description=LONG,
    classifiers=[], 
    keywords='cement',
    author='BJ Dierkes',
    author_email='wdierkes@5dollarwhitebox.org',
    url='http://builtoncement.org',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ConfigObj",
        "Genshi",
        "cement >=0.8.9, <0.9",
        "nose",
        "jsonpickle",
        ],
    setup_requires=[
        ],
    test_suite='nose.collector',
    entry_points="""
    [console_scripts]
    cement-test = cement_test.core.appmain:main
    """,
    namespace_packages=[
        'cement_test', 
        'cement_test.lib', 
        'cement_test.bootstrap',
        'cement_test.controllers',
        'cement_test.model',
        'cement_test.helpers',
        'cement_test.templates',
        ],
    )
