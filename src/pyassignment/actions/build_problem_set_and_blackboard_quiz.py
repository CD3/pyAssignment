
from ..writers.latex import *
from ..writers.blackboard_quiz import *
from ..filters import QuizExtractor
from ..utils import LatexAux, ColorCodes, working_directory
import os,shutil,subprocess,re,sys

def BuildProblemSetAndBlackboardQuiz(ass,basename,extra_quiz_questions=None,remove=False):
  current_dir = os.getcwd()
  assignment_dir = "_"+basename

  if os.path.exists(assignment_dir) and remove:
    shutil.rmtree(assignment_dir)
  if not os.path.exists(assignment_dir):
    os.mkdir(assignment_dir)

  with working_directory(assignment_dir):

    # Write problem set
    latex_filename = basename+'.tex'
    with open(latex_filename, 'w') as f:
      latex_writer = Latex(f)
      latex_writer.dump(ass)

    # run latex in the background
    latex_cmd = "pdflatex -interaction=nonstopmode {}".format(latex_filename)
    if shutil.which("pdflatex"):
      latex_proc = subprocess.Popen( latex_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else: raise RuntimeError("Could not find 'pdflatex' command. Please install it, or add the directory containing it to your PATH")


    # Write quiz
    quiz = QuizExtractor().filter(ass)
    if not extra_quiz_questions is None:
      for q in extra_quiz_questions._questions:
        quiz._questions.append(q)


    # We need/want to add a statement to reference which problem set question each
    # quiz question is about. The problem set question numbers will be written
    # to the .aux file.
    # NOTE: we can't read the aux file until AFTER the latex's first pass
    if latex_proc.wait(30):
      print(ColorCodes.WARNING, file=sys.stderr)
      print(latex_proc.stdout.read().decode('utf-8'), file=sys.stderr)
      print(ColorCodes.ENDC, file=sys.stderr)
      raise RuntimeError("There was a problem running pdflatex")
    aux = LatexAux(basename+'.aux')
    # now we can run latex again in the background
    latex_proc = subprocess.Popen( latex_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # replace labels in the quiz text
    template = "For problem #{LABEL}: "
    for qq in quiz._questions:
      if qq.meta.has("ancestor_uuids"):
        labels = list()
        for u in qq.meta.ancestor_uuids:
          uuid = str(u)
          if uuid in aux.labels:
            label = aux.labels[uuid]['label']
            labels.append(label.strip(".()"))
          else:
            raise RuntimeError("Quiz question needs to reference a problem set question (uuid=%s), but could not find label in .aux file (%s)."%(uuid,basename+".aux"))
        prefix = template.format(LABEL='.'.join(labels))
      elif qq.meta.has("parent_uuid"):
        uuid = str(qq.meta.parent_uuid)
        if uuid in aux.labels:
          label = aux.labels[uuid]['label']
        else:
          raise RuntimeError("Quiz question needs to reference a problem set question (uuid=%s), but could not find label in .aux file (%s)."%(uuid,basename+".aux"))
        prefix = template.format(LABEL=label)
      else:
        print("WARNING: A quiz question with no ancestors/parent was found. This means that no reference to the problem set will be added.")
        prefix = ""

      qq.text = prefix + qq.text

    # write the blackboard quiz
    blackboard_filename = basename+'-quiz.txt'
    with open(blackboard_filename, 'w') as f:
      blackboard_writer = BlackboardQuiz(f)
      blackboard_writer.dump(quiz)

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

  # wait for latex to finish (it's probably already done)
  if latex_proc.wait(30):
    print(ColorCodes.WARNING, file=sys.stderr)
    print(latex_proc.stdout.read().decode('utf-8'), file=sys.stderr)
    print(ColorCodes.ENDC, file=sys.stderr)
    raise RuntimeError("There was a problem running pdflatex")

