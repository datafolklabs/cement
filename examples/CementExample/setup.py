from setuptools import setup, find_packages
import sys, os

version = '0.1beta'

setup(name='cement_example',
    version=version,
    description="Cement Example",
    long_description="""Cement Example""",
    classifiers=[], 
    keywords='',
    author='BJ Dierkes',
    author_email='wdierkes@5dollarwhitebox.org',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        ],
    entry_points="""
    [console_scripts]
    cement-example = cement_example.core:main
    """,
    namespace_packages=['cement_example', 'cement_example.plugins'],
    )