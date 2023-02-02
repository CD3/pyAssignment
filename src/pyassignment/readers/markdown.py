from .reader_base import *
from .json import *
import yaml
import pyparsing
import subprocess, tempfile
import sys

class Markdown(ReaderBase):
  '''A (very) limited Markdown parser. Currently
     just supports parsing multiple choice questions.'''

  def __init__(self,fh=None):
    super().__init__(fh)
    self.throw_on_missing_answers = True

  def _markdown_to_json( self, markdown_text ):
    '''Return a json representation of the markdown text.'''

    # going to use the md_to_json tool here.
    # need to write the markdown to disk, then call md_to_json on the file.
    with tempfile.NamedTemporaryFile(delete=False) as f:
      f.write(markdown_text.encode('utf-8'))

    res = subprocess.run("md_to_json {}".format(f.name),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if res.returncode:
      print("Error: there was a problem running md_to_json.")
      print("       Is 'markdown-to-json' installed?")
      print("Stdout:")
      print(res.stdout.decode('utf-8'))
      print("Stderr:")
      print(res.stderr.decode('utf-8'))
      sys.exit(1)
    else:
      return res.stdout.decode('utf-8')

  def load(self, fh=None, ass=None):
    if ass is None:
      ass = Assignment()

    fh = super().get_fh(fh)

    text = fh.read()

    # look for a pandoc-style configuration section. this
    # will be a yaml file imbedded in the text between two sets of '---'.
    res = pyparsing.originalTextFor(pyparsing.QuotedString(quoteChar='---',multiline=True)).searchString( text )
    config = None
    if len(res):
      text = text.replace(res[0][0],"")
      config = yaml.load(res[0][0].strip("-"), Loader=yaml.FullLoader)

    in_data = json.loads(self._markdown_to_json(text))

    # need to process JSON before passing to the JSON reader
    qkey = "Questions"
    for k in in_data.keys():
      if k.lower() == "questions":
        qkey = k

    out_data = dict()
    out_data['questions'] = list()
    i = 0
    N = len(in_data.get(qkey,list()))
    while i < N:
      q = dict()
      q['text'] = in_data[qkey][i]
      if i+1 < N and isinstance( in_data[qkey][i+1], list ):
        i += 1
        q['answer'] = dict()
        q['answer']['choices'] = in_data[qkey][i]
      elif self.throw_on_missing_answers:
        raise RuntimeError("A question without an answer was found. Question test '{}'".format(q['text']) )

      out_data['questions'].append(q)
      i += 1


    ass = JSON().load(io.StringIO(json.dumps(out_data)))
    if config is not None:
      ass.meta.__dict__.update( config )

    return ass



