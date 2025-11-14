#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hadoop集群管理脚本
用法: python myhadoop.py [start|stop|status]
"""

import argparse
import logging
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Hadoop配置
HADOOP_HOME = "/opt/module/hadoop-3.1.3"
HOSTS = {
    "hdfs": "hadoop102",
    "yarn": "hadoop103",
    "historyserver": "hadoop102"
}


def run_ssh_command(host, command, timeout=60):
    """在远程主机上执行命令"""
    ssh_command = f"ssh {host} '{command}'"
    logger.info(f"在 {host} 上执行: {command}")
    
    try:
        result = subprocess.run(
            ssh_command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            timeout=timeout
        )
        logger.debug(f"命令输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"在 {host} 上执行命令失败: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        logger.error(f"在 {host} 上执行命令超时")
        return False


def start_cluster():
    """启动Hadoop集群"""
    logger.info("=================== 启动Hadoop集群 ===================")
    
    # 启动HDFS
    logger.info("--------------- 启动HDFS ---------------")
    success = run_ssh_command(
        HOSTS["hdfs"], 
        f"{HADOOP_HOME}/sbin/start-dfs.sh"
    )
    if not success:
        logger.error("启动HDFS失败")
        return False
    
    # 启动YARN
    logger.info("--------------- 启动YARN ---------------")
    success = run_ssh_command(
        HOSTS["yarn"], 
        f"{HADOOP_HOME}/sbin/start-yarn.sh"
    )
    if not success:
        logger.error("启动YARN失败")
        return False
    
    # 启动HistoryServer
    logger.info("--------------- 启动HistoryServer ---------------")
    success = run_ssh_command(
        HOSTS["historyserver"], 
        f"{HADOOP_HOME}/bin/mapred --daemon start historyserver"
    )
    if not success:
        logger.error("启动HistoryServer失败")
        return False
    
    logger.info("=================== Hadoop集群已启动 ===================")
    return True


def stop_cluster():
    """停止Hadoop集群"""
    logger.info("=================== 停止Hadoop集群 ===================")
    
    # 停止HistoryServer
    logger.info("--------------- 停止HistoryServer ---------------")
    run_ssh_command(
        HOSTS["historyserver"], 
        f"{HADOOP_HOME}/bin/mapred --daemon stop historyserver"
    )
    
    # 停止YARN
    logger.info("--------------- 停止YARN ---------------")
    run_ssh_command(
        HOSTS["yarn"], 
        f"{HADOOP_HOME}/sbin/stop-yarn.sh"
    )
    
    # 停止HDFS
    logger.info("--------------- 停止HDFS ---------------")
    success = run_ssh_command(
        HOSTS["hdfs"], 
        f"{HADOOP_HOME}/sbin/stop-dfs.sh"
    )
    
    if success:
        logger.info("=================== Hadoop集群已停止 ===================")
    else:
        logger.error("停止HDFS失败")
    
    return success


def check_cluster_status():
    """检查Hadoop集群状态"""
    logger.info("=================== 检查Hadoop集群状态 ===================")
    
    # 检查HDFS
    logger.info("--------------- 检查HDFS状态 ---------------")
    run_ssh_command(HOSTS["hdfs"], f"{HADOOP_HOME}/bin/hdfs dfsadmin -report")
    
    # 检查YARN
    logger.info("--------------- 检查YARN状态 ---------------")
    run_ssh_command(HOSTS["yarn"], f"{HADOOP_HOME}/bin/yarn node -list")
    
    logger.info("=================== 状态检查完成 ===================")
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Hadoop集群管理工具")
    parser.add_argument(
        "action", 
        choices=["start", "stop", "status"], 
        help="操作: start-启动集群, stop-停止集群, status-检查状态"
    )
    
    args = parser.parse_args()
    
    if args.action == "start":
        success = start_cluster()
    elif args.action == "stop":
        success = stop_cluster()
    else:
        success = check_cluster_status()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()