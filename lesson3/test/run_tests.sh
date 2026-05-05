#!/bin/bash

FILE=$1
MODE=$2

if [ "$MODE" == "lvn" ]; then
    bril2json < "$FILE" | python3 ../local_value_numbering.py

elif [ "$MODE" == "dce" ]; then
    bril2json < "$FILE" | python3 ../dead_code_elimination.py 

elif [ "$MODE" == "full" ]; then
    bril2json < "$FILE" \
    | python3 ../local_value_numbering.py \
	| bril2json \
    | python3 ../dead_code_elimination.py \
    | bril2json | brili

else
    echo "Usage: ./run_tests.sh <file.bril> [lvn|dce|full]"
fi
