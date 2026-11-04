#!/bin/bash
# Example Hadoop Streaming job; adjust jar and HDFS paths for your cluster.
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /user/student/online_retail.csv \
  -output /user/student/output_country_sales \
  -mapper mapper.py -reducer reducer.py \
  -file mapper.py -file reducer.py
