from setuptools import setup, find_packages
import sys, os

setup(name='helloworld',
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
        "configobj",
        # remove if not using genshi templating
        "genshi",
        "cement >=0.8.9, <0.9",
        ],
    setup_requires=[
        # uncomment for nose testing
        # "nose",
        ],
    test_suite='nose.collector',
    entry_points="""
    [console_scripts]
    helloworld = helloworld.core.appmain:main
    """,
    namespace_packages=[
        'helloworld', 
        'helloworld.lib', 
        'helloworld.bootstrap',
        'helloworld.controllers',
        'helloworld.model',
        'helloworld.helpers',
        'helloworld.templates',
        ],
    )
