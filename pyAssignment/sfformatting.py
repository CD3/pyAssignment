
import pyparsing


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


def fmt( text, *args, **kwargs ):
  delimiters = None
  if 'delimiters' in kwargs:
    delimiters = kwargs['delimiters']

  formatter = SFFormatter(delimiters=delimiters)

  return formatter.fmt( text, *args, **kwargs )



class Namespace(dict):
    def __init__(self,**kwargs):
        dict.__init__(self,kwargs)
        self.__dict__ = self
    def fmt(self,text):
      '''Format a string using self as context.'''
      return fmt(text, **self.__dict__)
    def call(self,func):
      '''Call a function with argument from self.'''
      pass

