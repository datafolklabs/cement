
import sys
from setuptools import setup, find_packages
from cement.utils import version

VERSION = version.get_version()

f = open('README.md', 'r')
LONG = f.read()
f.close()

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
    long_description_content_type='text/markdown',
    classifiers=[],
    keywords='cli framework',
    author='Data Folk Labs, LLC',
    author_email='team@datafolklabs.com',
    url='http://builtoncement.com',
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
