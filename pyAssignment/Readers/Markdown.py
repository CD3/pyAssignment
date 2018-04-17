from .ReaderBase import *
from .HTML import *
import mistletoe
import yaml
import pyparsing

class Markdown(ReaderBase):
  '''A (very) limited Markdown parser. Currently
     just supports parsing multiple choice questions.'''

  def __init__(self,fh=None):
    super().__init__(fh)

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
      config = yaml.load(res[0][0].strip("-"))

    ass = HTML().load(io.StringIO(mistletoe.markdown(io.StringIO(text))))
    if config is not None:
      ass.meta.__dict__.update( config )

    return ass


    

