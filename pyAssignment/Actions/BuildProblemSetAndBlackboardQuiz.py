
from ..Writers.Latex import *
from ..Writers.BlackboardQuiz import *
from ..Filters import QuizExtractor
from ..Utils import LatexAux, ColorCodes
import os,shutil,subprocess,re,sys

def BuildProblemSetAndBlackboardQuiz(ass,basename,remove=False):
  current_dir = os.getcwd()
  assignment_dir = "_"+basename
  if os.path.exists(assignment_dir):
    if remove:
      shutil.rmtree(assignment_dir)
    else:
      raise RuntimeError("Assignment directory '%s' already exists. Either delete it, or pass 'remove=True' to BuildProblemSetAndBlackboardQuiz."%assignment_dir)

  os.mkdir(assignment_dir)
  os.chdir(assignment_dir)

  # Write problem set
  latex_filename = basename+'.tex'
  with open(latex_filename, 'w') as f:
    latex_writer = Latex(f)
    latex_writer.dump(ass)

  if shutil.which("latexmk"): subprocess.check_call( "latexmk -pdf", shell=True )
  else: raise RuntimeError("Could not find 'latexmk' command. Please install it, or add the directory containing it to your PATH")


  # Write quiz
  quiz = QuizExtractor().filter(ass)

  # We need/want to add a statement to reference which problem set question each
  # quiz question is about. The problem set question numbers will be written
  # to the .aux file.
  aux = LatexAux(basename+'.aux')

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

    qq.text = prefix + qq.text

  blackboard_filename = basename+'-quiz.txt'
  with open(blackboard_filename, 'w') as f:
    blackboard_writer = BlackboardQuiz(f)
    blackboard_writer.dump(quiz)

  with open(blackboard_filename,'r') as f:
    text = f.read()
    ms = [ m for m in re.finditer('\\\[a-zA-Z]+[\[{]',text) ]
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

