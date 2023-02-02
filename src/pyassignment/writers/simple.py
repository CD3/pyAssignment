from .writer_base import *
from ..assignment.answers import *

class Simple(WriterBase):

  def __init__(self,fh=None):
    self.fh = fh
    self.i = 0

  def dump(self, ass, fh=None):
    fh = super().get_fh(fh)

    fh.write("NAMESPACE:\n")
    self._dump_namespace(ass._namespace, fh)
    fh.write("\n\nQUESTIONS:\n")
    self._dump_questions(ass._questions, fh)

  def _dump_questions(self,qs,fh,prefix=""):
    if len(qs) > 0:
      for q in qs:
        self.i += 1
        self._dump_question(q,fh,prefix)

  def _dump_question(self,q,fh,prefix):
    fh.write( "%s%d. %s"%( prefix,self.i,q.formatted_text ) )
    fh.write("\n")

    self._dump_answer(q._answer,fh,prefix+"  ")

    i_save = self.i
    self.i = 0
    self._dump_questions(q._parts,fh,prefix+"  ")
    self.i = 0
    self._dump_questions(q._questions,fh,prefix+"  ")
    self.i = i_save

  def _dump_answer(self,a,fh,prefix):
    if a is None:
      return

    fh.write( "%sANS: "%( prefix ) )

    if( isinstance(a,Numerical) ):
      fh.write( "{}".format(a.quantity) )
    if( isinstance(a,Text) ):
      fh.write( "{}".format(a.text) )
    if( isinstance(a,MultipleChoice) ):
      correct = list(a.correct_formatted_choices)
      i = 0
      for c in a.all_formatted_choices:
        i += 1
        if i > 1:
          fh.write( "{}     ".format( prefix ) )
        fh.write( "{}".format( c) )
        if c in correct:
          fh.write(" (correct)")
        fh.write( "\n")


    fh.write("\n")

  def _dump_namespace(self,ns,fh,prefix=""):
    for k in sorted(ns.__dict__.keys()):
      fh.write("{0}{1} = {2}\n".format(prefix,k,ns.__dict__[k]))

