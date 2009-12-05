from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='Cement',
    version=version,
    description="Cement CLI Application Framework",
    long_description="""Cement CLI Application Framework""",
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
    """,
    namespace_packages=[
        'cement', 'cement.plugins', 'cement.handlers', 'cement.helpers'
        ],
    )