import pathlib
from argparse import ArgumentParser
from pyAssignment.Assignment import Assignment
import pyAssignment.Writers as Writers
import pyAssignment.Assignment.Answers as Answer

parser = ArgumentParser(description="A small program for creating Blackboard quizzes from a set of images.")

parser.add_argument("images",
                    action="store",
                    nargs="*",
                    help="Image files to insert into quiz." )

parser.add_argument("-n", "--number-of-choices",
                    action="store",
                    default=4,
                    help="An option with argument",)

parser.add_argument("-c", "--choices",
                    action="store",
                    default="abcdefghijklmnopqrstuvwxyz",
                    help="An option with argument",)

parser.add_argument("-o", "--output-filename",
                    action="store",
                    default="blackboard-quiz-from-images.txt",
                    help="Name of file to write quiz to",)

args = parser.parse_args()



ass = Assignment()

for image in args.images:
  with ass.add_question() as q:
    with q.add_figure() as f:
      f.filename = image

    with q.add_answer(Answer.MultipleChoice) as a:
      for i in range(args.number_of_choices):
        a.incorrect += args.choices[i]

with open(args.output_filename,'w') as fh:
  writer = Writers.BlackboardQuiz(fh)
  writer.figure_text = ""
  writer.dump(ass)
