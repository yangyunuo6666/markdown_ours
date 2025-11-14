#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查看集群所有节点的JPS进程状态
用法: python jpsall.py
"""

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# 集群节点列表
HOSTS = ["hadoop102", "hadoop103", "hadoop104"]


def run_ssh_command(host, command):
    """在远程主机上执行命令并返回结果"""
    try:
        result = subprocess.run(
            ["ssh", host, command],
            check=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return host, result.stdout, None
    except subprocess.CalledProcessError as e:
        return host, None, f"命令执行失败: {e.stderr}"
    except subprocess.TimeoutExpired:
        return host, None, "命令执行超时"


def main():
    """主函数"""
    print("正在检查集群节点进程状态...")
    
    # 使用线程池并行执行
    with ThreadPoolExecutor(max_workers=len(HOSTS)) as executor:
        # 提交所有任务
        future_to_host = {
            executor.submit(run_ssh_command, host, "jps"): host 
            for host in HOSTS
        }
        
        # 收集并显示结果
        for future in as_completed(future_to_host):
            host = future_to_host[future]
            try:
                host, output, error = future.result()
                print(f"\n=============== {host} ===============")
                if error:
                    print(f"错误: {error}")
                else:
                    print(output.strip())
            except Exception as e:
                print(f"\n=============== {host} ===============")
                print(f"执行异常: {e}")


if __name__ == "__main__":
    main()