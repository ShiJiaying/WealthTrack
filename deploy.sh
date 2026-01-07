#!/bin/bash

echo "==================================="
echo "名人动态追踪系统 - 部署脚本"
echo "==================================="

# 检查参数
if [ "$1" == "github" ]; then
    echo "部署到 GitHub Pages..."
    cd frontend
    npm install
    npm run build
    echo "✓ 前端构建完成"
    echo "请推送代码到 GitHub，GitHub Actions 将自动部署"
    
elif [ "$1" == "docker" ]; then
    echo "使用 Docker 部署..."
    
    # 检查 .env 文件
    if [ ! -f "backend/.env" ]; then
        echo "❌ 错误: backend/.env 文件不存在"
        echo "请先创建 .env 文件并配置 DEEPSEEK_API_KEY"
        exit 1
    fi
    
    # 构建前端
    echo "构建前端..."
    cd frontend
    npm install
    npm run build
    cd ..
    
    # 启动 Docker
    echo "启动 Docker 容器..."
    docker-compose up -d --build
    
    echo "✓ 部署完成"
    echo "前端: http://localhost"
    echo "后端: http://localhost:8000"
    echo "API文档: http://localhost:8000/docs"
    
elif [ "$1" == "railway" ]; then
    echo "部署到 Railway..."
    echo "1. 安装 Railway CLI: npm i -g @railway/cli"
    echo "2. 登录: railway login"
    echo "3. 初始化: railway init"
    echo "4. 设置环境变量: railway variables set DEEPSEEK_API_KEY=your_key"
    echo "5. 部署: railway up"
    
elif [ "$1" == "render" ]; then
    echo "部署到 Render..."
    echo "1. 推送代码到 GitHub"
    echo "2. 在 Render 控制台连接 GitHub 仓库"
    echo "3. 选择 render.yaml 配置"
    echo "4. 设置环境变量 DEEPSEEK_API_KEY"
    echo "5. 点击部署"
    
else
    echo "用法: ./deploy.sh [github|docker|railway|render]"
    echo ""
    echo "选项:"
    echo "  github   - 部署前端到 GitHub Pages"
    echo "  docker   - 使用 Docker Compose 本地部署"
    echo "  railway  - 部署到 Railway"
    echo "  render   - 部署到 Render"
    exit 1
fi
