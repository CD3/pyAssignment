import contextlib
import inspect
import textwrap
import uuid

from ..utils import Namespace, SFFormatter, collection, set_state_context


class Element(object):
    """A base class for common functionality used by elements of an assignment."""

    def __init__(self):
        self._uuid = uuid.uuid4()

        # a namespace to store arbitrary data
        self._namespace = Namespace()

        # a namespace to store meta data
        self._metadata = Namespace()
        # a dict to store config data
        self._metadata.config = dict()

        # a string formatter that just works
        self._formatter = SFFormatter()

        # ability to turn on/off linting
        self._lint_flag = True
        self.disable_linter = set_state_context(self, {"_lint_flag": False})

        # a list of tags that the user can add to the element
        self._tags = collection()

    def _lint(self, text):
        if not self._lint_flag:
            return text

        return textwrap.dedent(text)

    @property
    def NS(self):
        return self._namespace

    @property
    def meta(self):
        return self._metadata

    # we want to intercept access to attributes so
    # that we can support a special syntax for tags.
    #
    # q.tags = "tag 1"
    #
    # should clear any current tags and create a collection
    # with one element that is "tag 1".
    #
    # q.tags += "tag 2"
    #
    # should add "tag 2" to the list of tags.
    #
    # q.tags = ["tag 3", "tag 4"]
    #
    # should clear all tags and add "tag 3" and "tag 4"

    def __setattr__(self, name, value):
        if name == "tags":
            if isinstance(value, list):
                self._tags = value
            else:
                self._tags = collection([value])
        else:
            super().__setattr__(name, value)

    @property
    def tags(self):
        return self._tags
