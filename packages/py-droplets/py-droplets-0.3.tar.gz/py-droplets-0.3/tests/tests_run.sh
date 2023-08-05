#!/bin/bash

export PYTHONPATH=../../py-pde:$PYTHONPATH
export NUMBA_WARNINGS=1
export MPLBACKEND="agg"

if [ ! -z $1 ] 
then 
	# test pattern was specified 
	echo 'Run unittests with pattern '$1
	python3 -m pytest -rs -k "$1" . ..
else
	# test pattern was not specified
	echo 'Run all unittests'
    python3 -m pytest -rs . ..
fi
