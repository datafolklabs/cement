
import sys
from setuptools import setup, find_packages
from cement.utils import version

VERSION = version.get_version()

LONG = """
Cement is an advanced CLI Application Framework for Python.  Its goal is to
introduce a standard, and feature-full platform for both simple and complex
command line applications as well as support rapid development needs without
sacrificing quality.

For more information please visit the official site at:

    * http://builtoncement.com/

"""

DEPS = [
    ### Required to build documentation
    # "Sphinx >= 1.0",
    ### Required for testing
    # "nose",
    # "coverage",
    ]

# Python < 2.7/3.2 require argparse
if (sys.version_info[0] < 3 and sys.version_info < (2, 7)) or \
   (sys.version_info[0] >= 3 and sys.version_info < (3, 2)):
    DEPS.append('argparse')

setup(name='cement',
    version=VERSION,
    description="CLI Application Framework for Python",
    long_description=LONG,
    classifiers=[],
    keywords='cli framework',
    author='Data Folk Labs, LLC',
    author_email='team@datafolklabs.com',
    url='http://builtoncement.org',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=DEPS,
    setup_requires=[],
    entry_points="""
    """,
    namespace_packages=[],
    )
