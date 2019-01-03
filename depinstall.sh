#!/bin/sh
while read p; do
pip3 install $p
done < requirements.pip
