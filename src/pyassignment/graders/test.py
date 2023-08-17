import contextlib
import os
import inspect
from ..utils import Namespace, SFFormatter, working_directory, collection


class Test(object):
    """
    A test class represents a single test that will be ran during grading.

    A test has a name, description, working directory, result, and a set of other
    tests to run if the current tests fails or passes.

    This class should be derived to implement specific test types. The deriving
    class only needs to implements the '__run__()' method, which will be called
    by this class.

    Properties:

      NS : A namespace that will be used when formatting strings.
      meta : A dict for string meta-data in the tests. Different tests can use this data to change behavior.
      name : A name for the test.
      description : A description of what the test does.
      directory : A directory that the test should be ran in.
      result : The result of the test. True means PASS. False means FAIL.
      score : The score for the test, i.e. the nubmer of points to add for this test.
      weight : The weight that should be given to the test score when total the score for multiple tests.
    """

    def __init__(self):
        self._name = None
        self._desc = None
        self._dir = None
        self._result = None

        self._on_fail_tests = collection()
        self._on_pass_tests = collection()

        self._formatter = SFFormatter()

        self._namespace = Namespace()
        self._meta = Namespace()

    def _update(self, other):
        self.NS.__dict__.update(other.NS.__dict__)
        self.meta.__dict__.update(other.meta.__dict__)
        self.working_directory = other._dir

    @property
    def NS(self):
        return self._namespace

    def fmt(self,text: str):
        return self._formatter.fmt(text, **self.NS.__dict__, **os.environ)

    @property
    def meta(self):
        return self._meta

    @property
    def name(self):
        if self._name is None:
            return ""
        else:
            return self.fmt(self._name)

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def description(self):
        if self._desc is None:
            return ""
        else:
            return self.fmt(self._desc)

    @description.setter
    def description(self, val):
        self._desc = val

    @property
    def working_directory(self):
        if self._dir is None:
            return None
        else:
            return self.fmt(self._dir)

    @working_directory.setter
    def working_directory(self, val):
        self._dir = val

    def run(self):
        # run this test
        with working_directory(self.working_directory):
            self._result = self.__run__()

        # if test passed, run the "on pass" tests
        if self._result:
            for t in self._on_pass_tests:
                t.run()
        else:
            for t in self._on_fail_tests:
                t.run()

        # return the result of this test
        return self._result

    @contextlib.contextmanager
    def add_on_fail_test(self, test=None):
        if test is None:
            test = self.__class__
        if inspect.isclass(test):
            t = test()
        else:
            t = test

        t._update(self)

        yield t
        if t._name is None:
            t.name = "Failure Follow-up Test " + str(len(self._on_fail_tests))

        self._on_fail_tests.append(t)

    @contextlib.contextmanager
    def add_on_pass_test(self, test=None):
        if test is None:
            test = self.__class__
        if inspect.isclass(test):
            t = test()
        else:
            t = test

        t._update(self)

        yield t
        if t._name is None:
            t.name = "Success Follow-up Test " + str(len(self._on_pass_tests))
        self._on_pass_tests.append(t)

    @property
    def result(self):
        return self._result

    @property
    def score(self):
        # return None if the test hasn't been run
        if self._result is None:
            return None

        # if test succeeded, return 100%
        if self._result:
            return 1
        else:
            # if test failed,
            # add up the score from the _on_fail_tests (if any)
            # and return
            score = 0
            total_weight = sum([t.weight for t in self._on_fail_tests])
            for t in self._on_fail_tests:
                score += t.weight * t.score / total_weight
            score *= self.fail_tests_weight
            return score

    @property
    def weight(self):
        try:
            return self._weight
        except:
            return 1

    @weight.setter
    def weight(self, val):
        self._weight = val

    @property
    def fail_tests_weight(self):
        try:
            return self._fail_tests_weight
        except:
            return 0.5

    @fail_tests_weight.setter
    def fail_tests_weight(self, val):
        self._fail_tests_weight = val

    def summarize(self, prefix=""):
        s = ""
        if self.result is None:
            s += prefix + "DID NOT RUN\n"
            return s

        if self.result:
            s += prefix + "PASS"

        if not self.result:
            s += prefix + "FAIL"

        s += "  "
        s += self.name
        s += ": "
        s += self.description
        s += "\n"

        if hasattr(self, "__summarize__"):
            s += self.__summarize__(prefix)

        if len(self._on_fail_tests):
            s += prefix + "  Additional Tests\n"
            for ft in self._on_fail_tests:
                s += ft.summarize(prefix="  " + prefix)

        if len(self._on_pass_tests):
            s += prefix + "  Additional Tests\n"
            for pt in self._on_pass_tests:
                s += pt.summarize(prefix="  " + prefix)

        return s

    def test_output(self, prefix=""):

        s = ""
        if self.result is None:
            s += prefix + "DID NOT RUN\n"
            return s

        if self.result:
            s += prefix + "PASS"

        if not self.result:
            s += prefix + "FAIL"

        s += "  "
        s += self.name
        s += ": "
        s += self.description
        s += "\n"

        s += "stdout:\n"
        if hasattr(self, "_o"):
            s += self._o
        if hasattr(self, "_output"):
            s += self._o

        s += "stderr:\n"
        if hasattr(self, "_e"):
            s += self._e
        if hasattr(self, "_error"):
            s += self._e

        if len(self._on_fail_tests):
            s += prefix + "  Additional Tests\n"
            for ft in self._on_fail_tests:
                s += ft.test_output(prefix="  " + prefix)

        if len(self._on_pass_tests):
            s += prefix + "  Additional Tests\n"
            for pt in self._on_pass_tests:
                s += pt.test_output(prefix="  " + prefix)

        return s
