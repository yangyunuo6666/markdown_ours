#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL到HDFS全量数据同步脚本
用法: python mysql_to_hdfs_full.py [table_name|all] [date]
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
DATAX_HOME = "/opt/module/datax"
APP = "ad"

# 表配置映射
TABLE_CONFIGS = {
    "product": {
        "json": f"{DATAX_HOME}/job/import/ad.product.json",
        "hdfs_path": "/origin_data/ad/db/product_full"
    },
    "ads": {
        "json": f"{DATAX_HOME}/job/import/ad.ads.json",
        "hdfs_path": "/origin_data/ad/db/ads_full"
    },
    "server_host": {
        "json": f"{DATAX_HOME}/job/import/ad.server_host.json",
        "hdfs_path": "/origin_data/ad/db/server_host_full"
    },
    "ads_platform": {
        "json": f"{DATAX_HOME}/job/import/ad.ads_platform.json",
        "hdfs_path": "/origin_data/ad/db/ads_platform_full"
    },
    "platform_info": {
        "json": f"{DATAX_HOME}/job/import/ad.platform_info.json",
        "hdfs_path": "/origin_data/ad/db/platform_info_full"
    }
}


def run_command(cmd, timeout=3600):
    """执行命令并返回结果"""
    logger.info(f"执行命令: {cmd}")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            timeout=timeout
        )
        logger.debug(f"命令输出: {result.stdout}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"命令执行失败: {e.stderr}")
        return False, e.stderr
    except subprocess.TimeoutExpired:
        logger.error("命令执行超时")
        return False, "命令执行超时"


def hdfs_test_path(hdfs_path):
    """检查HDFS路径是否存在"""
    cmd = f"hadoop fs -test -e {hdfs_path}"
    success, _ = run_command(cmd)
    return success


def hdfs_mkdir(hdfs_path):
    """创建HDFS目录"""
    cmd = f"hadoop fs -mkdir -p {hdfs_path}"
    return run_command(cmd)


def hdfs_count(hdfs_path):
    """获取HDFS目录内容大小"""
    cmd = f"hadoop fs -count {hdfs_path}"
    success, output = run_command(cmd)
    
    if success and output:
        # count命令返回: 文件数 目录数 内容大小(字节) 路径
        parts = output.strip().split()
        if len(parts) >= 3:
            return int(parts[2])  # 返回内容大小(字节)
    
    return 0


def hdfs_clean_directory(hdfs_path):
    """清空HDFS目录"""
    cmd = f"hadoop fs -rm -r -f {hdfs_path}/*"
    return run_command(cmd)


def handle_targetdir(hdfs_path):
    """处理目标路径"""
    logger.info(f"检查路径: {hdfs_path}")
    
    if not hdfs_test_path(hdfs_path):
        logger.info(f"路径 {hdfs_path} 不存在，正在创建...")
        success, _ = hdfs_mkdir(hdfs_path)
        if not success:
            return False
    else:
        logger.info(f"路径 {hdfs_path} 已存在")
        content_size = hdfs_count(hdfs_path)
        
        if content_size == 0:
            logger.info(f"路径 {hdfs_path} 为空")
        else:
            logger.info(f"路径 {hdfs_path} 不为空，正在清空...")
            success, _ = hdfs_clean_directory(hdfs_path)
            if not success:
                return False
    
    return True


def import_data(table_name, do_date):
    """执行数据导入"""
    if table_name not in TABLE_CONFIGS:
        logger.error(f"未知的表名: {table_name}")
        return False
    
    config = TABLE_CONFIGS[table_name]
    json_path = config["json"]
    hdfs_base_path = config["hdfs_path"]
    full_hdfs_path = f"{hdfs_base_path}/{do_date}"
    
    # 处理目标目录
    if not handle_targetdir(full_hdfs_path):
        logger.error(f"处理目标目录失败: {full_hdfs_path}")
        return False
    
    # 执行DataX任务
    cmd = f"python {DATAX_HOME}/bin/datax.py -p'-Dtargetdir={full_hdfs_path}' {json_path}"
    success, output = run_command(cmd, timeout=7200)  # 2小时超时
    
    if success:
        logger.info(f"表 {table_name} 同步成功")
        return True
    else:
        logger.error(f"表 {table_name} 同步失败: {output}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="MySQL到HDFS全量数据同步工具")
    parser.add_argument(
        "table", 
        choices=list(TABLE_CONFIGS.keys()) + ["all"],
        help="要同步的表名或'all'同步所有表"
    )
    parser.add_argument(
        "date", 
        nargs="?", 
        help="同步日期，格式为YYYY-MM-DD，默认为前一天"
    )
    
    args = parser.parse_args()
    
    # 处理日期
    if args.date:
        do_date = args.date
    else:
        do_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    logger.info(f"开始数据同步，日期: {do_date}")
    
    # 执行同步
    if args.table == "all":
        tables = list(TABLE_CONFIGS.keys())
        success = True
        for table in tables:
            if not import_data(table, do_date):
                success = False
                logger.error(f"表 {table} 同步失败，停止后续同步")
                break
    else:
        success = import_data(args.table, do_date)
    
    # 输出最终结果
    if success:
        logger.info("所有数据同步完成")
        sys.exit(0)
    else:
        logger.error("数据同步过程中出现错误")
        sys.exit(1)


if __name__ == "__main__":
    main()