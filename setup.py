from setuptools import setup, find_packages
import sys, os

version = '0.4.4'

LONG = """
Cement is a CLI Application Framework for Python. It promotes code re-use by
way of plugins and helper libraries that can be maintained internally, or
shared with the community.

At a minimum, Cement easily sets up the following:

 * Configuration file parsing [using ConfigObj]
 * Command line arguments and option parsing [using OptParse]
 * Logging [using Logger]
 * Plugin support [partially using setuptools]
 * Basic "hook" support


These pieces are important for a fully functional command line application.
Normally to accomplish what's listed above would require dozens of lines of
work before you even begin coding your application. With Cement, the above is
configured with more or less a single command (via paste).

Cement is most generally used as a starting point from which to begin
developing a command line type application. That said, applications using
cement can also share plugins with either cement or other applications using
cement.

GETTING STARTED:

Stable versions of Cement can be installed via the cheeze shop:
::
    $ easy_install cement


Development versions of Cement can be checked out of Git:
::
    $ git clone git://github.com/derks/cement.git

    $ cd cement

    $ python setup.py install


Additionally, Cement applications, plugins, and helpers can be created via
PasteScript. Once Cement is installed, the following command will create a
command line application built on top of the Cement Framework:
::
    $ paster cement-app 


The following command will create an external plugin for your application:
::
    $ paster cement-plugin  


Have a helper library you want to make plugable?
::
    $ paster cement-helper
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
    license='Python Software Foundation (PSF)',
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
        "ConfigObj",
        "PasteScript >= 1.7",
        ],
    # FIX ME: This installs, but requiring CementABI == 0.4.20091211 doesn't
    # work.    
    #provides=[
    #    "CementABI (0.4.20091211)",
    #    ],
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
