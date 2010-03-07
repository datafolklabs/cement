from setuptools import setup, find_packages
import sys, os

setup(name='cement-tests-073',
    version='0.1',
    description='',
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
        # Uncomment to use shared plugins from The Rosendale Project.
        #"Rosendale",
        ],
    setup_requires=[
        ],
    test_suite='nose.collector',
    entry_points="""
    [console_scripts]
    cementtests073 = cementtests073.core.appmain:main
    """,
    namespace_packages=[
        'cementtests073', 
        'cementtests073.bootstrap',
        'cementtests073.controllers',
        'cementtests073.model',
        'cementtests073.helpers',
        'cementtests073.templates',
        ],
    )