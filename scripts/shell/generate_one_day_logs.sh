#!/bin/bash
# 日志生成脚本：generate_logs.sh
# 功能：生成指定日期的日志数据
# 用法：generate_one_day_logs.sh 2025-06-03

# --- 参数检查 ---
if [ $# -ne 1 ]; then
    echo "错误：请提供一个日期参数（格式：YYYY-MM-DD）"
    echo "用法：$0 <日期>"
    exit 1
fi

DATE="$1"

# 日期格式校验
if ! [[ $DATE =~ ^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$ ]]; then
    echo "错误：无效的日期格式，请使用 YYYY-MM-DD 格式"
    exit 1
fi

# --- 配置文件路径 ---
CONFIG_FILE="/opt/module/ad_mock/nginxLogGen.setting"

# --- 服务控制函数 ---
# control_service() {
#     local service=$1
#     local action=$2
#     echo "[$(date '+%F %T')] ${action^} $service"
#     "$service.sh" "$action"
# }

# --- 修改配置文件 ---
modify_config() {
    echo "修改配置文件: $CONFIG_FILE"
    
    # 直接修改配置文件，不创建备份
    sed -i.bak -e "s/^startTime = .*/startTime = $DATE 00:00:00/" \
              -e "s/^endTime = .*/endTime = $DATE 23:59:59/" \
              "$CONFIG_FILE"
    
    # 验证修改
    echo "修改后的配置："
    grep -E '^(startTime|endTime)' "$CONFIG_FILE"
}

# --- 分发配置文件 ---
distribute_config() {
    echo "分发配置文件到集群节点"
    
    # 分发到 hadoop102
    scp "$CONFIG_FILE" hadoop102:"$CONFIG_FILE"
    
    # 分发到 hadoop103
    scp "$CONFIG_FILE" hadoop103:"$CONFIG_FILE"
}

# --- 主流程 ---
echo "===== 开始生成 $DATE 日志数据 ====="

# 启动基础服务
# control_service zk start
# control_service kfk start

# # 启动日志生成器
# control_service ad_f1 start
# control_service ad_f2 start 
# sleep 2

# 配置修改与分发
modify_config 
distribute_config
sleep 2

# 生成日志文件
echo "[$(date '+%F %T')] 生成日志数据"
ad_mock.sh
# sleep 7

# 关闭服务
#control_service ad_f1 stop
#control_service ad_f2 stop
# control_service kfk stop
# control_service zk stop

echo "===== 日志生成完成 ====="
echo "生成日期: $DATE"