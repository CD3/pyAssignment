import pytest

import io,os,re,pathlib

import utils

from pyAssignment.Utils import *

def test_html_images(tmpdir):
  cwd = str(pathlib.Path().absolute())
  with utils.TempDir(tmpdir):

    text = image2html( cwd+"/data/test-image.png" )
    assert text.startswith(r'<img src="data:image/png;base64,')
    assert text.endswith(r'" >')
    if not os.path.isdir("_tmp"):
      os.mkdir("_tmp")
    with open( "_tmp/html-image-png.html","w") as f:
      f.write(text)



    text = image2html( cwd+"/data/test-image.jpg" )
    assert text.startswith(r'<img src="data:image/jpg;base64,')
    assert text.endswith(r'" >')
    if not os.path.isdir("_tmp"):
      os.mkdir("_tmp")
    with open( "_tmp/html-image-jpg.html","w") as f:
      f.write(text)



    text = image2html( cwd+"/data/test-image.svg" )
    if not os.path.isdir("_tmp"):
      os.mkdir("_tmp")
    with open( "_tmp/html-image-svg.html","w") as f:
      f.write(text)


