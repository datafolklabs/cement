from setuptools import setup, find_packages
import sys, os

# Note to distro packagers: This application requires Cement API 
# version 0.7-0.8:20100210

setup(name='cementtest',
    version='0.8.9',
    description='Cement External Application for Testing',
    classifiers=[], 
    keywords='',
    author='BJ Dierkes',
    author_email='wdierkes@5dollarwhitebox.org',
    url='http://builtoncement.org',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ConfigObj",
        "Genshi",
        "cement >=0.8.9, <0.9",
        ],
    setup_requires=[
        ],
    test_suite='nose.collector',
    entry_points="""
    [console_scripts]
    cementtest = cementtest.core.appmain:main
    """,
    namespace_packages=[
        'cementtest', 
        'cementtest.lib', 
        'cementtest.bootstrap',
        'cementtest.controllers',
        'cementtest.model',
        'cementtest.helpers',
        'cementtest.templates',
        ],
    )
