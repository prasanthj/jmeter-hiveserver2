import os,sys,re,math
from getopt import getopt
from glob import glob
from os.path import basename

testplan = """<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="2.8" jmeter="2.13 r1665067">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="Test Plan" enabled="true">
      <stringProp name="TestPlan.comments"></stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath">./jdbc-binaries/1.3.0-SNAPSHOT/apache-hive-1.3.0-SNAPSHOT-jdbc.jar</stringProp>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="LLAP" enabled="true">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="Loop Controller" enabled="true">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">%(repeats)d</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">%(threads)d</stringProp>
        <stringProp name="ThreadGroup.ramp_time">1</stringProp>
        <longProp name="ThreadGroup.start_time">1431644035000</longProp>
        <longProp name="ThreadGroup.end_time">1431644035000</longProp>
        <boolProp name="ThreadGroup.scheduler">false</boolProp>
        <stringProp name="ThreadGroup.duration"></stringProp>
        <stringProp name="ThreadGroup.delay"></stringProp>
      </ThreadGroup>
      <hashTree>
        <JDBCDataSource guiclass="TestBeanGUI" testclass="JDBCDataSource" testname="TPC-DS" enabled="true">
          <stringProp name="dataSource">hs2_tpcds</stringProp>
          <stringProp name="poolMax">%(threads)d</stringProp>
          <stringProp name="timeout">10000</stringProp>
          <stringProp name="trimInterval">60000</stringProp>
          <boolProp name="autocommit">false</boolProp>
          <stringProp name="transactionIsolation">DEFAULT</stringProp>
          <boolProp name="keepAlive">true</boolProp>
          <stringProp name="connectionAge">500000</stringProp>
          <stringProp name="checkQuery"></stringProp>
          <stringProp name="dbUrl">%(jdbc_tpcds)s</stringProp>
          <stringProp name="driver">org.apache.hive.jdbc.HiveDriver</stringProp>
          <stringProp name="username"></stringProp>
          <stringProp name="password"></stringProp>
        </JDBCDataSource>
        <hashTree/>
        <JDBCDataSource guiclass="TestBeanGUI" testclass="JDBCDataSource" testname="TPC-H" enabled="true">
          <stringProp name="dataSource">hs2_tpch</stringProp>
          <stringProp name="poolMax">%(threads)d</stringProp>
          <stringProp name="timeout">10000</stringProp>
          <stringProp name="trimInterval">60000</stringProp>
          <boolProp name="autocommit">false</boolProp>
          <stringProp name="transactionIsolation">DEFAULT</stringProp>
          <boolProp name="keepAlive">true</boolProp>
          <stringProp name="connectionAge">500000</stringProp>
          <stringProp name="checkQuery"></stringProp>
          <stringProp name="dbUrl">%(jdbc_tpch)s</stringProp>
          <stringProp name="driver">org.apache.hive.jdbc.HiveDriver</stringProp>
          <stringProp name="username"></stringProp>
          <stringProp name="password"></stringProp>
        </JDBCDataSource>
        <hashTree/>
        %(jdbc_queries)s
        <hashTree/>
        <ResultCollector guiclass="SummaryReport" testclass="ResultCollector" testname="Summary Report" enabled="true">
          <boolProp name="ResultCollector.error_logging">false</boolProp>
          <objProp>
            <name>saveConfig</name>
            <value class="SampleSaveConfiguration">
              <time>true</time>
              <latency>true</latency>
              <timestamp>true</timestamp>
              <success>true</success>
              <label>true</label>
              <code>true</code>
              <message>true</message>
              <threadName>true</threadName>
              <dataType>true</dataType>
              <encoding>false</encoding>
              <assertions>true</assertions>
              <subresults>true</subresults>
              <responseData>false</responseData>
              <samplerData>false</samplerData>
              <xml>false</xml>
              <fieldNames>false</fieldNames>
              <responseHeaders>false</responseHeaders>
              <requestHeaders>false</requestHeaders>
              <responseDataOnError>false</responseDataOnError>
              <saveAssertionResultsFailureMessage>false</saveAssertionResultsFailureMessage>
              <assertionsResultsToSave>0</assertionsResultsToSave>
              <bytes>true</bytes>
              <threadCounts>true</threadCounts>
            </value>
          </objProp>
          <stringProp name="filename"></stringProp>
        </ResultCollector>
        <hashTree/>
        <ResultCollector guiclass="ViewResultsFullVisualizer" testclass="ResultCollector" testname="View Results Tree" enabled="true">
          <boolProp name="ResultCollector.error_logging">false</boolProp>
          <objProp>
            <name>saveConfig</name>
            <value class="SampleSaveConfiguration">
              <time>true</time>
              <latency>true</latency>
              <timestamp>true</timestamp>
              <success>true</success>
              <label>true</label>
              <code>true</code>
              <message>true</message>
              <threadName>true</threadName>
              <dataType>true</dataType>
              <encoding>false</encoding>
              <assertions>true</assertions>
              <subresults>true</subresults>
              <responseData>false</responseData>
              <samplerData>false</samplerData>
              <xml>false</xml>
              <fieldNames>false</fieldNames>
              <responseHeaders>false</responseHeaders>
              <requestHeaders>false</requestHeaders>
              <responseDataOnError>false</responseDataOnError>
              <saveAssertionResultsFailureMessage>false</saveAssertionResultsFailureMessage>
              <assertionsResultsToSave>0</assertionsResultsToSave>
              <bytes>true</bytes>
              <threadCounts>true</threadCounts>
            </value>
          </objProp>
          <stringProp name="filename"></stringProp>
        </ResultCollector>
        <hashTree/>
        <ResultCollector guiclass="GraphVisualizer" testclass="ResultCollector" testname="Graph Results" enabled="true">
          <boolProp name="ResultCollector.error_logging">false</boolProp>
          <objProp>
            <name>saveConfig</name>
            <value class="SampleSaveConfiguration">
              <time>true</time>
              <latency>true</latency>
              <timestamp>true</timestamp>
              <success>true</success>
              <label>true</label>
              <code>true</code>
              <message>true</message>
              <threadName>true</threadName>
              <dataType>true</dataType>
              <encoding>false</encoding>
              <assertions>true</assertions>
              <subresults>true</subresults>
              <responseData>false</responseData>
              <samplerData>false</samplerData>
              <xml>false</xml>
              <fieldNames>false</fieldNames>
              <responseHeaders>false</responseHeaders>
              <requestHeaders>false</requestHeaders>
              <responseDataOnError>false</responseDataOnError>
              <saveAssertionResultsFailureMessage>false</saveAssertionResultsFailureMessage>
              <assertionsResultsToSave>0</assertionsResultsToSave>
              <bytes>true</bytes>
              <threadCounts>true</threadCounts>
            </value>
          </objProp>
          <stringProp name="filename"></stringProp>
        </ResultCollector>
        <hashTree/>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
"""

jdbc_req = """
        <JDBCSampler guiclass="TestBeanGUI" testclass="JDBCSampler" testname="%(qtype)s %(qname)s" enabled="true">
          <stringProp name="dataSource">hs2_%(qtype)s</stringProp>
          <stringProp name="query"><![CDATA[
          %(qtext)s
          ]]>
          </stringProp>
          <stringProp name="queryArguments"></stringProp>
          <stringProp name="queryArgumentsTypes"></stringProp>
          <stringProp name="queryTimeout"></stringProp>
          <stringProp name="queryType">Select Statement</stringProp>
          <stringProp name="resultSetHandler">Store as String</stringProp>
          <stringProp name="resultVariable"></stringProp>
          <stringProp name="variableNames"></stringProp>
        </JDBCSampler>
"""

def main(argv):
    (opts, args) = getopt(argv, "u:t:n:")
    threads = 1
    repeats = 1
    jdbc = "jdbc:hive2://localhost:10000/"
    for k,v in opts:
        if(k == "-u"):
            jdbc = v
        if(k == "-t"):
            threads = int(v)
        if(k == "-n"):
            repeats = int(v)
    tpcds_jdbc = jdbc + "tpcds5_bin_partitioned_orc_200";
    tpch_jdbc = jdbc + "tpch_orc_flat_1000";

    queries = []
    queries += [("tpcds", v) for v in glob("queries/tpc-ds/*.sql")]
    queries += [("tpch", v) for v in glob("queries/tpc-h/*.sql")]

    jdbc_queries = []
    for (qtype, q) in queries:
        qtext = open(q).read()
        if (len(qtext.split(";")) > 2):
            sys.stderr.write("Cannot load " + q + " too many queries in one file")
            continue
        qtext = qtext.replace(";","")
        qname = basename(q).replace(".sql","")
        jdbc_queries.append(jdbc_req % { "qname" : qname, "qtext" : qtext, "qtype" : qtype })
    args = {
        "jdbc_tpcds" : tpcds_jdbc,
        "jdbc_tpch" : tpch_jdbc,
        "threads" : threads,
        "repeats" : repeats,
        "jdbc_queries" : "<hashTree/>\n".join(jdbc_queries)
    }
    print testplan % args

if __name__ == "__main__":
    main(sys.argv[1:])
