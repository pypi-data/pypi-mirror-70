# Lattice Explorer
# Copyright (C) 2020  Dominik Vilsmeier

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from pathlib import Path
import re

from setuptools import setup, find_packages


def get_version():
    text = Path('lattice_explorer/__init__.py').read_text()
    return re.findall("^__version__ = '(.+)'$", text, flags=re.M)[0]


setup(
    name='lattice-explorer',
    version=get_version(),
    description=(
        'Interactively explore MADX lattices by tweaking lattice parameters '
        'and observing the effect on lattice functions.'
    ),
    long_description=Path('README.rst').read_text(),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    keywords=['MADX', 'lattice', 'visualization', 'interactive'],
    url='https://gitlab.com/Dominik1123/lattice-explorer',
    author='Dominik Vilsmeier',
    author_email='d.vilsmeier@gsi.de',
    license='GPL-3.0',
    packages=find_packages(),
    install_requires=[
        'arguable',
        'cpymad',
        'matplotlib',
        'numpy',
        'PyQt5',
    ],
    python_requires='>=3.7',
)
