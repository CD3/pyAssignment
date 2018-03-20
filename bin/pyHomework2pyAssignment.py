#! /usr/bin/env python2

import os,sys
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

def fmt_Anserr(a):
  return "NONE"


with open(args.output,'w') as f:

  f.write("ass = Assignment()\n")

  for q in ass._questions:
    f.write("""
with ass.add_question() as q:
  q.text = "{TEXT}"
""".format(TEXT=q.question_str))

    for k in q.v.__dict__:
      f.write("""\
  q.NS.{k} = '{v}'\n""".format(k=k,v=fmt_NS_var(q.v.__dict__[k])))

    for a in q._answers:
      f.write("{}\n".format(fmt_Answer(a)))

    for p in q._parts:
      f.write("""\
  with ass.add_part() as p:
    p.text = {TEXT}
""".format(TEXT=p.question_str))
