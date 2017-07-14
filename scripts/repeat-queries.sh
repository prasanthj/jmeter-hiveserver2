#!/bin/bash
set -e

INPUT=${1:-"queries.csv"}
export REPETITIONS=${2:-4}
FILENAME=${INPUT%.csv}
OUTFILE=${FILENAME##*/}_$REPETITIONS.csv

echo "Input: $INPUT"
echo "Repetitions: $REPETITIONS"
echo "Output: $OUTFILE"
echo ""

cat $INPUT | awk -F^ '{for (i=1; i <= ENVIRON["REPETITIONS"]; i++) { printf "%s_%d^%s\n",$1,i,$2}}' > $OUTFILE

echo "Completed!"
