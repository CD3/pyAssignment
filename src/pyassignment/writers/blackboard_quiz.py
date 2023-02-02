from .writer_base import *
from ..assignment.answers import *
from ..utils import image2html

import pyparsing
import re
import pathlib

try:
  import macro_expander
  have_macro_expander = True
except:
  have_macro_expander = False
  class DummyMacroProcessor:
    def process(self,text):
      return text
    def readCache(self,trash):
      pass
    def writeCache(self,trash):
      pass


import io
import multiprocessing

class BlackboardQuiz(WriterBase):
  def __init__(self,fh=None,use_macro_expander_cache=True):
    super().__init__(fh)
    self.config.default_relative_numerical_uncertainty = 0.01
    self.config.minimum_relative_numerical_uncertainty = 0.01
    self.macro_expander_cache_path = pathlib.Path("pyassignment-BlackboardQuiz-Writer-Cache.bin")
    if have_macro_expander:
      self.macro_processor = macro_expander.MacroProcessor(use_cache=use_macro_expander_cache)
    else:
      self.macro_processor = DummyMacroProcessor()

    if self.macro_expander_cache_path.is_file():
      self.macro_processor.readCache(str(self.macro_expander_cache_path))

    self.figure_text = "</br>Consider the figure above. "


  @property
  def default_relative_numerical_uncertainty(self):
    return self.config.default_relative_numerical_uncertainty

  @property
  def minimum_relative_numerical_uncertainty(self):
    return config.minimum_relative_numerical_uncertainty

  @default_relative_numerical_uncertainty.setter
  def default_relative_numerical_uncertainty(self,val):
    try:
      val = val.to("")
    except:
      pass
    self.config.default_relative_numerical_uncertainty = val

  @minimum_relative_numerical_uncertainty.setter
  def minimum_relative_numerical_uncertainty(self,val):
    try:
      val = val.to("")
    except:
      pass

    config.minimum_relative_numerical_uncertainty = val


  def dump(self, ass, fh=None):
    fh = super().get_fh(fh)

    buffer = io.StringIO()
    self._dump_questions(ass._questions, buffer)

    # do line formatting in parallel
    # p = multiprocessing.Pool()
    # lines = p.map(format_line, buffer.getvalue().split("\n") )
    lines = map(self._format_line, buffer.getvalue().split("\n") )

    fh.write( "\n".join(lines) )

    # save the macro_expander cache for future calls.
    self.macro_processor.writeCache(str(self.macro_expander_cache_path))

  def _format_line(self,text):
    if have_macro_expander:
      latex_math = pyparsing.QuotedString( quoteChar='$', convertWhitespaceEscapes=False )
      def latex_math_to_mathimg(s,loc,toks):
        return [ r'\mathimg[o="html",tex2im_opts="-r 100x100"]{%s}'%t for t in toks ]
      latex_math.addParseAction(latex_math_to_mathimg)
      text = latex_math.transformString(text)

      text = self.macro_processor.process(text)

      # need to clean up text.
      # should not have any new line chars
      text = text.replace("\n"," ")
      # should not have multiple spaces together
      text = re.sub(" +"," ",text)

    return text

  def _dump_questions(self,qs,fh,level=0):
    for q in qs:
      self._dump_question(q,fh,level)

  def _dump_question(self,q,fh,level=0):
    t = self._get_type(q)

    if t == "MULTIPART":
      print("Detected multi-part question. Will merge question text with text from first part.")
      q._text += "</br>"+q._parts[0]._text
      q._answer = q._parts[0]._answer
      q._parts = q._parts[1:]
      t = self._get_type(q)


    toks = list()
    toks.append(t)

    text = ""

    if level > 0:
      text += "This question is about the same scenario as the previous question.</br>"


    if len(q._figures):
      for f in q._figures:
        fmt = None
        if f.meta.has("fmt"):
          fmt = f.meta.fmt
        attrs = ""
        if f.meta.has("attributes"):
          attrs = f.meta.attributes
        text += image2html(f.filename,fmt,attrs).replace("\n"," ")+self.figure_text

    text += re.sub("[ \n]+"," ",q.formatted_text)





    toks.append(text)

    a = q._answer

    if t == "MC" or t == "MA":
      all_choices = self.MC_Answer_get_all_choices(a)
      correct_choices = self.MC_Answer_get_correct_choices(a)
      if len(correct_choices) < 1:
        raise RuntimeError( "Multiple choice answer to question does not have a correct answer: " + q.text )

      # if there is more than one correct answer
      # then this should actually be marked as a multiple answer (MA) question.
      if len(correct_choices) > 1:
        t = "MA"

      for choice in all_choices:
        toks.append(choice)
        if choice not in correct_choices:
          toks.append("incorrect")
        else:
          toks.append("correct")

    if t == "NUM":
      ans = a.quantity

      # we are using the pythonic 'try-and-ask-for-forgiveness-later' method of type inspection.

      # if the quantity has units, add a statement to the question text specifying
      # the units that the answer should be given in.
      unit_str = ""
      try: # a pint quantity
        unit_str = "{}".format(ans.units)
      except:
        pass

      try: # a pyErrorProp uncertain quantity
        unit_str = "{}".format(ans.nominal.units)
      except:
        pass

      if len(unit_str) > 0 and unit_str != "dimensionless":
        toks[1] += " Give your answer in {}.".format(unit_str)

      val = ans
      try: # a pint quantity
        val = ans.magnitude
      except:
        pass
      try: # a pyErrorProp uncertain quantity
        val = ans.nominal.magnitude
      except:
        pass

      toks.append("{:.2E}".format(val))

      unc = None
      try: # a pyErrorProp uncertain quantity
        unc = ans.uncertainty.to( ans.nominal.units ).magnitude
      except:
        pass


      unc_type = type(val)
      if unc_type is int:
        unc_type = float

      if unc is None and self.config.default_relative_numerical_uncertainty:
        unc = val*unc_type(self.config.default_relative_numerical_uncertainty)

      if self.config.minimum_relative_numerical_uncertainty and unc != None and abs(val*unc_type(self.config.minimum_relative_numerical_uncertainty)) > abs(unc):
        unc = val*unc_type(self.config.minimum_relative_numerical_uncertainty)

      unc = abs(unc)

      toks.append("{:.2E}".format(unc))

    if t == "FIB":
      if a.formatted_text == "":
        raise RuntimeError( "Fill in the blank question does not have an answer: " + q.text )
      answers = a.formatted_text.split(';')
      for answer in answers:
        toks.append(answer)


    fh.write("\t".join(toks)+"\n")

    # write question parts
    if len(q._parts) > 0:
      self._dump_questions( q._parts, fh, level+1)




  def _get_type(self,q):
    if q._answer is None:
      if len(q._parts) > 0:
        return "MULTIPART"
      raise RuntimeError( "Question does not contain an answer: " + q.text )

    a = q._answer

    if isinstance(a,Numerical):
      return "NUM"

    if isinstance(a,MultipleChoice):
      if len(a._correct) > 1:
        return "MA"
      else:
        return "MC"

    if isinstance(a,Essay):
      return "ESS"

    if isinstance(a,FileResponse):
      return "FIL"

    if isinstance(a,Text):
      return "FIB"

    raise RuntimeError( "Answer type was not recognized: " + str(type(a)) )

