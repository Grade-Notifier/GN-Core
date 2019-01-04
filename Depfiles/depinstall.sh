#!/bin/sh
while read p; do
pip3 install $p
done < dependencies.pip

while read p; do
composer require p
done < dependencies.comp
