#! /bin/bash

set -e

tag=$1
shift

cd testing
../env/bin/pytest

echo "__version__ = '${tag}'" > version.py
git add version.py
git commit -m "version bump: ${tag}"

