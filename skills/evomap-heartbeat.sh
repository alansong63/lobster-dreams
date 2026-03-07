#!/bin/bash
# EvoMap 自动心跳脚本
# 每 15 分钟发送一次心跳，保持节点在线

NODE_ID="node_alansong_1772770746"
NODE_SECRET="c6d158d83054815d1c8b3765634e8b62d58dc16ae121821992e4582c5889eb00"
LOG_FILE="/home/ubuntu/.openclaw/workspace/logs/evomap-heartbeat.log"

send_heartbeat() {
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    echo "[$timestamp] Sending heartbeat..." >> "$LOG_FILE"
    
    response=$(curl -s -X POST https://evomap.ai/a2a/heartbeat \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $NODE_SECRET" \
        -d "{\"node_id\": \"$NODE_ID\"}")
    
    status=$(echo "$response" | jq -r '.status // "error"')
    
    if [ "$status" = "ok" ]; then
        echo "[$timestamp] ✅ Heartbeat OK" >> "$LOG_FILE"
    else
        echo "[$timestamp] ❌ Heartbeat failed: $response" >> "$LOG_FILE"
    fi
}

# 如果是 systemd 服务模式，持续运行
if [ "$1" = "--daemon" ]; then
    echo "Starting EvoMap heartbeat daemon (every 15 minutes)..." >> "$LOG_FILE"
    while true; do
        send_heartbeat
        sleep 900  # 15 minutes
    done
else
    # 单次执行模式（用于 cron）
    send_heartbeat
fi
