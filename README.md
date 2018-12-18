# `pyAssignment`

A python module for authoring homework assignments and assessments.

# Description

This is a rewrite of the [`pyHomework`](https://github.com/CD3/pyHomework) module, which was created to help
write homework assignments for physics classes. The rewrite is currently in progress.

## Features

- Build assignments and compute solutions in pure Python.
    - Output assignment to LaTeX and build a PDF.
    - Output assignment to a Blackboard quiz.
    - Create problem set / Blackboard quiz pair. I.e. a Blackboard quiz that asks questions about
      a problem set distributed as PDF.
- [`pyErrorProp'](https://github.com/CD3/pyErrorProp) integration. Tolerances for numerical solutions
  can be automatically calculated using error propagation.

## Installing

To install `pyAssignment`, code this repository and use `pip` to install.

```bash
$ git clone https://github.com/CD3/pyAssignment
$ cd pyAssignment
$ pip install .
```


`pyAssignment` depends on the following modules available on PyPi, which you will need to install with `pip`.

- pytest
- markdown-to-json
- numpy
- Pint
- PyLaTeX
- pyparsing
- PyYAML


In addition to these, you will need to install `macro_expander`

```bash
$ pip install git+https://github.com/CD3/macro_expander
```

Optionally, if you want to do error propagation (which is very useful), you will need to install `pyErrorProp`

```bash
$ pip install git+https://github.com/CD3/pyErrorProp
```

You will also need a LaTeX installation, such as texlive, with `pdflatex` to use the LaTeX writer.

## Examples

My primary use case for `pyAssignment` is writing a Physics homework set. I want to create a PDF that contains
problems that the students must work, and then I want to create a Blackboard quiz for the students to complete
that asks questions about the problem set. The Blackboard quiz will typically contain some multiple choice questions
and several numerical answer questions, where the students must compute a numerical value for one of the problems
in the problem set and enter their answer into the quiz.

The basic procedure for create this type of assignment is to

1. Create an object of the `Assignment` class.
1. Add questions to the assignment with the `add_question()` method of the assignment object.
1. Add parts to a question with the `add_part()` method of the question object.
1. Add quiz questions for a question or part with the `add_question()` method of the question object.
1. Add an answer to the quiz question with the `add_answer()` method of the quiz question object.

Here is a basic working example

```python
import os,sys
from pyAssignment.Assignment import Assignment
import pyAssignment.Assignment.Answers as Answer
from pyAssignment.Actions import BuildProblemSetAndBlackboardQuiz
import pint

units = pint.UnitRegistry()
Q_ = units.Quantity

ass = Assignment()
ass.meta.title = r'Simple Assignment'

with ass.add_question() as q:
  q.text = r'''Calculate the weight of a 20 kg mass.'''

  with q.add_question() as qq:
    qq.text = r'''What is the mass?'''
    with qq.add_answer(Answer.Numerical) as a:
      a.quantity = (Q_(20,'kg')*Q_(9.8,'m/s^2')).to('N')


basename = os.path.basename(__file__).replace(".py","")
BuildProblemSetAndBlackboardQuiz(ass,basename)

```

The `BuildProblemSetAndBlackboardQuiz` function is an "action". It takes an assignment object and creates a PDF containing
the assignment questions, and any parts that the questions might have. Questions contained in each question or part
are extracted and written to a text file that is suitable for uploading directly into a Blackboard quiz.
Both files are written to a sub-directory named `_<BASENAME>`, where
`<BASENAME>` is the basename of the assignment file. For example, if the
assignment file is named `BasicAssignment.py`, then the PDF and Blackboard quiz
file will be named `_BasicAssignment/BasicAssignment.pdf` and
`_BasicAssignment/BasicAssignment-quiz.txt`, respectivly.


[Here](./doc/examples/_BasicAssignment/BasicAssignment.pdf) is the PDF that gets generated.

[Here](./doc/examples/_BasicAssignment/BasicAssignment-quiz.txt) is the Blackboard quiz file that gets generated.

A couple of things to note about the Blackboard quiz:

1. `pyAssignment` automatically determines what problem number each quiz question corresponds to and inserts a statement
   "For problem #X: " at the beginning of each question. This was actually the original motivation for creating `pyHomework`.
   I wanted a way to write quizzes for homework assignments that could be automatically graded and did not require me to
   restate a bunch of information from the problem set. In order to do this, each quiz question needed to reference a specific
   problem number. Doing this manually can be error-prone, as you can imagine...
1. `pyAssignment` automatically detects the units for a numerical answer and inserts a statement "Give your answer in X." at
   the end of each question text. Blackboard only accepts numerical values, its not possible to specify the units in your answer,
   so the quiz question must indicate to the student what units their answer is to be expressed in. Otherwise, students
   will say "Well, I computed the answer in Y. I think its the same thing as X, can you please check this?".
1. `pyAssignment` automatically computes a tolerance for the numerical answer. If no estimate of error
   is given (i.e. you don't specify uncertainties in your input values), then `pyAssignment` will use 1%. It is also
   possible to have the tolerance directly computed using error propagation (using the [`pyErrorProp'](https://github.com/CD3/pyErrorProp) module). However, `pyAssignment`
   will always use at least a 1% tolerance, even if the actual uncertainty is compted to be less. This lets the students
   safely round their answer to three significant figures when they enter it into Blackboard.
