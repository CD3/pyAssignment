from .WriterBase import *
from ..Assignment.Answers import *

import pyparsing
import re

try:
  import macro_expander
  have_macro_expander = True
except:
  have_macro_expander = False


class BlackboardQuiz(WriterBase):
  def __init__(self,fh=None):
    super().__init__(fh)
    self.config.default_relative_numerical_uncertainty = 0.01
    self.config.minimum_relative_numerical_uncertainty = 0.01

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

    self._dump_questions(ass._questions, fh)

  def _format_line(self,text):
    if have_macro_expander:
      latex_math = pyparsing.QuotedString( quoteChar='$', convertWhitespaceEscapes=False )
      def latex_math_to_mathimg(s,loc,toks):
        return [ r'\mathimg[o="html"]{%s}'%t for t in toks ]
      latex_math.addParseAction(latex_math_to_mathimg)
      text = latex_math.transformString(text)

      proc = macro_expander.MacroProcessor()
      text = proc.process(text)

      # need to clean up text.
      # should not have any new line chars
      text = text.replace("\n"," ")
      text = re.sub(" +"," ",text)
      # should not have multiple spaces together

    return text

  def _dump_questions(self,qs,fh,level=0):
    for q in qs:
      self._dump_question(q,fh,level)

  def _dump_question(self,q,fh,level=0):
    t = self._get_type(q)

    toks = list()
    toks.append(t)
    toks.append(q.formatted_text)

    a = q._answer

    if t == "MC":
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
      q = a.quantity

      # we are using the pythonic 'try-and-ask-for-forgiveness-later' method of type inspection.

      # if the quantity has units, add a statement to the question text specifying
      # the units that the answer should be given in.
      unit_str = ""
      try: # a pint quantity
        unit_str = "{}".format(q.units)
      except:
        pass

      try: # a pyErrorProp uncertain quantity
        unit_str = "{}".format(q.nominal.units)
      except:
        pass

      if len(unit_str) > 0 and unit_str != "dimensionless":
        toks[1] += " Give your answer in {}.".format(unit_str)

      val = q
      try: # a pint quantity
        val = q.magnitude
      except:
        pass
      try: # a pyErrorProp uncertain quantity
        val = q.nominal.magnitude
      except:
        pass

      toks.append("{:.2E}".format(val))

      unc = None
      try: # a pyErrorProp uncertain quantity
        unc = q.uncertainty.to( q.nominal.units ).magnitude
      except:
        pass


      if unc is None and self.config.default_relative_numerical_uncertainty:
        unc = val*self.config.default_relative_numerical_uncertainty

      if self.config.minimum_relative_numerical_uncertainty and unc != None and val*self.config.minimum_relative_numerical_uncertainty > unc:
        unc = val*self.config.minimum_relative_numerical_uncertainty

      toks.append("{:.2E}".format(unc))

    if t == "FIB":
      if a.formatted_text == "":
        raise RuntimeError( "Fill in the blank question does not have an answer: " + q.text )
      answers = a.formatted_text.split(';')
      for answer in answers:
        toks.append(answer)


    fh.write(self._format_line("\t".join(toks))+"\n")
      
       

      
  def _get_type(self,q):
    if q._answer is None:
      raise RuntimeError( "Question does not contain an answer: " + q.text )

    a = q._answer

    if isinstance(a,Numerical):
      return "NUM"

    if isinstance(a,MultipleChoice):
      return "MC"

    if isinstance(a,Essay):
      return "ESS"

    if isinstance(a,Text):
      return "FIB"

    raise RuntimeError( "Answer type was not recognized: " + str(type(a)) )

