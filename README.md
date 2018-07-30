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
- (`pyErrorProp')[https://github.com/CD3/pyErrorProp] integration. Tolerances for numerical solutions
  can be automatically calculated using error propagation.

## Examples

My primary use case for `pyAssignment` is writing a Physics homework set. I want to create a PDF that contains
problem that the students must work, and then I want to create a Blackboard quiz that the students must complete
that asks questions about the problem set. The Blackboard quiz will typically contain some multiple choice questions
and several numerical answer questions, where the students must compute a numerical value for one of the problems
in the problem set and enter their answer into the quiz.
