from ..writers.blackboard_quiz import *
from ..utils import ColorCodes
import os,shutil,subprocess,re,sys

def BuildBlackboardAssignment(ass,basename,remove=False):
  current_dir = os.getcwd()
  assignment_dir = "_"+basename

  if os.path.exists(assignment_dir) and remove:
    shutil.rmtree(assignment_dir)
  if not os.path.exists(assignment_dir):
    os.mkdir(assignment_dir)

  os.chdir(assignment_dir)

  blackboard_filename = basename+'.txt'
  with open(blackboard_filename, 'w') as f:
    blackboard_writer = BlackboardQuiz(f)
    blackboard_writer.dump(ass)

  # read the quiz file that was just written and check
  # to see if there are any latex commands that didn't get
  # replaced.
  with open(blackboard_filename,'r') as f:
    text = f.read()
    ms = [ m for m in re.finditer(r'\\\[a-zA-Z]+[\[{]',text) ]
    if len(ms) > 0:
      print(ColorCodes.WARNING, file=sys.stderr)
      print("WARNING: it appears that the quiz text ({}) contains one ore more LaTeX macros.".format(blackboard_filename), file=sys.stderr)
      print("         This is almost certainly *NOT* what you want.", file=sys.stderr)
      print("Possible Macros:", file=sys.stderr)
      i = 0
      for m in ms:
        print(i,m.group(0),"Starting at character",m.start(0), file=sys.stderr)
        i += 1
      print(ColorCodes.ENDC, file=sys.stderr)

  os.chdir(current_dir)

