from setuptools import setup, find_packages
import sys, os

# You probably want to change the name, this is a healthy default for paster
setup(name='helloworld_helpers_myhelper',
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
        "Cement >=0.5, <0.7",
        ],
    setup_requires=[
        ],
    test_suite='nose.collector',
    entry_points="""
    """,
    namespace_packages=['helloworld', 'helloworld.helpers'],
    )
