#!/bin/bash
#脚本用法:ad_hdfs_to_ods.sh all 2023-05-28

APP=ad

if [ -n "$2" ] ;then
   do_date=$2
else
   do_date=`date -d '-1 day' +%F`
fi

#声明一个Map结构，保存ods表名与origin_data路径的映射关系
declare -A tableToPath
tableToPath["ods_ads_info_full"]="/origin_data/ad/db/ads_full"
tableToPath["ods_platform_info_full"]="/origin_data/ad/db/platform_info_full"
tableToPath["ods_product_info_full"]="/origin_data/ad/db/product_full"
tableToPath["ods_ads_platform_full"]="/origin_data/ad/db/ads_platform_full"
tableToPath["ods_server_host_full"]="/origin_data/ad/db/server_host_full"
tableToPath["ods_ad_log_inc"]="/origin_data/ad/log/ad_log"

load_data(){
    sql=""
    for i in $*; do
        #判断路径是否存在
        hadoop fs -test -e ${tableToPath["$i"]}/$do_date
        #路径存在方可装载数据
        if [[ $? = 0 ]]; then
            sql=$sql"load data inpath '${tableToPath["$i"]}/$do_date' overwrite into table ${APP}.$i partition(dt='$do_date');"
        fi
    done
    hive -e "$sql"
}

case $1 in
    "ods_ads_info_full")
        load_data "ods_ads_info_full"
    ;;
    "ods_platform_info_full")
        load_data "ods_platform_info_full"
    ;;
    "ods_product_info_full")
        load_data "ods_product_info_full"
    ;;
    "ods_ads_platform_full")
        load_data "ods_ads_platform_full"
    ;;
    "ods_server_host_full")
        load_data "ods_server_host_full"
    ;;
    "ods_ad_log_inc")
        load_data "ods_ad_log_inc"
    ;;
    "all")
        load_data "ods_ads_info_full" "ods_platform_info_full" "ods_product_info_full" "ods_ads_platform_full" "ods_server_host_full" "ods_ad_log_inc"
    ;;
esac

