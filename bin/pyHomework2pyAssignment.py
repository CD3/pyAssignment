#! /usr/bin/env python2

import os,sys,textwrap
from argparse import ArgumentParser

if os.path.isdir( '../pyAssignment' ):
  sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

parser = ArgumentParser(description="A sweet program for doing something.")

parser.add_argument("homework_script",
                    action="store",
                    help="Homework script" )

parser.add_argument("-o", "--output",
                    action="store",
                    default="/dev/stdout",
                    help="Output file",)


args = parser.parse_args()



with open(args.homework_script,'r') as f:
  input_lines = f.readlines()

def filt(line):
  if line.startswith("Build()"):
    return False
  return True

def trans(line):
  if line.startswith("Setup("):
    return line.replace('__file__',"'{}'".format(args.homework_script))
  return line

script_lines = [ trans(line) for line in filter( filt, input_lines ) ]
script_text = "".join(script_lines)

script_dir = os.path.dirname(args.homework_script)

currdir = os.getcwd()
os.chdir(script_dir)
sys.path.append( script_dir )
exec(script_text)
os.chdir(currdir)



def fmt_NS_var(v):
  return "{}".format(v)

def fmt_NS_assignment_line(k,v):
  return "q.NS.{k} = '''{v}'''\n".format(k=k,v=fmt_NS_var(v))

def fmt_Answer(a):
  return "NONE"

def fmt_Question(q):
  text = """\
with ass.add_question() as q:
  q.text = '''{TEXT}'''

""".format(TEXT=q.question_str)
  return text

def fmt_Part(p):
  text = """\
with q.add_part() as p:
  p.text = '''{TEXT}'''

""".format(TEXT=p.question_str)
  return text

def indent(text,level=1):
  if level == 0:
    return text

  if level == 1:
    lines = list()
    for line in text.split("\n"):
      if len( line.strip() ) > 0:
        lines.append("  " + line)
      else:
        lines.append(line)

    return "\n".join( lines )

  if level > 1:
    return indent(text,level-1)

with open(args.output,'w') as f:
  f.write("import sys\n")
  f.write("from pyAssignment.Assignment import Assignment\n")
  f.write("from pyAssignment.Writers import Simple\n")

  f.write("ass = Assignment()\n")

  for q in ass._questions:
    f.write("\n")
    f.write( fmt_Question(q) )

    for k in q.v.__dict__:
      f.write( indent(fmt_NS_assignment_line(k,q.v.__dict__[k])))

    for a in q._answers:
      f.write(indent(fmt_Answer(a)))

    for p in q._parts:
      f.write( indent(fmt_Part(p)))

  f.write("""\
writer = Simple(sys.stdout)
writer.dump(ass)
""")


