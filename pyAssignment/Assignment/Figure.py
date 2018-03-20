import contextlib,textwrap,inspect

from ..Utils import Namespace, SFFormatter, set_state_context

class Figure(object):
  '''Represents a figure.'''

  def __init__(self):
    self._filename = ""
    self._caption = ""
    self._namespace = Namespace()

    self._lint_flag = True
    self.disable_linter = set_state_context(self, {'_lint_flag':False})

    self._formatter = SFFormatter()

  def _lint(self,text):
    if not self._lint_flag:
      return text

    return textwrap.dedent(text)


  @property
  def NS(self):
    return self._namespace


  @property
  def caption(self):
    return self._caption

  @caption.setter
  def caption(self,val):
    self._caption = self._lint(val)

  @property
  def formatted_caption(self):
    return self._formatter.fmt( self._caption, **self.NS.__dict__ )

  @property
  def filename(self):
    return self._filename

  @filename.setter
  def filename(self,val):
    # todo: if file does not exist, search
    # for a candidate
    self._filename = self._lint(val)

