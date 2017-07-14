#!/bin/bash
set -e

QUERY_FILE=${1:-"queries.csv"}
RESULTS_FILE=${2:-"results.xml"}
OUTPUT="report.txt"
COLUMN_SEPARATOR='\t'

test -f $QUERY_FILE >/dev/null 2>&1 || { echo >&2 "$QUERY_FILE not found!"; exit 1; }
test -f $RESULTS_FILE >/dev/null 2>&1 || { echo >&2 "$RESULTS_FILE not found!"; exit 1; }

echo "Queries: $QUERY_FILE"
echo "Results: $RESULTS_FILE"
echo "Output: $OUTPUT"

> $OUTPUT
grep ".sql" $QUERY_FILE | cut -f1 -d. | sort | uniq | while read query; do
  printf "$query$COLUMN_SEPARATOR" >> $OUTPUT
  grep query $RESULTS_FILE | grep -Ev "Error|Set" | grep "$query.sql" | cut -f2 -d= | cut -f2 -d'"' | tr '\n' $COLUMN_SEPARATOR >> $OUTPUT
  printf "\n" >> $OUTPUT
done

echo ""
echo "Completed!"
