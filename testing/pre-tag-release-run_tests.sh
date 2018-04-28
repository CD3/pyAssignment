#! /bin/bash

set -e

root=$(git rev-parse --show-toplevel)
cd $root
./util-scripts/run_tests.sh

