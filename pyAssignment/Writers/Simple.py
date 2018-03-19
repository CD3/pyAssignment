
from .WriterBase import *

class SimpleWriter(WriterBase):

  def __init__(self,fh=None):
    self.fh = fh
    self.i = 0


  def _dump_question(self,q,fh,prefix):
    fh.write( "%s%d. %s"%( prefix,self.i,q.formatted_text ) )
    fh.write("\n")

    i_save = self.i
    self.i = 0
    self._dump_questions(q._parts,fh,prefix+"  ")
    self.i = 0
    self._dump_questions(q._questions,fh,prefix+"  ")
    self.i = i_save

  def _dump_questions(self,qs,fh,prefix=""):
    if len(qs) > 0:
      for q in qs:
        self.i += 1
        self._dump_question(q,fh,prefix)

  def dump(self, ass, fh=None):
    fh = super().get_fh(fh)

    self._dump_questions(ass._questions, fh)

