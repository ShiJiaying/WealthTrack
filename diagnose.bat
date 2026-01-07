@echo off
echo ========================================
echo 系统诊断
echo ========================================
echo.

echo [1] 检查后端服务...
curl -s http://localhost:8000/ >nul 2>&1
if %errorlevel% equ 0 (
    echo    ✓ 后端服务正常运行
    curl -s http://localhost:8000/ 
) else (
    echo    ✗ 后端服务未运行
    echo    请先启动后端: cd backend ^&^& python main.py
)
echo.

echo [2] 检查前端服务...
curl -s http://localhost:3000/ >nul 2>&1
if %errorlevel% equ 0 (
    echo    ✓ 前端服务正常运行
) else (
    echo    ✗ 前端服务未运行
    echo    请先启动前端: cd frontend ^&^& npm run dev
)
echo.

echo [3] 测试 API 接口...
echo    测试 /api/news...
curl -s http://localhost:8000/api/news?limit=1
echo.
echo.

echo [4] 检查数据库...
if exist backend\celebrity_tracker.db (
    echo    ✓ 数据库文件存在
    cd backend
    python -c "import sqlite3; conn = sqlite3.connect('celebrity_tracker.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM news_items'); print('   新闻数量:', cursor.fetchone()[0]); cursor.execute('SELECT COUNT(*) FROM analyses'); print('   分析数量:', cursor.fetchone()[0])"
    cd ..
) else (
    echo    ✗ 数据库文件不存在
)
echo.

echo [5] 检查环境配置...
if exist backend\.env (
    echo    ✓ backend/.env 文件存在
) else (
    echo    ✗ backend/.env 文件不存在
    echo    请创建: cd backend ^&^& copy .env.example .env
)
echo.

echo ========================================
echo 诊断完成
echo ========================================
pause
