#!/bin/sh
while read p; do
  pip3 install $p -U
done < ./Depfiles/dependencies.pip

while read p; do
  composer require p
done < ./Depfiles/dependencies.comp

if [ "$HOSTNAME" = "venus" ] || [ "$HOSTNAME" = "mars" ] ; then
  npm install
  gulp --gulpfile src/site/development-assets/generate-css.js
fi