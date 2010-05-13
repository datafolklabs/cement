from setuptools import setup, find_packages
import sys, os

version = '0.8.2'

LONG = """
Cement is an advanced CLI Application Framework for Python. It promotes code 
re-use by way of plugins and helper libraries that can be shared between 
any application built on Cement.  The MVC and overall framework design is 
very much inspired by the TurboGears2 web framework.  Its goal is to introduce
a standard, and feature-full platform for both simple and complex command line 
applications as well as support rapid development needs without sacrificing
quality.

At a minimum, Cement configures the following features for every application:
::
     * Multiple Configuration file parsing (default: /etc, ~/)
     * Command line argument and option parsing
     * Dual Console/File Logging Support
     * Full Internal and External (3rd Party) Plugin support
     * Basic "hook" support
     * Full MVC support for advanced application design
     * Text output rendering with Genshi templates
     * Json output rendering allows other programs to access your CLI-API
    

The above provides any level developer with a solid, and fully functional 
cli application from the very start with more or less a single command via 
the paster utility.  Cement brings an end to the 'hack it out, and [maybe] 
clean it up later' routine that we all find ourselves in under deadlines.

Any application can utilize existing plugins from The Rosendale Project, or 
from other 3rd party resources to extend functionality.  The plugin system is 
designed to allow portability of re-usable code, and it is encouraged to 
contribute any plugins back to the project to extend the functionality of 
Cement.  When creating plugins specifically for re-use within the community, 
please be sure to follow the standard naming convention 'HelloWorld Plugin for 
Cement' as an example.  The actual module name should be something like:
'myapp.plugin.helloworld'. 

The Cement CLI Application Framework is Open Source and is distributed under 
The MIT License.  


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


setup(name='Cement',
    version=version,
    description="Python CLI Application Framework",
    long_description=LONG,
    classifiers=[], 
    keywords='cli framework',
    author='BJ Dierkes',
    author_email='wdierkes@5dollarwhitebox.org',
    url='http://github.com/derks/cement',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ConfigObj",
        "jsonpickle",
        # Only required if you want to use paster
        "PasteScript", 
        "tempita",
        # Required for documentation
        "Sphinx",
        "Pygments",
        ],
    setup_requires=[
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
    namespace_packages=[],
    )
