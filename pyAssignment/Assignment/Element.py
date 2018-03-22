
from ..Utils import Namespace, SFFormatter, set_state_context
import contextlib,textwrap,inspect
import uuid


class Element(object):
  '''A base class for common functionality used by elements of an assignment.'''

  def __init__(self):
    self._uuid = uuid.uuid4()

    # a namespace to store arbitrary data
    self._namespace = Namespace()

    # a namespace to store meta data
    self._metadata = Namespace()

    # a string formatter that just works
    self._formatter = SFFormatter()

    # ability to turn on/off linting
    self._lint_flag = True
    self.disable_linter = set_state_context(self, {'_lint_flag':False})


  def _lint(self,text):
    if not self._lint_flag:
      return text

    return textwrap.dedent(text)



  @property
  def NS(self):
    return self._namespace

  @property
  def meta(self):
    return self._metadata
