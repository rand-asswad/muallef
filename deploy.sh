#!/bin/sh

set -e

# read tokens
[ -z "${GH_PAGES_PAT}" ] && exit 0
[ "${TRAVIS_BRANCH}" != "master" ] && exit 0

# git global configs
git config --global user.email "asswad.rand@gmail.com"
git config --global user.name "Rand Asswad"

# clone gh-pages branch
git clone -b gh-pages https://${GITHUB_PAT}@github.com/${TRAVIS_REPO_SLUG}.git rmd_output

# copy output
cd rmd_output
cp -r ../docs/out/* ./

# update gh-pages branch
git add --all *
git commit -m "Update RMD output" || true
git push -q origin gh-pages