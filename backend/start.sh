#!/bin/bash

echo "检查并安装 Python 依赖..."
pip install -r requirements.txt

echo "启动后端服务..."
python main.py
