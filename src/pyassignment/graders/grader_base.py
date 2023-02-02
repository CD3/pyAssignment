from ..utils import Namespace, collection
import pickle


class GraderBase(object):
    """
    A base class for writing automated grader scripts.

    This class stores a Namespace instance that can be used to store dynamic data in the grading script's text fields.
    """

    def __init__(self):
        self._namespace = Namespace()

    @property
    def NS(self):
        return self._namespace
