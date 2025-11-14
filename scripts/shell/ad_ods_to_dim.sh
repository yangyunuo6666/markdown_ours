#!/bin/bash
##DIM层数据装载脚本
#用法：ad_ods_to_dim.sh all 2025-05-28

APP=ad

# 如果是输入的日期按照取输入日期；如果没输入日期取当前时间的前一天
if [ -n "$2" ] ;then
    do_date=$2
else 
    do_date=`date -d "-1 day" +%F`
fi

dim_platform_info_full="
insert overwrite table ${APP}.dim_platform_info_full partition (dt='$do_date')
select
    id,
    platform_name_en,
    platform_name_zh
from ${APP}.ods_platform_info_full
where dt = '$do_date';
"

dim_ads_info_full="
insert overwrite table ${APP}.dim_ads_info_full partition (dt='$do_date')
select
    ad.id,
    ad_name,
    product_id,
    name,
    price,
    material_id,
    material_url,
    group_id
from
(
    select
        id,
        ad_name,
        product_id,
        material_id,
        group_id,
        material_url
    from ${APP}.ods_ads_info_full
    where dt = '$do_date'
) ad
left join
(
    select
        id,
        name,
        price
    from ${APP}.ods_product_info_full
    where dt = '$do_date'
) pro
on ad.product_id = pro.id;
"

case $1 in
"dim_ads_info_full")
    hive -e "$dim_ads_info_full"
;;
"dim_platform_info_full")
    hive -e "$dim_platform_info_full"
;;
"all")
    hive -e "$dim_ads_info_full$dim_platform_info_full"
;;
esac

