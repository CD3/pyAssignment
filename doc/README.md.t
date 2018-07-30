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
\file{./examples/BasicAssignment.py}
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
1. `pyAssignment` automatically detects the units for a numerical answer and inserts a statement "Give your answer in X" at
   the end of each question text. Blackboard only accepts numerical values, its not possible to specify the units in your answer,
   so the quiz question must indicate to the student what units their answer is to be expressed in. Otherwise, students
   will say "well, I computed the answer in X. I think its the same thing as Y, can you please check this?".
1. `pyAssignment` automatically computes a tolerance for the numerical answer. If no estimate of error
   is given (i.e. you don't specify uncertainties in your input values), then `pyAssignment` will use 1%. It is also
   possible to have the tolerance directly computed using error propagation. However, `pyAssignment`
   will always use at least a 1% tolerance, even if the actual uncertainty is compted to be less. This lets the students
   safely round their answer to three significant figures when they enter it into Blackboard.
