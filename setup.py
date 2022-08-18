
import sys
from setuptools import setup, find_packages
from cement.utils import version

VERSION = version.get_version()

f = open('README.md', 'r')
LONG = f.read()
f.close()

setup(name='cement',
    version=VERSION,
    python_requires='>=3.5',
    description='Application Framework for Python',
    long_description=LONG,
    long_description_content_type='text/markdown',
    classifiers=[],
    install_requires=[],
    keywords='cli framework',
    author='Data Folk Labs, LLC',
    author_email='derks@datafolklabs.com',
    url='https://builtoncement.com',
    project_urls={
        'Documentation': 'https://docs.builtoncement.com',
        'Source': 'https://github.com/datafolklabs/cement',
    },
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'cement': ['cement/cli/templates/generate/*']},
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    entry_points = {   
        'console_scripts' : [
            'cement = cement.cli.main:main',
        ],
    },
    extras_require = {
        'ext.alarm': [],
        'ext.argparse': [],
        'ext.colorlog': ['colorlog'],
        'ext.configparser': [],
        'ext.daemon': [],
        'ext.dummy': [],
        'ext.generate': [],
        'ext.jinja2': ['jinja2'],
        'ext.json': [],
        'ext.logging': [],
        'ext.memcached': ['pylibmc'],
        'ext.mustache': ['pystache'],
        'ext.plugin': [],
        'ext.print': [],
        'ext.redis': ['redis'],
        'ext.scrub': [],
        'ext.smtp': [],
        'ext.tabulate': ['tabulate'],
        'ext.watchdog': ['watchdog'],
        'ext.yaml': ['pyYaml'],
    }
)
