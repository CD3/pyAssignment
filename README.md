# `pyAssignment`

A python module for authoring homework assignments and assessments.

# Description

This is a rewrite of the [`pyHomework`](https://github.com/CD3/pyHomework) module, which was created to help
write homework assignments for physics classes. The rewrite is currently in progress.

## Features

- Build assignments and compute solutions in pure Python.
    - Write assignment to LaTeX.
    - Write assignment to Blackboard Quiz.
- Command-line grader.
    - Write tests that are ran in the shell.
- [`pyErrorProp'](https://github.com/CD3/pyErrorProp) integration. Tolerances for numerical solutions
  can be automatically calculated using error propagation.

## Examples

My primary use case for `pyAssignment` is writing a Physics homework set. I want to create a PDF that contains
problem that the students must work, and then I want to create a Blackboard quiz that the students must complete
that asks questions about the problem set. The Blackboard quiz will typically contain some multiple choice questions
and several numerical answer questions, where the students must compute a numerical value for one of the problems
in the problem set and enter their answer into the quiz.

The basic procedure for create this type of assignment is to

1. Create an object of the `Assignment` class.
1. Add questions to the assignment with the `add_question()` method of the assignment object.
1. Add parts to the question with the `add_part()` method of the question object.
1. Add quiz questions for a question  or part with the `add_question()` method of the question object.
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

[Here](.doc/examples/_BasicAssignment/BasicAssignment.pdf) is the PDF that gets generated.

[Here](.doc/examples/_BasicAssignment/BasicAssignment-quiz.txt) is the Blackboard quiz file that gets generated.

Both files are written to a sub-directory named `_<BASENAME>`, where
`<BASENAME>` is the basename of the assignment file. For example, if the
assignment file is named `BasicAssignment.py`, then the PDF and Blackboard quiz
file will be named `_BasicAssignment/BasicAssignment.pdf` and
`_BasicAssignment/BasicAssignment-quiz.txt`, respectivly.

Note that `pyAssignment` automatically computes a tolerance for the numerical answer. If no estimate of error
is given (i.e. you don't specify uncertainties in your input values), then `pyAssignment` will use 1%.
