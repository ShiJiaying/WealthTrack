#!/bin/bash

echo "=== 启动名人动态追踪系统 ==="

# 启动后端
echo "1. 启动后端服务..."
cd backend
# pip install -r requirements.txt > /dev/null 2>&1
python main.py &
BACKEND_PID=$!
echo "后端服务已启动 (PID: $BACKEND_PID)"

# 等待后端启动
echo "等待后端服务就绪..."
sleep 5

# 启动前端
echo "2. 启动前端服务..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "前端服务已启动 (PID: $FRONTEND_PID)"

echo ""
echo "=== 服务启动完成 ==="
echo "后端: http://localhost:8000"
echo "前端: http://localhost:3000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
wait
