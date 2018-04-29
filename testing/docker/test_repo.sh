#! /bin/bash

set -e

cp -r /var/repo repo
cd repo
pytest "$@"

python ./setup.py install
