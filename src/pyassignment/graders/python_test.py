from .test import *
import inspect


class PythonTest(Test):
    def __init__(self):
        super().__init__()
        self._func = None

    @property
    def function(self):
        return self._func

    @function.setter
    def function(self, func):
        self._func = func

    def __run__(self):
        if self._func is None:
            raise Exception("No function set for PythonTest.")
        sig = inspect.signature(self._func)
        argtypes = [sig.parameters[name].annotation for name in sig.parameters]
        if len(argtypes) == 0:
            self._result = self._func()
        elif len(argtypes) == 1:
            if argtypes[0] == self.__class__:
                self._result = self._func(self)
            elif argtypes[0] == type(self.NS):
                self._result = self._func(self.NS)
            else:
                raise Exception(
                    "Unknown function argument type for PythonTest callable."
                )
        else:
            raise Exception("Unknown function signature for PythonTest callable.")
        return self._result
