from ..utils import Namespace, SFFormatter, set_state_context

class WriterBase(object):
  def __init__(self,fh=None):
    self.fh = fh
    self.config = Namespace()
    self.config.add_none_of_the_above_choice = True
    self.config.none_of_the_above_text = "None of the above."

  def MC_Answer_get_all_choices(self,a):
    all_choices = list(a.all_formatted_choices)
    # we want to allow the answer to override the add_none_of_the_above_choice
    # configuration option
    add_none_of_the_above_choice = self.config.add_none_of_the_above_choice
    if a.meta.has('add_none_of_the_above_choice'):
      add_none_of_the_above_choice = a.meta.add_none_of_the_above_choice

    none_of_the_above_text = self.config.none_of_the_above_text
    if a.meta.has('none_of_the_above_text'):
      none_of_the_above_text = a.meta.none_of_the_above_text

    if add_none_of_the_above_choice:
      all_choices += [none_of_the_above_text]

    return all_choices

  def MC_Answer_get_correct_choices(self,a):
    correct_choices = list(a.correct_formatted_choices)

    add_none_of_the_above_choice = self.config.add_none_of_the_above_choice
    if a.meta.has('add_none_of_the_above_choice'):
      add_none_of_the_above_choice = a.meta.add_none_of_the_above_choice

    none_of_the_above_text = self.config.none_of_the_above_text
    if a.meta.has('none_of_the_above_text'):
      none_of_the_above_text = a.meta.none_of_the_above_text

    if len(correct_choices) == 0 and add_none_of_the_above_choice:
      correct_choices += [none_of_the_above_text]

    return correct_choices



  def get_fh(self,fh=None):
    if fh is None:
      fh = self.fh
    if fh is None:
      raise(RuntimeError("No filehandle available."))
    return fh
