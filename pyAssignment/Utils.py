from types import SimpleNamespace
from inspect import getargspec

import os

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

class collection(list):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)

  def find(self, pattern, exact=True):
    if exact:
      return self.index(pattern)
    else:
      for i in range(len(self)):
        if pattern in self[i]:
          return i
        return -1

  def __iadd__(self,val):
    if not isinstance(val,list):
      val = [val]
    return super().__iadd__(val)

class LatexAux(object):
  def __init__(self,filename):
    self._filename = filename
    self._newlabels = dict()

    class parser:
      pp = pyparsing
      name = pp.Word(pp.alphas)
      argument = pp.originalTextFor(pp.nestedExpr( '{', '}' ))

      command = pp.Combine( pp.WordStart('\\') + pp.Literal('\\') + name('name') + pp.ZeroOrMore(argument)('arguments') )

      newlabel = Namespace()
      newlabel.arg1 = argument('name')
      newlabel.arg2 = argument('label') #+argument('page')

    if not os.path.exists(self._filename): raise RuntimeError( "LatexAux: .aux file does not appear to exist: "+self._filename )
    with open(filename,'r') as f:
      text = f.read()
    

    res = parser.command.searchString(text)


    # extract labels from \newlabel commands
    for r in res:
      if r.name == "newlabel":
        name = r.arguments[0].strip('{}')
        # argument contains two sub-arguments that we need to parse
        label,page = [e.strip('{}') for e in (parser.argument('label') + parser.argument('page')).parseString( r.arguments[1][1:-1] )]
        
        self._newlabels[name] = {'label':label,'page':page}

  @property
  def labels(self):
    return self._newlabels


class ColorCodes:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


