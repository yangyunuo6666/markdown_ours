#!/bin/bash
#必须在spark目录下执行
# 需要先开启hadoop、hive、clickhouse服务
# 执行：load_one_day_data.sh 2025-06-03

# --- 关键修复：安全函数重写 ---
safe_execute() {
    # 直接执行参数数组而非eval字符串
    echo "正在执行：$*"
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        echo "命令执行失败：$*"
        echo "错误代码：$status"
        exit $status
    fi
}


# --- 主脚本开始 ---
if [ $# -ne 1 ]; then
    echo "错误：请提供一个日期参数（格式：YYYY-MM-DD）"
    echo "用法：$0 <日期>"
    exit 1
fi

DATE="$1"

if ! [[ $DATE =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "错误：无效的日期格式，请使用 YYYY-MM-DD 格式"
    exit 1
fi

# 强制在指定目录执行 (替换成你的实际目录)
REQ_DIR="/opt/module/spark"
if [ "$(pwd)" != "$REQ_DIR" ]; then
    echo "错误：必须在目录 $REQ_DIR 下执行此脚本"
    echo "建议运行: cd $REQ_DIR && $0 $DATE"
    exit 1
fi


# --- 命令执行（使用安全方式）---
# 注意：不再使用引号包裹整个命令
safe_execute mysql_to_hdfs_full.sh all "$DATE"
safe_execute ad_hdfs_to_ods.sh all "$DATE"
safe_execute ad_ods_to_dim.sh all "$DATE"
safe_execute ad_ods_to_dwd.sh all "$DATE"

# --- 安全执行Spark命令 ---
# 直接作为参数数组传递，避免eval解析
safe_execute spark-submit \
  --class com.atguigu.ad.spark.HiveToClickhouse \
  --master yarn \
  ad_hive_to_clickhouse-1.0-SNAPSHOT-jar-with-dependencies.jar \
  --hive_db ad \
  --hive_table dwd_ad_event_inc \
  --hive_partition "$DATE" \
  --ck_url jdbc:clickhouse://hadoop102:8123/ad_report \
  --ck_table dwd_ad_event_inc \
  --batch_size 1000

echo "所有命令执行成功！"