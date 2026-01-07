@echo off
setlocal

echo ===================================
echo 名人动态追踪系统 - 部署脚本
echo ===================================
echo.

if "%1"=="github" (
    echo 部署到 GitHub Pages...
    cd frontend
    call npm install
    call npm run build
    echo.
    echo 前端构建完成
    echo 请推送代码到 GitHub，GitHub Actions 将自动部署
    
) else if "%1"=="docker" (
    echo 使用 Docker 部署...
    
    if not exist "backend\.env" (
        echo 错误: backend\.env 文件不存在
        echo 请先创建 .env 文件并配置 DEEPSEEK_API_KEY
        exit /b 1
    )
    
    echo 构建前端...
    cd frontend
    call npm install
    call npm run build
    cd ..
    
    echo 启动 Docker 容器...
    docker-compose up -d --build
    
    echo.
    echo 部署完成
    echo 前端: http://localhost
    echo 后端: http://localhost:8000
    echo API文档: http://localhost:8000/docs
    
) else (
    echo 用法: deploy.bat [github^|docker]
    echo.
    echo 选项:
    echo   github   - 部署前端到 GitHub Pages
    echo   docker   - 使用 Docker Compose 本地部署
    exit /b 1
)

endlocal
