#!/bin/sh

export PYTHONPATH=$(pwd):$PYTHONPATH

startingDir=$(pwd)
for dir in $(find tests/ -type d)
do
    dir=${dir%*/}
    cd ${dir};
    python -m unittest discover .;
    if [ $? -ne "0" ]; then
	echo "There were test failures. Stopping."
	exit 1
    fi
    cd ${startingDir}
done
echo "All tests have passed."
exit 0
