#!/bin/bash

# build osx pkg
# install location: /Library/quicklojure
mkdir -p .tmp/usr/bin .tmp/Library
cp -R quicklojure .tmp/Library/
cd .tmp/usr/bin
ln -s /Library/quicklojure/clj clj
cd -
pkgbuild --identifier quicklojure.pkg.app --root .tmp quicklojure.pkg
#rm -rf .tmp
