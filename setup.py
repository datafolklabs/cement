
import sys
from setuptools import setup, find_packages
from cement.utils import version

VERSION = version.get_version()

f = open('README.md', 'r')
LONG = f.read()
f.close()

setup(name='cement',
    version=VERSION,
    description='CLI Application Framework for Python',
    long_description=LONG,
    long_description_content_type='text/markdown',
    classifiers=[],
    keywords='cli framework',
    author='Data Folk Labs, LLC',
    author_email='derks@datafolklabs.com',
    url='http://builtoncement.org',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    entry_points="""
        [console_scripts]
        cement = cement.cli.main:main
    """,
)
