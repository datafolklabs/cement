from setuptools import setup, find_packages
import sys, os

VERSION = '0.8.17'

LONG = """
Cement is an advanced CLI Application Framework for Python. The 'devtools' 
package provides tools and libraries needed for developing applications that
are built on Cement.  Note that this is only part of 'cement' as a whole.  The 
entire source is available from:

    http://builtoncement.org/cement/0.8/download/
    

The Cement CLI Application Framework is Open Source and is distributed under 
The MIT License.  


MORE INFORMATION:

All documentation is available from the official website:

    http://builtoncement.org    
    

GETTING STARTED:

Stable versions can be installed via the cheeze shop:
::
    $ easy_install cement.devtools


Development versions can be checked out of Git:
::
    $ git clone git://github.com/derks/cement.git
    
    $ cd cement/src/cement.devtools/
    
    $ python setup.py install


With the 'devtools' package, Cement applications and plugins can be 
created via PasteScript. The following command will create a command line 
application built on top of the Cement Framework:
::
    $ paster cement-app myapp


The following command will create an external plugin for your application:
::
    $ paster cement-plugin myapp myplugin

"""


setup(name='cement.devtools',
    version=VERSION,
    description="Development Tools for the Cement CLI Application Framework",
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
        "PasteScript", 
        "tempita",
        "cement == %s" % VERSION,
        ],
    setup_requires=[
        ],
    entry_points="""
        [paste.global_paster_command]
        cement-app = cementdevtools.paste.commands:CementAppCommand
        cement-plugin = cementdevtools.paste.commands:CementPluginCommand
        [paste.paster_create_template]
        cementapp = cementdevtools.paste.template:CementAppTemplate
        cementplugin = cementdevtools.paste.template:CementPluginTemplate
    """,
    namespace_packages=[],
    )
