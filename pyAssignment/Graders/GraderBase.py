from ..Utils import Namespace, collection
import pickle

class GraderBase(object):
  def __init__(self):
    self._namespace = Namespace()

  @property
  def NS(self):
    return self._namespace
