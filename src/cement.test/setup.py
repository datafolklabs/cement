from setuptools import setup, find_packages
import sys, os

VERSION = '0.8.13'

LONG = """
The Cement Test application was created to facilitate proper testing of the
Cement CLI Application Framework.  Most of the features in Cement rely on
a loaded application to be access them, making testing a bit more 
complex than simply running nose on the cement module.  

The Cement Test application is simply a generic/useless application created
via the cement.devtools paster template, with a few added lines of code to
reach more of the framework and assist in testing coverage.  The primary
use of cement-test is for the nose tests in ./tests.

The Cement Test application is Open Source and is distributed under 
The MIT License.  
"""

setup(name='cement-test',
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
