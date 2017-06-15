#!/bin/bash
set -e

INPUT=${1:-"queries.csv"}
FILENAME=${INPUT%.csv}
OUTFILE=${FILENAME##*/}_sorted.csv

echo "Input: $INPUT"
echo "Output: $OUTFILE"
echo ""

cat $INPUT | cut -f1 -d^ | cut -f1 -d"." | cut -f2 -d'y' | sort -n |  sed "s/\$/.sql/" | sed 's/^/query/' | while read query; do grep $query $INPUT; done > $OUTFILE

echo "Completed!"
