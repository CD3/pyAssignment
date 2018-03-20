from .ReaderBase import *
import mistletoe
import html.parser


class HTML(ReaderBase):

  class Parser(html.parser.HTMLParser):
    def __init__(self,ass):
      super().__init__()
      self.ass = ass
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)


  def __init__(self,fh=None):
    super().__init__(fh)

  def load(self, fh=None, ass=None):
    if ass is None:
      ass = Assignment()

    fh = super().get_fh(fh)

    parser = HTML.Parser(ass)
    parser.feed(fh)


    return ass

    

