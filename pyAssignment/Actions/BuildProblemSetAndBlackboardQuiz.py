
from ..Writers.Latex import *
from ..Writers.BlackboardQuiz import *
from ..Filters import QuizExtractor
from ..Utils import LatexAux
import os,shutil,subprocess

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
    prefix = ""
    if qq.meta.has("parent_uuid"):
      uuid = str(qq.meta.parent_uuid)
      if uuid in aux.labels:
        label = aux.labels[uuid]['label']
      else:
        raise RuntimeError("Quiz question needs to reference a problem set question (uuid=%s), but could not find label in .aux file (%s)."%(uuid,basename+".aux"))
      prefix = template.format(LABEL=label)
    else:
      print("WARNING: A quiz question with no parent was found. This means that no reference to the problem set will be added.")

    qq.text = prefix + qq.text

  blackboard_filename = basename+'-quiz.txt'
  with open(blackboard_filename, 'w') as f:
    blackboard_writer = BlackboardQuiz(f)
    blackboard_writer.dump(quiz)



  os.chdir(current_dir)

