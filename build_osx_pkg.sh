#!/bin/bash

# build osx pkg
# install location: /Library/quicklojure
# package structure
# /usr/bin/clj
# /Library
#   + quicklojure/*
#   + lib/*.jar
#
mkdir -p .tmp/usr/bin .tmp/Library/quicklojure
cp -R src/* .tmp/Library/quicklojure/
cp -R lib .tmp/Library/quicklojure/
cd .tmp/usr/bin
ln -s /Library/quicklojure/clj.sh clj
cd -
pkgbuild --identifier quicklojure.pkg.app --root .tmp quicklojure.pkg
rm -rf .tmp
