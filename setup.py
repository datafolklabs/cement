from setuptools import setup, find_packages
import sys, os

version = '0.1'

LONG = """
Cement is a basic Python CLI Application Framework.  Almost every command
line type application has a number of basic pieces that have to exist before
any real code and logic gets written.  At a minimum, Cement easily sets up
the following:

    Configuration file parsing [using ConfigObj]
    Command line arguments and option parsing [using OptParse]
    Logging [using Logger]
    Plugin support [partially using setuptools]
    

These four pieces are the most important for a fully functional command
line application.  Normally to accomplish what's listed above would require 
dozens of lines of code before you even begin coding your application.  With 
Cement, the above is configured with more or less a single line of code.

Cement is most generally used as a starting point from which to begin 
developing a command line type application.  That said, applications using
cement can also share plugins with either cement or other applications
using cement.
"""


setup(name='Cement',
    version=version,
    description="Python CLI Application Framework",
    long_description=LONG,
    classifiers=[], 
    keywords='',
    author='BJ Dierkes',
    author_email='wdierkes@5dollarwhitebox.org',
    url='http://github.com/derks/python-cement',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ConfigObj"
        ],
    entry_points="""
    """,
    namespace_packages=[
        'cement', 'cement.plugins', 'cement.handlers', 'cement.helpers'
        ],
    )