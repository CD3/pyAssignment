from .answer_base import *

class Text(AnswerBase):
  def __init__(self):
    super().__init__()
    self._text = None

    self._lint_flag = True
    self.disable_linter = set_state_context(self, {'_lint_flag':False})

  def _lint(self,text):
    if not self._lint_flag:
      return text

    return textwrap.dedent(text)

  @property
  def text(self):
    if hasattr(self._text,'__call__'):
      return self._namespace.call( self._text )
    return self._text

  @text.setter
  def text(self,val):
    if hasattr(val,'__call__'):
      self._text = val
    else:
      self._text = self._lint(val)

  @property
  def formatted_text(self):
      return self._formatter.fmt( self.text, **self.NS.__dict__ )
