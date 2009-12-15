from setuptools import setup, find_packages
import sys, os

version = '0.4'

LONG = """
Cement is a basic Python CLI Application Framework.  Almost every command
line type application has a number of basic pieces that have to exist before
any real code and logic gets written.  At a minimum, Cement easily sets up
the following: Configuration file parsing, Command line arguments and option 
parsing, Logging, and Plugin support.
    
These four pieces are the most important for a fully functional command
line application.  Normally to accomplish what's listed above would require 
dozens of lines of non-reusable code for every application before you even 
begin coding.  With Cement, the above is configured with more or less a 
single line of code.

Cement is most generally used as a starting point from which to begin 
developing a command line type application.  That said, applications using
cement can also share plugins with either cement or other applications
using cement.
"""


setup(name='cement',
    version=version,
    description="Python CLI Application Framework",
    long_description=LONG,
    classifiers=[], 
    keywords='cli framework',
    author='BJ Dierkes',
    author_email='wdierkes@5dollarwhitebox.org',
    url='http://github.com/derks/cement',
    license='GNU GPLv3',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ConfigObj",
        # Only required if you want to use paster
        "PasteScript", 
        "tempita",
        ],
    setup_requires=[
        "PasteScript >= 1.7",
        "ConfigObj"
        ],
    # FIX ME: This installs, but requiring CementABI == 0.4.20091211 doesn't
    # work.    
    provides=[
        "CementABI (0.4.20091211)",
        ],
    entry_points="""
        [paste.global_paster_command]
        cement-app = cement.paste.commands:CementAppCommand
        cement-plugin = cement.paste.commands:CementPluginCommand
        cement-helper = cement.paste.commands:CementHelperCommand
        [paste.paster_create_template]
        cementapp = cement.paste.template:CementAppTemplate
        cementplugin = cement.paste.template:CementPluginTemplate
        cementhelper = cement.paste.template:CementHelperTemplate
    """,
    namespace_packages=[
        'cement', 'cement.plugins', 'cement.helpers'
        ],
    )
