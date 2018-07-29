from .WriterBase import *
from ..Assignment import *

from pylatex import Document,Command,Head,Foot,PageStyle,Package,Itemize,Enumerate,Figure
from pylatex.section import Section,Paragraph
from pylatex.utils import italic, NoEscape



class Latex(WriterBase):
  '''
  Customization Points:

  assignment.meta.title : document title.
  assignment.meta.date : document date.
  assignment.meta.header : dict of fancy headers.
  assignment.meta.footer : dict of fancy footers.
  assignment.meta.make_key : bool that specifies if a key should be printed at the end of the document.
  assignment.meta.header_includes : list of lines that will be added to the preamble.
  assignment.meta.config['questions']['enumeration_symbols'] : list of symbols used for question numbering.
  assignment.meta.config['answer']['multiple_choice_symbol'] : symbol used for multiple choice answers.
  assignment.meta.config['answer']['numerical_spacing'] : spacing added after a question with a numerical answer.
  assignment.meta.config['answer']['numerical_spacing'] : spacing added after a question with a numerical answer.

  '''
  def __init__(self,fh=None):
    super().__init__(fh)
    self._packages = collection()
    self._packages += "physics"
    self._packages += "siunitx"
    self._packages += "fullpage"
    self._packages += "datetime"

    self.make_key = False

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

    make_key = self.make_key
    # if assignment has a make_key entry, use it instead
    if ass.meta.has('make_key'):
      make_key = ass.meta.make_key
    if make_key:
      self.build_key(doc,ass)

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
        
    for i in sorted(ass._information.keys()):
      info = ass._information[i]
      doc.append(NoEscape(info.formatted_text))

    level = 0
    with doc.create(Enumerate(enumeration_symbol=NoEscape(enumeration_symbols[level]))) as qlist:
      level += 1
      for i in range(len(ass._questions)):
        q = ass._questions[i]
        label = r"\label{%s}"%q._uuid
        if q.meta.has('label'):
          label += r"\label{%s}"%q.meta.label

        qlist.add_item( NoEscape(label+q.formatted_text) )



        if q._answer is not None:
          try: # multiple choice
            # NOTE: need to access all_formatted_choices member of q._answer
            # so that try block will fail before an enumeration is created
            all_choices = self.MC_Answer_get_all_choices(q._answer)
            symb = r'\alph*)'
            try:
              symb = ass.meta.config['answer']['multiple_choice/symbol']
            except:
              pass
            with doc.create(Enumerate(enumeration_symbol=NoEscape(symb))) as clist:
              for choice in all_choices:
                label = r'\label{%s}'%id(choice)
                clist.add_item( NoEscape(label+choice) )
          except:
            pass

          try: # numerical
            ans = q._answer.quantity
            space="2in"
            try:
              space = ass.meta.config['answer']['numerical/spacing']
            except:
              pass
            doc.append(NoEscape(r"\vspace{%s}"%space))
          except:
            pass


          try: # text
            ans = q._answer.text
            space="2in"
            try:
              space = ass.meta.config['answer']['text/spacing']
            except:
              pass
            doc.append(NoEscape(r"\vspace{%s}"%space))
          except:
            pass




        with doc.create(Enumerate(enumeration_symbol=NoEscape(enumeration_symbols[level]))) as plist:
          level += 1
          for p in q._parts:
            label = r"\label{%s}"%p._uuid
            if p.meta.has('label'):
              label += r"\label{%s}"%p.meta.label

            plist.add_item( NoEscape(label+p.formatted_text) )

        level -= 1

      level -= 1

  def build_preamble(self,doc,ass):

    # add packages
    for e in self._packages:
      try:
        p,o = e
      except:
        p = e
        o = None

      doc.preamble.append(Package(p,o))

    # allow assignment metadata to add header info
    # this allows support pandoc-style config data in input files
    if ass.meta.has("header_includes"):
      if not isinstance( ass.meta.header_includes, list ):
        ass.meta.header_includes = [ass.meta.header_includes]
      for line in ass.meta.header_includes:
        doc.preamble.append(NoEscape(line))

    doc.preamble.append(Package('fancyhdr'))
    doc.preamble.append(Command('pagestyle','fancyplain'))
    doc.preamble.append(Command('setlength',[NoEscape(r'\headheight'),'0.5in']))
    if ass.meta.has("header"):
      for h in ass.meta.header:
        doc.preamble.append(Head(position=h,data=NoEscape(ass.meta.header[h])))
    if ass.meta.has("footer"):
      for f in ass.meta.footer:
        doc.preamble.append(Foot(position=f,data=NoEscape(ass.meta.footer[f])))
    doc.preamble.append(Command('renewcommand',[NoEscape(r'\headrulewidth'),'0pt']))



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
        label = ("\label{%s}"%f._uuid)
        if f.meta.has("label"):
          label += r"\label{%s}"%f.meta.label
        fig.add_caption(NoEscape(label+f.formatted_caption))

  def build_key(self,doc,ass):
    doc.append(NoEscape(r"\newpage"))
    doc.append(NoEscape(r"\textbf{\large Answers:}"))
    for i in range(len(ass._questions)):
      q = ass._questions[i]
      doc.append(NoEscape(r"\\ \ref{%s}"%q._uuid))

      if q._answer is not None:
        try: # multiple choice
          answers = [ r'\ref{%s}'%id(choice) for choice in self.MC_Answer_get_correct_choices(q._answer) ]
          doc.append(NoEscape(",".join(answers)))
        except: pass

        try: # numerical
          ans = q._answer.quantity
          doc.append(NoEscape("{}".format(ans)))
        except:
          pass

        try: # text
          ans = q._answer.text
          doc.append(NoEscape("{}".format(ans)))
        except:
          pass




    

