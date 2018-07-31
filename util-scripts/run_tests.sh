#! /bin/bash

sudo docker run --rm -v $PWD:/var/repo cdc3/pyassignment-testing-3.6:latest "$@"
