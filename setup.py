#! /usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    # long_description = f.read()
long_description= ""

setup(
    name='pyAssignment',
    version="1.1.2",
    description='A Python module for authoring and assessing homework assignments',
    long_description=long_description,  # Optional
    url='https://github.com/CD3/pyAssignment',
    author='C.D. Clark III',
    packages=find_packages(),
    install_requires=['markdown-to-json','numpy','pyparsing','Pint','PyLaTeX','PyYAML','macro-expander>=0.2','pyErrorProp'],

    scripts=["bin/assignment", "bin/assignment-new", "bin/assignment-make-quiz", "bin/assignment-preview-bb-quiz", "bin/create-blackboard-quiz-from-images.py"]
    # entry_points='''
    # [console_scripts]
    # create-blackboard-quiz-from-images=pyAssignment.scripts.command_line_programs:create_blackboard_quiz_from_images
)
