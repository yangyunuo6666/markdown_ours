#!/bin/bash
#ip&uA数据装载脚本，数据来自ods_ad_log_inc
#用法：ad_ods_to_dwd.sh all 2025-05-28

APP=ad

# 如果是输入的日期按照取输入日期；如果没输入日期取当前时间的前一天
if [ -n "$2" ] ;then
    do_date=$2
else 
    do_date=`date -d "-1 day" +%F`
fi

dwd_ad_event_inc="
set hive.vectorized.execution.enabled=false;
--初步解析
create temporary table coarse_parsed_log
as
select
    parse_url('http://www.example.com' || request_uri, 'QUERY', 't') event_time,
    split(parse_url('http://www.example.com' || request_uri, 'PATH'), '/')[3] event_type,
    parse_url('http://www.example.com' || request_uri, 'QUERY', 'id') ad_id,
    split(parse_url('http://www.example.com' || request_uri, 'PATH'), '/')[2] platform,
    parse_url('http://www.example.com' || request_uri, 'QUERY', 'ip') client_ip,
    reflect('java.net.URLDecoder', 'decode', parse_url('http://www.example.com'||request_uri,'QUERY','ua'), 'utf-8') client_ua,
    parse_url('http://www.example.com'||request_uri,'QUERY','os_type') client_os_type,
    parse_url('http://www.example.com'||request_uri,'QUERY','device_id') client_device_id
from ${APP}.ods_ad_log_inc
where dt='$do_date';
--进一步解析ip和ua
create temporary table fine_parsed_log
as
select
    event_time,
    event_type,
    ad_id,
    platform,
    client_ip,
    client_ua,
    client_os_type,
    client_device_id,
    ${APP}.parse_ip('hdfs://hadoop102:8020/ip2region/ip2region.xdb',client_ip) region_struct,
    if(client_ua != '',${APP}.parse_ua(client_ua),null) ua_struct
from coarse_parsed_log;
--高速访问ip
create temporary table high_speed_ip
as
select
    distinct client_ip
from
(
    select
        event_time,
        client_ip,
        ad_id,
        count(1) over(partition by client_ip,ad_id order by cast(event_time as bigint) range between 300000 preceding and current row) event_count_last_5min
    from coarse_parsed_log
)t1
where event_count_last_5min>100;
--周期访问ip
create temporary table cycle_ip
as
select
    distinct client_ip
from
(
    select
        client_ip,
        ad_id,
        s
    from
    (
        select
            event_time,
            client_ip,
            ad_id,
            sum(num) over(partition by client_ip,ad_id order by event_time) s
        from
        (
            select
                event_time,
                client_ip,
                ad_id,
                time_diff,
                if(lag(time_diff,1,0) over(partition by client_ip,ad_id order by event_time)!=time_diff,1,0) num
            from
            (
                select
                    event_time,
                    client_ip,
                    ad_id,
                    lead(event_time,1,0) over(partition by client_ip,ad_id order by event_time)-event_time time_diff
                from coarse_parsed_log
            )t1
        )t2
    )t3
    group by client_ip,ad_id,s
    having count(*)>=5
)t4;
--高速访问设备
create temporary table high_speed_device
as
select
    distinct client_device_id
from
(
    select
        event_time,
        client_device_id,
        ad_id,
        count(1) over(partition by client_device_id,ad_id order by cast(event_time as bigint) range between 300000 preceding and current row) event_count_last_5min
    from coarse_parsed_log
    where client_device_id != ''
)t1
where event_count_last_5min>100;
--周期访问设备
create temporary table cycle_device
as
select
    distinct client_device_id
from
(
    select
        client_device_id,
        ad_id,
        s
    from
    (
        select
            event_time,
            client_device_id,
            ad_id,
            sum(num) over(partition by client_device_id,ad_id order by event_time) s
        from
        (
            select
                event_time,
                client_device_id,
                ad_id,
                time_diff,
                if(lag(time_diff,1,0) over(partition by client_device_id,ad_id order by event_time)!=time_diff,1,0) num
            from
            (
                select
                    event_time,
                    client_device_id,
                    ad_id,
                    lead(event_time,1,0) over(partition by client_device_id,ad_id order by event_time)-event_time time_diff
                from coarse_parsed_log
                where client_device_id != ''
            )t1
        )t2
    )t3
    group by client_device_id,ad_id,s
    having count(*)>=5
)t4;
--维度退化
insert overwrite table ${APP}.dwd_ad_event_inc partition (dt='$do_date')
select
    event_time,
    event_type,
    event.ad_id,
    ad_name,
    product_id,
    product_name,
    product_price,
    material_id,
    material_url,
    group_id,
    plt.id,
    platform_name_en,
    platform_name_zh,
    region_struct.country,
    region_struct.area,
    region_struct.province,
    region_struct.city,
    event.client_ip,
    event.client_device_id,
    if(event.client_os_type!='',event.client_os_type,ua_struct.os),
    nvl(ua_struct.osVersion,''),
    nvl(ua_struct.browser,''),
    nvl(ua_struct.browserVersion,''),
    event.client_ua,
    if(coalesce(pattern,hsi.client_ip,ci.client_ip,hsd.client_device_id,cd.client_device_id) is not null,true,false)
from fine_parsed_log event
left join ${APP}.dim_crawler_user_agent crawler on event.client_ua regexp crawler.pattern
left join high_speed_ip hsi on event.client_ip = hsi.client_ip
left join cycle_ip ci on event.client_ip = ci.client_ip
left join high_speed_device hsd on event.client_device_id = hsd.client_device_id
left join cycle_device cd on event.client_device_id = cd.client_device_id
left join
(
    select
        ad_id,
        ad_name,
        product_id,
        product_name,
        product_price,
        material_id,
        material_url,
        group_id
    from ${APP}.dim_ads_info_full
    where dt='$do_date'
)ad
on event.ad_id=ad.ad_id
left join
(
    select
        id,
        platform_name_en,
        platform_name_zh
    from ${APP}.dim_platform_info_full
    where dt='$do_date'
)plt
on event.platform=plt.platform_name_en;
"

case $1 in
"dwd_ad_event_inc")
    hive -e "$dwd_ad_event_inc"
;;
"all")
    hive -e "$dwd_ad_event_inc"
;;
esac

