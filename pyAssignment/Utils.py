from types import SimpleNamespace
from inspect import getargspec

import pyparsing

class Namespace(SimpleNamespace):
  def has(self,attr):
    return hasattr(self,attr)

  def clear(self):
    self.__dict__.clear()

  def __len__(self):
    return len(self.__dict__)

  def call(self,func,**kwargs):
    # get list of args required by f
    rargs = getargspec(func).args
    # build args to pass to f from our __dict__ and kwargs.
    # use the value in __dict__ unless an entry exists in kwargs

    args = dict()
    missing = list()
    for a in rargs:
      if a in kwargs:
        args[a] = kwargs[a]
      elif a in self.__dict__:
        args[a] = self.__dict__[a]
      else:
        missing.append(a)

    if len(missing) > 0:
      msg  = "ERROR: could not find all arguments for function.\n"
      msg += "expected: "+str(rargs)+"\n"
      msg += "missing: "+str(missing)+"\n"
      raise RuntimeError(msg)

    result = func(**args)

    return result
  
class SFFormatter(object):
  def __init__(self, delimiters=None):
    self.delimiters = ('{','}') if delimiters is None else delimiters
    self.throw = False
    self.warn  = False

    self.token = pyparsing.Literal(self.delimiters[0]) + pyparsing.SkipTo(pyparsing.Literal(self.delimiters[1]), failOn=pyparsing.Literal(self.delimiters[0])) + pyparsing.Literal(self.delimiters[1])
  

  def fmt(self,text,*args,**kwargs):

    def replaceToken(text,loc,toks):
      exp = toks[1]
      try:
        # use the build-in string format method
        return ('{'+exp+'}').format(*args,**kwargs)
      except Exception as e:
        if self.throw:
          raise e
        if self.warn:
          print("WARNING: failed to replace '"+exp+"' using string.format().")

        return None

    self.token.setParseAction(replaceToken)
    text = self.token.transformString( text )

    return text

# a context manager for temperarily disabling
# flags in an instance
class set_state_context(object):
  def __init__(self,obj,state):
    self.obj = obj
    self.state = state
    self.saved_state = None
  def __enter__(self):
    self.saved_state = dict()
    for k in self.state.keys():
      self.saved_state[k] = getattr(self.obj,k)
      setattr(self.obj,k,self.state[k])
  def __exit__(self,type,value,traceback):
    for k in self.state.keys():
      setattr(self.obj,k,self.saved_state[k])
    self.saved_state = None
