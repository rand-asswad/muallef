#!/bin/sh

set -ev

cd docs

make clean
make pdf html presentation gitbook

cd ..