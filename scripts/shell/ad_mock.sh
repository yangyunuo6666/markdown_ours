#!/bin/bash
# 广告数仓：一键生成数据脚本
for i in hadoop102 hadoop103
do
echo "========== $i =========="
        ssh $i "cd /opt/module/ad_mock ; java -jar /opt/module/ad_mock/NginxDataGenerator-1.0-SNAPSHOT-jar-with-dependencies.jar >/dev/null  2>&1 &"
done
