from .WriterBase import *
from ..Assignment import *

from pylatex import Document,Command,Head,PageStyle,Package,Itemize,Enumerate
from pylatex.utils import italic, NoEscape



class Latex(WriterBase):
  def __init__(self,fh=None):
    super().__init__(fh)
    self._packages = collection()
    self._packages += "physics"
    self._packages += "siunitx"
    self._packages += "fullpage"

  @property
  def packages(self):
    return self._packages

  @packages.setter
  def packages(self,val):
    self._packages = val

  def dump(self,ass,fh=None):
    fh = super().get_fh(fh)

    doc = Document()

    self.build_preamble(doc,ass)
    self.build_questions(doc,ass)

    fh.write(doc.dumps())

    return
    
  def build_questions(self,doc,ass):

    enumeration_symbols = list()
    if ass.meta.has("config"):
      if 'enumeration_symbols' in ass.meta.config:
        for symb in ass.meta.config['enumeration_symbols']:
          enumeration_symbols.append(symb)

    while len(enumeration_symbols) < 5:
      enumeration_symbols.append(r'\arabic*.')
        
    level = 0
    with doc.create(Enumerate(enumeration_symbol=NoEscape(enumeration_symbols[level]))) as qlist:
      level += 1
      for q in ass._questions:
        qlist.add_item( NoEscape(q.formatted_text) )
        # if q._answer is not None:
          # pass
        with doc.create(Enumerate(enumeration_symbol=NoEscape(enumeration_symbols[level]))) as plist:
          level += 1
          for p in q._parts:
            plist.add_item( NoEscape(p.formatted_text) )

        level -= 1

      level -= 1


  def build_preamble(self,doc,ass):

    header_and_footer = PageStyle("header")
    if ass.meta.has("header"):
      for h in ass.meta.header:
        with header_and_footer.create(Head(h)):
          header_and_footer.append( NoEscape(ass.meta.header[h]) )
    if ass.meta.has("footer"):
      for f in ass.meta.footer:
        with header_and_footer.create(Foot(f)):
          header_and_footer.append( NoEscape(ass.meta.footer[f]) )
    doc.preamble.append(header_and_footer)

    for e in self._packages:
      try:
        p,o = e
      except:
        p = e
        o = None

      doc.preamble.append(Package(p,o))


    if ass.meta.has("title"):
      doc.preamble.append(Command('title',ass.meta.title))
    if ass.meta.has("date"):
      doc.preamble.append(Command('date',ass.meta.date))

    

