from ..writers.latex import *
from ..utils import ColorCodes
import os,shutil,subprocess,re,sys

def BuildPDFAssignment(ass,basename,remove=False):
  current_dir = os.getcwd()
  assignment_dir = "_"+basename

  if os.path.exists(assignment_dir) and remove:
    shutil.rmtree(assignment_dir)
  if not os.path.exists(assignment_dir):
    os.mkdir(assignment_dir)

  os.chdir(assignment_dir)

  # Write problem set
  latex_filename = basename+'.tex'
  with open(latex_filename, 'w') as f:
    latex_writer = Latex(f)
    latex_writer.dump(ass)

  # run latex in the background in case it hangs
  # we need to run it twice for cross-references
  latex_cmd = "pdflatex -interaction=nonstopmode {}".format(latex_filename)
  for i in range(2):
    if shutil.which("pdflatex"):
      latex_proc = subprocess.Popen( latex_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else: raise RuntimeError("Could not find 'pdflatex' command. Please install it, or add the directory containing it to your PATH")

    try:
      # wait for latex to finish, but time out if it is taking too long
      if latex_proc.wait(10):
        print(ColorCodes.WARNING, file=sys.stderr)
        print(latex_proc.stdout.read().decode('utf-8'), file=sys.stderr)
        print(ColorCodes.ENDC, file=sys.stderr)
        raise RuntimeError("There was a problem running pdflatex")
    except subprocess.TimeoutExpired as e:
      print(ColorCodes.FAIL, file=sys.stderr)
      print("LaTeX command is taking too long to return.", file=sys.stderr)
      print("This probably means that it hung on a syntax error.", file=sys.stderr)
      print("Check the log file '%s'."%(basename+".log"), file=sys.stderr)
      print(ColorCodes.ENDC, file=sys.stderr)
      return



  os.chdir(current_dir)

