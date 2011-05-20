
from setuptools import setup, find_packages
import sys, os

VERSION = '1.9.1'

LONG = """
Cement is an advanced CLI Application Framework for Python. This package 
provides the Json framework extension allowing applications to use
the Json output handler.

The Cement CLI Application Framework is Open Source and is distributed under 
The MIT License.  


MORE INFORMATION:

All documentation is available from the official website:

    http://builtoncement.org
    
"""

setup(name='cement.ext.json',
    version=VERSION,
    description="Json Framework Extension for Cement",
    long_description=LONG,
    classifiers=[], 
    keywords='cli framework cement',
    author='BJ Dierkes',
    author_email='wdierkes@5dollarwhitebox.org',
    url='http://builtoncement.org',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "jsonpickle", 
        ],
    setup_requires=[
        ],
    entry_points="""
    """,
    namespace_packages=[
        'cement.ext'
        ],
    )
