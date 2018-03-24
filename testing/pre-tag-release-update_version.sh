#! /bin/bash

set -e

tag=$1
shift

root=$(git rev-parse --show-toplevel)
echo "cd'ing to root directory ($root)"
cd $root

echo "__version__ = '${tag}'" > version.py
git add version.py
git commit -m "version bump: ${tag}"

