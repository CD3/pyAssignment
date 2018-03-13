from types import SimpleNamespace
import pyparsing

class Namespace(SimpleNamespace):
  def has(self,attr):
    return hasattr(self,attr)

  def clear(self):
    self.__dict__.clear()

  def __len__(self):
    return len(self.__dict__)

  
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

