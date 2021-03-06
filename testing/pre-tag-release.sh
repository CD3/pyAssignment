#! /bin/bash

set -e

tag=$1
shift

root=$(git rev-parse --show-toplevel)
echo "cd'ing to root directory ($root)"
cd $root

./testing/pre-tag-release-run_tests.sh ${tag}
./testing/pre-tag-release-update_version.sh ${tag}
