#!/bin/bash

case $1 in
"start"){
        echo ================== 启动 Kafka集群 ==================

        #启动 Zookeeper集群
        zk.sh start

        #启动 Kafka采集集群
        kfk.sh start

        };;
"stop"){
        echo ================== 停止 Kafka集群 ==================

        #停止 Kafka采集集群
        kfk.sh stop

		#循环直至 Kafka 集群进程全部停止
		kafka_count=$(xcall jps | grep Kafka | wc -l)
		while [ $kafka_count -gt 0 ]
		do
			sleep 1
			kafka_count=$(xcall | grep Kafka | wc -l)
            echo "当前未停止的 Kafka 进程数为 $kafka_count"
		done

        #停止 Zookeeper集群
        zk.sh stop
};;
esac
