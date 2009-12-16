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
        "ConfigObj",
        "cement == 0.4",
        ],
    setup_requires=[
        "PasteScript >= 1.7"
        ],
    test_suite='nose.collector',
    entry_points="""
    [console_scripts]
    helloworld = helloworld.appmain:main
    """,
    namespace_packages=['helloworld', 'helloworld.plugins'],
    )