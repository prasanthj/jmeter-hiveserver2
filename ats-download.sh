#!/bin/bash

DAG_PREFIX=$1
DAG_IDX_FROM=$2
DAG_IDX_TO=$3
for (( i=$DAG_IDX_FROM; i<=$DAG_IDX_TO; i++ ))
do
  echo "Downloading ATS data for ${DAG_PREFIX}_${i} .."; 
  time hadoop jar tez-debug-jars/tez-debugtool-0.0.1-SNAPSHOT.jar org.apache.tez.tools.debug.Main --dagId ${DAG_PREFIX}_${i} --sourceType HIVE_ATS --sourceType TEZ_ATS; 
done
