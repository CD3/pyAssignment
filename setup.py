#! /usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path
import version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    # long_description = f.read()
long_description= ""

print("version:",version.__version__)
setup(
    name='pyAssignment',
    version=version.__version__,
    description='A Python module for authoring and assessing homework assignments',
    long_description=long_description,  # Optional
    url='https://github.com/CD3/pyAssignment',
    author='C.D. Clark III',
    packages=find_packages(),
    scripts=["bin/assignment", "bin/assignment-new", "bin/assignment-make-quiz", "bin/assignment-preview-bb-quiz"]
)
