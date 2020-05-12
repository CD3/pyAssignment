import pytest

import io,os,re

from pyAssignment.Utils import *

def test_html_images():

  text = image2html( "./data/test-image.png" )
  assert text.startswith(r'<img src="data:image/png;base64,')
  assert text.endswith(r'" >')
  if not os.path.isdir("_tmp"):
    os.mkdir("_tmp")
  with open( "_tmp/html-image-png.html","w") as f:
    f.write(text)



  text = image2html( "./data/test-image.jpg" )
  assert text.startswith(r'<img src="data:image/jpg;base64,')
  assert text.endswith(r'" >')
  if not os.path.isdir("_tmp"):
    os.mkdir("_tmp")
  with open( "_tmp/html-image-jpg.html","w") as f:
    f.write(text)



  text = image2html( "./data/test-image.svg" )
  if not os.path.isdir("_tmp"):
    os.mkdir("_tmp")
  with open( "_tmp/html-image-svg.html","w") as f:
    f.write(text)


