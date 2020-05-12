import os,contextlib
@contextlib.contextmanager
def TempDir(path):
  CWD = os.getcwd()
  os.chdir(path)
  try:
    yield
  finally:
    os.chdir(CWD)
