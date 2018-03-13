from types import SimpleNamespace

class Namespace(SimpleNamespace):
  def has(self,attr):
    return hasattr(self,attr)

  def clear(self):
    self.__dict__.clear()

  def __len__(self):
    return len(self.__dict__)

  
