import json
import pathlib
import sys
import xml
import xml.etree.ElementTree as ET
from typing import Annotated

import jinja2
import pint
import typer

import pyassignment.assignment
import pyassignment.writers

app = typer.Typer()

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity
ureg2 = pint.UnitRegistry()
Q2_ = ureg.Quantity


class UnknownTag(Exception):
    def __init__(self, tag):
        super().__init__(f"Unknown tag '{tag}'")


def quantity_format(v, sigfit=3):
    if type(v) is not Q_:
        return v

    if type(v.magnitude) is int:
        return f"{{v:Lx}}".format(v=v)

    return f"{{v:.{sigfig}Lx}}".format(v=v)


@app.command()
def main(assignment_file: Annotated[pathlib.Path, typer.Argument()]):
    if not assignment_file.exists():
        print(f"File {assignment_file} does not exist.")
        raise typer.Exit(1)

    tree = ET.parse(assignment_file)
    root = tree.getroot()

    ass = build_assignment(root)
    writer = pyassignment.writers.simple.Simple(sys.stdout)
    writer.dump(ass)

    print("Done building assignment.")


def build_assignment(root):
    # add stuff....

    ass = pyassignment.assignment.assignment.Assignment()
    for child in root:
        if child.tag == "question":
            q = build_question(child)
            ass._questions.append(q)
        elif child.tag == "information":
            pass
        elif child.tag == "meta":
            pass
        else:
            raise UnknownTag(child.tag)

    return ass


def build_question(root):
    known_tags = ["inputs","outputs","calculations","answer"]
    for child in root:
        if child.tag not in known_tags:
            raise UnknownTag(child.tag)

    q = pyassignment.assignment.question.Question()

    ctx_script = build_context_script(root)
    print(ctx_script)

    # env = jinja2.Environment(undefined=jinja2.DebugUndefined)
    # env.filters["quant"] = quantity_format
    # tmpl = env.from_string(root.text)
    #
    # q.text = tmpl.render(ctx)

    return q

def build_context_script(root):
    # build render script to be ran in separate process
    # should include:
    # - common setup code
    # - initial variable definitions
    # - calculations (that use initial variables)
    # - ? some final variable definitions?
    context_tags = [
            'inputs',
            'calculations',
            'outputs',
            ]

    render_script_lines = []
    context_elements = { element.tag:element for element in root if element.tag in context_tags}
    for tag in context_elements:
        if tag not in context_elements:
            continue
        element = context_elements[tag]

        if element.tag == "inputs":
            render_script_lines += build_context_script_inputs(element)
        if element.tag == "calculations":
            render_script_lines += build_context_script_calculations(element)
        if element.tag == "outputs":
            render_script_lines += build_context_script_outputs(element)
    print(render_script_lines)


def build_context_script_inputs(element):
    render_script_lines = []
    for line in element.text.split("\n"):
        line = line.strip()
        if line == "":
            continue
        if '=' in line:
            k,v = line.split('=',maxsplit=2)
            line = f"{k} = Q_('{v}')"

        render_script_lines.append(line)

    return render_script_lines

def build_context_script_calculations(element):
    render_script_lines = []
    for line in element.text.split("\n"):
        line = line.strip()
        if line == "":
            continue
        render_script_lines.append(line)

    return render_script_lines

def build_context_script_outputs(element):
    render_script_lines = []
    for line in element.text.split("\n"):
        line = line.strip()
        if line == "":
            continue
        if '=' in line:
            k,v = line.split('=',maxsplit=2)
            line = f"{k} = Q_('{v}')"

        render_script_lines.append(line)

    return render_script_lines




def build_variables(root):
    ctx = {}
    lines = root.text.split("\n")
    for line in lines:
        if line is None:
            continue
        if "=" not in line:
            continue
        n, v = line.split("=", maxsplit=2)
        ctx[n.strip()] = Q_(v.strip())

    return ctx


def build_information(root):
    pass
