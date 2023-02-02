import subprocess

def run(cmd,**kwargs):
  '''
  Run a shell command and return the exit code, standard output, and standar error.
  '''
  c = subprocess.run( cmd, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE )
  r = c.returncode
  o = c.stdout
  e = c.stderr

  try:
    o = o.decode('utf-8')
    e = e.decode('utf-8')
  except: pass

  if 'debug' in kwargs and kwargs['debug']:
    print("CMD:",cmd)
    print("R:",r)
    print("O:",o)
    print("E:",e)

  return r,o,e


