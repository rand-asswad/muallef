#!/bin/sh

cd docs

make clean
make pdf html presentation gitbook

cd ..