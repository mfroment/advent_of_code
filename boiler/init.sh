#!/bin/bash

mkdir -p input tests tests/input

BASEDIR=$(dirname $0)
PARENT=$(basename $(pwd))
for file in $(find $BASEDIR -type f ! -path $0 -exec realpath --relative-to=$BASEDIR {} \;)
do
  source=$BASEDIR/$file
  target=${file/DAY/$1}
  if [ ! -f $target ]; then
    echo "Creating: ${target}"
    perl -npe 's,DAY,'$1',g;s,PARENT,'$PARENT',g;' $source > $target
  fi
done
