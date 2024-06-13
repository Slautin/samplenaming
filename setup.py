#!/usr/bin/env python

import os
from setuptools import setup, find_packages
#module_dir = os.path.dirname(os.path.abspath(__file__))
##with open('README.rst') as f:
##    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name = 'samplenaming',
    packages = find_packages(exclude=('tests', 'docs')),
    include_package_data = True,
    version = '0.0.0',
    install_requires = ['anaconda>=3.0', 'monty>=0.7.2',
                        'qrcode', 'numpy>=1.0',
                        'scipy>=0.14.0', 'pandas>=1.0'],
##  extras_require = {'doc': ['codecov>=2.0', 'sphinx>=1.3.1']},
    package_data={
        "samplenaming.periodictable": ["*.json"],
    },
##    entry_points={
##        'console_scripts': ['seakmc = seakmc.script.seakmc:main']
##        },
##    license = license,
    description = 'Sample Naming for MERSEC at University of Tennessee, Knoxville',
    author = 'Tao Liang',
    author_email = 'xhtliang120@gmail.com',
    url = 'https://github.com/TaoLiang120/samplenaming',
)
