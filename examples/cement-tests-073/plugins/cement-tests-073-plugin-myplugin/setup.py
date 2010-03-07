from setuptools import setup, find_packages
import sys, os

# You probably want to change the name, this is a healthy default for paster
setup(name='cement-tests-073_plugin_myplugin',
    version='0.1',
    description='myplugin plugin for cement-tests-073',
    classifiers=[], 
    keywords='',
    author='',
    author_email='',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ConfigObj",
        "Genshi",
        "Cement >=0.7.3, <0.9",
        "cement-tests-073",
        ],
    setup_requires=[
        ],
    test_suite='nose.collector',
    entry_points="""
    """,
    namespace_packages=[
        'cement-tests-073.bootstrap',
        'cement-tests-073.controllers',
        'cement-tests-073.model',
        'cement-tests-073.helpers',
        'cement-tests-073.templates',
        ],
    )