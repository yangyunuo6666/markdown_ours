#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DWD层数据装载脚本，数据来自ods_ad_log_inc
用法: python ad_ods_to_dwd.py [dwd_ad_event_inc|all] [date]
"""

import argparse
import logging
import subprocess
import sys
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 配置
APP = "ad"


def run_hive_query(query, timeout=3600):
    """执行Hive查询"""
    logger.info("执行Hive查询")
    
    try:
        result = subprocess.run(
            ["hive", "-e", query],
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        logger.debug(f"Hive输出: {result.stdout}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Hive查询失败: {e.stderr}")
        return False, e.stderr
    except subprocess.TimeoutExpired:
        logger.error("Hive查询超时")
        return False, "Hive查询超时"


def dwd_ad_event_inc(do_date):
    """执行DWD层数据装载"""
    query = f"""
set hive.vectorized.execution.enabled=false;
-- 初步解析
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
from {APP}.ods_ad_log_inc
where dt='{do_date}';

-- 进一步解析ip和ua
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
    {APP}.parse_ip('hdfs://hadoop102:8020/ip2region/ip2region.xdb',client_ip) region_struct,
    if(client_ua != '',{APP}.parse_ua(client_ua),null) ua_struct
from coarse_parsed_log;

-- 高速访问ip
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

-- 周期访问ip
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

-- 高速访问设备
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

-- 周期访问设备
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

-- 维度退化
insert overwrite table {APP}.dwd_ad_event_inc partition (dt='{do_date}')
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
left join {APP}.dim_crawler_user_agent crawler on event.client_ua regexp crawler.pattern
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
    from {APP}.dim_ads_info_full
    where dt='{do_date}'
)ad
on event.ad_id=ad.ad_id
left join
(
    select
        id,
        platform_name_en,
        platform_name_zh
    from {APP}.dim_platform_info_full
    where dt='{do_date}'
)plt
on event.platform=plt.platform_name_en;
"""
    
    return run_hive_query(query)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="DWD层数据装载工具")
    parser.add_argument(
        "action", 
        choices=["dwd_ad_event_inc", "all"],
        help="操作: dwd_ad_event_inc-处理事件数据, all-处理所有数据"
    )
    parser.add_argument(
        "date", 
        nargs="?", 
        help="处理日期，格式为YYYY-MM-DD，默认为前一天"
    )
    
    args = parser.parse_args()
    
    # 处理日期
    if args.date:
        do_date = args.date
    else:
        do_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    logger.info(f"开始DWD层数据装载，日期: {do_date}")
    
    # 执行处理
    if args.action == "dwd_ad_event_inc" or args.action == "all":
        success, output = dwd_ad_event_inc(do_date)
        if not success:
            logger.error("DWD层数据装载失败")
            sys.exit(1)
    
    logger.info("DWD层数据装载完成")
    sys.exit(0)


if __name__ == "__main__":
    main()