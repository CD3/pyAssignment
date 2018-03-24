#! /bin/bash

set -e

tag=$1
shift

git stash

cd testing
../env/bin/pytest

echo "__version__ = '${tag}'" > version.py

git stash pop
