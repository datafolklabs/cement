
from setuptools import setup, find_packages
import sys, os

VERSION = '2.0.2'

LONG = """
Cement is an advanced CLI Application Framework for Python.  Its goal is to 
introduce a standard, and feature-full platform for both simple and complex 
command line applications as well as support rapid development needs without 
sacrificing quality.

More Information:

 * DOCS: http://builtoncement.org/2.0/
 * CODE: http://github.com/cement/
 * PYPI: http://pypi.python.org/pypi/cement/
 * SITE: http://builtoncement.org/
 * T-CI: http://travis-ci.org/cement/cement

"""


setup(name='cement',
    version=VERSION,
    description="CLI Application Framework for Python",
    long_description=LONG,
    classifiers=[], 
    keywords='cli framework',
    author='BJ Dierkes',
    author_email='derks@bjdierkes.com',
    url='http://builtoncement.org',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        ### Required to build documentation
        # "Sphinx >= 1.0",
        ### Required for testing
        # "nose",
        # "coverage",
        ],
    setup_requires=[
        ],
    entry_points="""
    """,
    namespace_packages=[
        'cement',
        'cement.ext',
        ],
    )
