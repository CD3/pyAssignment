from .WriterBase import *
from ..Assignment.Answer import *

class BlackboardQuiz(WriterBase):
  def __init__(self,fh=None):
    super().__init__(fh)
    self._default_relative_numerical_uncertainty = 0.01
    self._minimum_relative_numerical_uncertainty = 0.01

  @property
  def default_relative_numerical_uncertainty(self):
    return _default_relative_numerical_uncertainty

  @property
  def minimum_relative_numerical_uncertainty(self):
    return _minimum_relative_numerical_uncertainty

  @default_relative_numerical_uncertainty.setter
  def default_relative_numerical_uncertainty(self,val):
    try:
      val = val.to("")
    except:
      pass
    _default_relative_numerical_uncertainty = val

  @minimum_relative_numerical_uncertainty.setter
  def minimum_relative_numerical_uncertainty(self,val):
    try:
      val = val.to("")
    except:
      pass

    _minimum_relative_numerical_uncertainty = val


  def dump(self, ass, fh=None):
    fh = super().get_fh(fh)

    self._dump_questions(ass._questions, fh)

  def _dump_questions(self,qs,fh,level=0):
    for q in qs:
      self._dump_question(q,fh,level)

  def _dump_question(self,q,fh,level=0):
    t = self._get_type(q)

    toks = list()
    toks.append(t)
    toks.append(q.formatted_text)

    a = q._answer

    if t == "MC" or t == "MA":
      correct_choices = list(a.correct_formatted_choices)
      for choice in a.all_formatted_choices:
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

      toks.append("{:.2e}".format(val))

      unc = None
      try: # a pyErrorProp uncertain quantity
        unc = q.uncertainty.to( q.nominal.units ).magnitude
      except:
        pass


      if unc is None and self._default_relative_numerical_uncertainty:
        unc = val*self._default_relative_numerical_uncertainty

      if self._minimum_relative_numerical_uncertainty and unc != None and val*self._minimum_relative_numerical_uncertainty > unc:
        unc = val*self._minimum_relative_numerical_uncertainty

      toks.append("{:.2e}".format(unc))

    if t == "FIB":
      answers = a.formatted_text.split(';')
      for answer in answers:
        toks.append(answer)


    fh.write("\t".join(toks)+"\n")
      
       

      
  def _get_type(self,q):
    if q._answer is None:
      raise RuntimeError( "Question does not contain an answers." + q.text )

    a = q._answer

    if isinstance(a,Numerical):
      return "NUM"

    if isinstance(a,MultipleChoice):
      if len(list(a.correct_formatted_choices)) < 1:
        raise RuntimeError( "Multiple choice answer to question does not have a correct answer." + q.text )
      if len(list(a.correct_formatted_choices)) == 1:
        return "MC"
      return "MA"

    if isinstance(a,Essay):
      return "ESS"

    if isinstance(a,Text):
      if a.formatted_text == "":
        raise RuntimeError( "Fill in the blank question does not have an answer." + q.text )
      return "FIB"

    raise RuntimeError( "Answer type was not recognized." + str(type(a)) )

