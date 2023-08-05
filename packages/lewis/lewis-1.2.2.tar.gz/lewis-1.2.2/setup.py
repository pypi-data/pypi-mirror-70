#!/usr/bin/env python
# -*- coding: utf-8 -*-
# *********************************************************************
# lewis - a library for creating hardware device simulators
# Copyright (C) 2016-2017 European Spallation Source ERIC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *********************************************************************

from setuptools import setup, find_packages


# as suggested on http://python-packaging.readthedocs.io/en/latest/metadata.html
def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='lewis',
    version='1.2.2',
    description='LeWIS - Let\'s Write Intricate Simulators!',
    long_description=readme(),
    url='https://github.com/DMSC-Instrument-Data/lewis',
    author='Michael Hart, Michael Wedel, Owen Arnold',
    author_email='michael.hart@stfc.ac.uk',
    license='GPL v3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='hardware simulation controls',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=['six', 'pyzmq', 'json-rpc', 'semantic_version',
                      'PyYAML', 'scanf==1.4.1'],

    extras_require={
        'epics': ['pcaspy'],
        'dev': ['flake8==3.5.0', 'mock>=1.0.1', 'sphinx>=1.4.5', 'sphinx_rtd_theme',
                'pytest>=3.6', 'pytest-cov', 'coverage', 'tox'],
    },

    entry_points={
        'console_scripts': [
            'lewis=lewis.scripts.run:run_simulation',
            'lewis-control=lewis.scripts.control:control_simulation'
        ],
    },
)
