@echo off
echo 启动后端服务...
cd backend
pip install -r requirements.txt
python main.py
pause
