"""Nox sessions."""
import os
import shlex
import shutil
import sys
from pathlib import Path
from textwrap import dedent

import nox


try:
    from nox_poetry import Session
    from nox_poetry import session
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.

    Please install it using the following command:

    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message)) from None


package = "lhaz_cli"
python_versions = ["3.8", "3.10"]
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = ("tests",)


@session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install("pytest")
    session.install(".")
    with session.chdir("testing"):
        session.run("pytest", *session.posargs)
