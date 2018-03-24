#! /bin/bash

set -e

root=$(git rev-parse --show-toplevel)
cd $root
cd testing
../env/bin/pytest

