#!/bin/bash
set -e

export _JAVA_OPTIONS="-Djava.awt.headless=true -Xmx8192m"

# to enable jmeter dashboard use the following
#jmeter -n -t hive2.jmx -l hive2.jtl -e -o hive2-dashboard

jmeter -n -t hive2.jmx
