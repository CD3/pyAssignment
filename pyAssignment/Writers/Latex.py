from .WriterBase import *
from ..Assignment import *

from pylatex import Document,Command,Head,Foot,PageStyle,Package,Itemize,Enumerate,Figure
from pylatex.utils import italic, NoEscape



class Latex(WriterBase):
  '''
  Customization Points:

  assignment.meta.title : document title
  assignment.meta.date : document date
  assignment.meta.header : dict of fancy headers
  assignment.meta.footer : dict of fancy footers
  assignment.meta.config['questions']['enumeration_symbols'] : list of symbols used for question numbering.
  assignment.meta.config['answers']['multiple_choice_symbol'] : symbol used for multiple choice answers
  assignment.meta.config['answers']['numerical_spacing'] : spacing added after a question with a numerical answer
  assignment.meta.config['answers']['numerical_spacing'] : spacing added after a question with a numerical answer

  '''
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
    self.build_figures(doc,ass)

    fh.write(doc.dumps())

    return
    

  def build_questions(self,doc,ass):
    enumeration_symbols = list()
    if ass.meta.has("config"):
      if ass.meta.config.get('question',dict()).get('enumeration_symbols', None) is not None:
        for symb in ass.meta.config['question']['enumeration_symbols']:
          enumeration_symbols.append(symb)

    while len(enumeration_symbols) < 5:
      enumeration_symbols.append(r'\arabic*.')
        
    level = 0
    with doc.create(Enumerate(enumeration_symbol=NoEscape(enumeration_symbols[level]))) as qlist:
      level += 1
      for q in ass._questions:
        qlist.add_item( NoEscape(q.formatted_text) )
        if q._answer is not None:
          try: # multiple choice
            # NOTE: need to access all_formatted_choices member of q._answer
            # so that try block will fail before an enumeration is created
            choices = list(q._answer.all_formatted_choices)
            symb = r'\alph*)'
            try:
              symb = ass.meta.config['answers']['multiple_choice/symbol']
            except:
              pass
            with doc.create(Enumerate(enumeration_symbol=NoEscape(symb))) as clist:
              for choice in choices:
                clist.add_item( NoEscape(choice) )
          except:
            pass

          try: # numerical
            ans = q._answer.quantity
            space="2in"
            try:
              space = ass.meta.config['answers']['numerical/spacing']
            except:
              pass
            doc.append(NoEscape(r"\vspace{%s}"%space))
          except:
            pass


          try: # numerical
            ans = q._answer.text
            space="2in"
            try:
              space = ass.meta.config['answers']['text/spacing']
            except:
              pass
            doc.append(NoEscape(r"\vspace{%s}"%space))
          except:
            pass




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


    maketitle = False
    if ass.meta.has("title"):
      doc.preamble.append(Command('title',ass.meta.title))
      maketitle = True
    if ass.meta.has("date"):
      doc.preamble.append(Command('date',ass.meta.date))
      maketitle = True
    else:
      doc.preamble.append(Command('date',''))

    if maketitle:
      doc.append(NoEscape(r'\maketitle'))

  def build_figures(self,doc,ass):
    for f in ass._figures:

      with doc.create(Figure()) as fig:
        width=r'0.4\textwidth'
        if f.meta.has('width'):
          width=f.meta.width
        fig.add_image(f.filename,width=NoEscape(width))
        fig.add_caption(NoEscape(f.formatted_caption))




    

