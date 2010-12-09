from setuptools import setup, find_packages
import sys, os

VERSION = '0.8.14'

LONG = """
Cement is an advanced CLI Application Framework for Python. The 'core' 
package provides the core framework required to run an application built on
top of Cement.

The Cement CLI Application Framework is Open Source and is distributed under 
The MIT License.  


MORE INFORMATION:

All documentation is available from the official website:

    http://builtoncement.org
    
    
GETTING STARTED:

Stable versions can be installed via the cheeze shop:
::
    $ easy_install cement.core


Development versions can be checked out of Git:
::
    $ git clone git://github.com/derks/cement.git
    
    $ cd cement/src/cement.core/
    
    $ python setup.py install


For development, and actually building applications on Cement, please see the
cement.devtools package.

"""


setup(name='cement.core',
    version=VERSION,
    description="CLI Application Framework for Python",
    long_description=LONG,
    classifiers=[], 
    keywords='cli framework',
    author='BJ Dierkes',
    author_email='wdierkes@5dollarwhitebox.org',
    url='http://builtoncement.org',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ConfigObj",
        "jsonpickle",
        "Genshi",
        # Required for documentation
        #"Sphinx >= 1.0",
        #"Pygments",
        ],
    setup_requires=[
        ],
    entry_points="""
    """,
    namespace_packages=[],
    )
