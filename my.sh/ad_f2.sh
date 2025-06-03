#!/bin/bash
#Flume的启停脚本
case $1 in
"start")
        echo " --------启动 hadoop104 日志数据flume-------"
        ssh hadoop104 "nohup /opt/module/flume/bin/flume-ng agent -n a1 -c /opt/module/flume/conf -f /opt/module/flume/job/ad_kafka_to_hdfs.conf >/dev/null 2>&1 &"
;;
"stop")

        echo " --------停止 hadoop104 日志数据flume-------"
        ssh hadoop104 "ps -ef | grep ad_kafka_to_hdfs | grep -v grep |awk '{print \$2}' | xargs -n1 kill"
;;
esac
