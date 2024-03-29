import pytest

import io,os,shutil,copy

import utils

from pyassignment.assignment import Assignment
import pyassignment.actions as Actions
import pyassignment.assignment.answers as Answer
import pyassignment.writers as Writers
from pyassignment.filters.predicates import has_tag

import pint
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

@pytest.mark.skipif( "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", reason="Not running latex on Travis CI" )
def test_problem_set_builder(tmpdir):
  with utils.TempDir(tmpdir):
    ass = Assignment()
    with ass.add_question() as q:
      q.text += "Question 1"
      with q.add_question() as qq:
        qq.text += "What is the answer to Q1?"
        with qq.add_answer(Answer.Numerical) as a:
          a.quantity = 1.23

    with ass.add_question() as q:
      q.text += "Question 2"
      with q.add_part() as p:
        p.text += "Question 2, Part 1"
        with p.add_question() as qq:
          qq.text += "What is the answer to Q2P1?"
          with qq.add_answer(Answer.Numerical) as a:
            a.quantity = 2.34

    if os.path.exists("_test"): shutil.rmtree("_test")
    os.mkdir("_test")

    Actions.BuildProblemSetAndBlackboardQuiz(ass,"test")
    shutil.rmtree("_test")

    Actions.BuildProblemSetAndBlackboardQuiz(ass,"test",remove=True)


    assert os.path.isdir("_test")
    assert os.path.isfile("_test/test.tex")
    assert os.path.isfile("_test/test.pdf")
    assert os.path.isfile("_test/test.aux")
    assert os.path.isfile("_test/test-quiz.txt")





