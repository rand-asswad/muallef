#!/bin/sh

REPO_NAME="muallef"
GH_USERNAME="rand-asswad"

OUTPUT_DIR=_out
GH_PAGES_DIR=_gh_pages

MAKE_ARGS="clean all"

# clone gh-pages branch (if not exists)
[ -d $GH_PAGES_DIR/.git ] || git clone -b gh-pages git@github.com:$GH_USERNAME/$REPO_NAME.git $GH_PAGES_DIR
touch $GH_PAGES_DIR/.nojekyll

# build docs if needed
[ -d $OUTPUT_DIR ] || make $MAKE_ARGS

# copy output
cp -r $OUTPUT_DIR/* $GH_PAGES_DIR/

# update gh-pages branch
cd $GH_PAGES_DIR
git add --all *
git commit -m "Update RMD output"
git push -q origin gh-pages
