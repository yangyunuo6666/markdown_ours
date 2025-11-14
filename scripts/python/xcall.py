#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在集群所有节点上执行相同命令
用法: python xcall.py [command]
"""

import argparse
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
            check=True, # 如果命令执行失败，则抛出异常
            capture_output=True, # 捕获标准输出和标准错误
            text=True, # 将输出作为字符串处理
            timeout=300 
        )
        return host, result.stdout, None
    except subprocess.CalledProcessError as e:
        return host, None, f"命令执行失败: {e.stderr}"
    except subprocess.TimeoutExpired:
        return host, None, "命令执行超时"


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="在集群所有节点上执行相同命令")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="要执行的命令")
    
    args = parser.parse_args()
    
    if not args.command:
        print("错误: 需要提供要执行的命令")
        sys.exit(1)
    
    command = " ".join(args.command)
    print(f"将在所有节点上执行命令: {command}")
    
    # 使用线程池并行执行
    with ThreadPoolExecutor(max_workers=len(HOSTS)) as executor:
        # 提交所有任务
        future_to_host = {
            executor.submit(run_ssh_command, host, command): host 
            for host in HOSTS
        }
        
        # 收集并显示结果
        all_success = True
        for future in as_completed(future_to_host):
            host = future_to_host[future]
            try:
                host, output, error = future.result()
                print(f"\n--------- {host} ---------")
                if error:
                    print(f"错误: {error}")
                    all_success = False
                else:
                    print(output.strip())
            except Exception as e:
                print(f"\n--------- {host} ---------")
                print(f"执行异常: {e}")
                all_success = False
    
    sys.exit(0 if all_success else 1)


if __name__ == "__main__":
    main()