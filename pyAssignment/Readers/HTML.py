from .ReaderBase import *
from lxml import etree


class HTML(ReaderBase):
  '''A (very) limited HTML parser. Currently
     just supports parsing multiple choice questions.'''


  def __init__(self,fh=None):
    super().__init__(fh)

  def load(self, fh=None, ass=None):
    fh = super().get_fh(fh)

    d = dict()
    tree = etree.parse(fh,etree.HTMLParser())

    current_section = None
    for e in tree.xpath('/html/body/*'):
      if e.tag == 'h1':
        current_section = e.text.lower()

      if e.tag == 'ol':
        if current_section == 'questions':
          d['questions'] = self._parse_questions( e )





    return self._load_from_dict(d)

  def _parse_questions(self, tree ):
    l = list()
    for e in tree.xpath('*'):
      if e.tag == 'li':
        l.append(dict())
        l[-1]['text'] = e.text
      if e.tag == 'ol':
        l[-1]['answer'] = self._parse_mc_answer(e)

    return l

  def _parse_mc_answer(self, tree ):
    d = dict()
    d['choices'] = list()
    for c in tree.xpath('li'):
      text = None
      text = c.text
      if text is None and len(c) > 0:
        text = c[0].text
        
      if text is None:
        raise RuntimeError("ERROR: could not parse answer text in MC question'"+etree.tostring(c).decode('utf-8')+"'")

      d['choices'].append(text)

    return d

    

