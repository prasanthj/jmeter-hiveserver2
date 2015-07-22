# jmeter-hiveserver2
Scripts to make JMeter JDBC sampler work with hiveserver2.

### Instructions to run
- Install Apache JMeter binaries from [here].
- Run ./testgen.py > example.jmx
- jmeter -t example.jmx
- Edit the JDBC hostname, password etc and the queries as you please
- Change the thread count, loop count, pool size (usually pool size == thread count)
- Save/Run etc.
  - No GUI mode
    - jmeter -n -t HiveServer2.jmx
  - For JMeter debug logging
    - jmeter -n -t HiveServer2.jmx -Ljmeter=DEBUG -Ljmeter.engine=DEBUG
  - Successful run should have 0% error like below
```
jmeter -n -t /work/pkgs/jmeter-configs/HiveServer2.jmx
Creating summariser <summary>
Created the tree successfully using /work/pkgs/jmeter-configs/HiveServer2.jmx
Starting the test @ Fri May 15 17:05:49 PDT 2015 (1431734749458)
Waiting for possible shutdown message on port 4445
summary =      5 in    22s =    0.2/s Avg: 19510 Min: 16585 Max: 21649 Err:     0 (0.00%)
Tidying up ...    @ Fri May 15 17:06:12 PDT 2015 (1431734772001)
... end of run
```
  - GUI mode
    - jmeter
    - Click Open and choose the HiveServer2.jmx file and press play button

[here]:http://jmeter.apache.org/download_jmeter.cgi

### To regenerate the jdbc uber jar for use with JMeter
- Checkout hive source and apply the following patches
  - git clone git@github.com:apache/hive.git
  - cd hive
  - Patch for hive uber JDBC jar. (NOTE: Skip this step if https://issues.apache.org/jira/browse/HIVE-9599 is already resolved). If not download the latest version of patch from HIVE-9599 and apply it
    -  curl https://issues.apache.org/jira/secure/attachment/12702319/HIVE-9599.2.patch | patch -p1
  - Patch for supporting setQueryTimeout implementation (NOTE: Skip this step if https://issues.apache.org/jira/browse/HIVE-9599 is already resolved). Only timeout = 0 is supported.
    - curl https://issues.apache.org/jira/secure/attachment/12733264/HIVE-10726.3.patch | patch -p0
- Compile hive
  - mvn clean install -DskipTests -Phadoop-2,dist
- Copy hive jdbc uber jar to $JMETER_HOME/lib
  - cp packaging/target/apache-hive-1.3.0-SNAPSHOT-jdbc.jar $JMETER_HOME/lib
