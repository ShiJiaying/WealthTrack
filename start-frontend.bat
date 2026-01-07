@echo off
echo 启动前端服务...
cd frontend
call npm install
call npm run dev
pause
