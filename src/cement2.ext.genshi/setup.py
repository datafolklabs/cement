
# NOTE: jsonpickle does not currently support Python3

from setuptools import setup, find_packages
import sys, os

VERSION = '1.9.9'

LONG = """
Cement is an advanced CLI Application Framework for Python. This package 
provides the Genshi framework extension allowing applications to use
the Genshi output handler and Text Templating Language.

The Cement CLI Application Framework is Open Source and is distributed under 
The BSD "three-clause" License.  


MORE INFORMATION:

All documentation is available from the official website:

    http://builtoncement.org
    
"""

setup(name='cement2.ext.genshi',
    version=VERSION,
    description="Genshi Framework Extension for Cement",
    long_description=LONG,
    classifiers=[], 
    keywords='cli framework cement',
    author='BJ Dierkes',
    author_email='wdierkes@5dollarwhitebox.org',
    url='http://builtoncement.org',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "genshi", 
        "cement2 >=1.9"
        ],
    setup_requires=[
        ],
    entry_points="""
    """,
    namespace_packages=[
        'cement2',
        'cement2.ext',
        'cement2.lib'
        ],
    )
