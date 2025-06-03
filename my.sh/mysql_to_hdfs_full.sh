#!/bin/bash
# 数据同步脚本，用于将MySQL中的数据同步到HDFS中
#mysql_to_hdfs_full.sh all 2025-05-28
# 使用datax工具进行数据同步
DATAX_HOME=/opt/module/datax

# 如果传入日期则do_date等于传入的日期，否则等于前一天日期
if [ -n "$2" ]; then
    do_date=$2
else
    do_date=`date -d "-1 day" +%F`
fi

# 处理目标路径，此处的处理逻辑是，如果目标路径不存在，则创建；若存在，则清空，目的是保证同步任务可重复执行
handle_targetdir() {
    hadoop fs -test -e $1
    if [[ $? -eq 1 ]]; then
        echo "路径$1不存在，正在创建......"
        hadoop fs -mkdir -p $1
    else
        echo "路径$1已经存在"
        fs_count=$(hadoop fs -count $1)
        content_size=$(echo $fs_count | awk '{print $3}')
        if [[ $content_size -eq 0 ]]; then
            echo "路径$1为空"
        else
            echo "路径$1不为空，正在清空......"
            hadoop fs -rm -r -f $1/*
        fi
    fi
}

# 数据同步
# 参数：arg1-datax 配置文件路径;arg2-源数据所在路径
import_data() {
    handle_targetdir $2
    python $DATAX_HOME/bin/datax.py -p"-Dtargetdir=$2" $1
}

case $1 in
"product")
    import_data /opt/module/datax/job/import/ad.product.json /origin_data/ad/db/product_full/$do_date
    ;;
"ads")
    import_data /opt/module/datax/job/import/ad.ads.json /origin_data/ad/db/ads_full/$do_date
    ;;
"server_host")
    import_data /opt/module/datax/job/import/ad.server_host.json /origin_data/ad/db/server_host_full/$do_date
    ;;
"ads_platform")
    import_data /opt/module/datax/job/import/ad.ads_platform.json /origin_data/ad/db/ads_platform_full/$do_date
    ;;
"platform_info")
    import_data /opt/module/datax/job/import/ad.platform_info.json /origin_data/ad/db/platform_info_full/$do_date
    ;;
"all")
    import_data /opt/module/datax/job/import/ad.product.json /origin_data/ad/db/product_full/$do_date
    import_data /opt/module/datax/job/import/ad.ads.json /origin_data/ad/db/ads_full/$do_date
    import_data /opt/module/datax/job/import/ad.server_host.json /origin_data/ad/db/server_host_full/$do_date
    import_data /opt/module/datax/job/import/ad.ads_platform.json /origin_data/ad/db/ads_platform_full/$do_date
    import_data /opt/module/datax/job/import/ad.platform_info.json /origin_data/ad/db/platform_info_full/$do_date
    ;;
esac
