# 快速开始指南

## 5 分钟快速部署

### 步骤 1: 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/trace_money.git
cd trace_money
```

### 步骤 2: 配置 API Key

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件，填入你的 DeepSeek API Key：
```env
DEEPSEEK_API_KEY=sk-your-api-key-here
```

获取 API Key: https://platform.deepseek.com/

### 步骤 3: 启动后端

```bash
pip install -r requirements.txt
python main.py
```

看到 "系统启动完成！" 表示成功。

### 步骤 4: 启动前端

打开新终端：

```bash
cd frontend
npm install
npm run dev
```

### 步骤 5: 访问应用

打开浏览器访问: http://localhost:3000

---

## 使用 Docker（推荐）

### 一键启动

**Windows:**
```bash
deploy.bat docker
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh docker
```

访问: http://localhost

---

## 部署到云端

### GitHub Pages（前端）

1. 推送代码到 GitHub
2. 在仓库设置中启用 GitHub Pages
3. 选择 "GitHub Actions" 作为源
4. 自动部署完成

### Railway（后端）

```bash
npm i -g @railway/cli
railway login
railway init
railway variables set DEEPSEEK_API_KEY=your_key
railway up
```

### Render（后端）

1. 访问 https://render.com/
2. 连接 GitHub 仓库
3. 选择 "Web Service"
4. 设置环境变量 `DEEPSEEK_API_KEY`
5. 点击部署

---

## 验证部署

### 检查后端

访问: http://localhost:8000/docs

应该看到 API 文档页面。

### 检查前端

访问: http://localhost:3000

应该看到仪表盘页面。

### 检查数据

```bash
cd backend
python stats.py
```

应该看到新闻和分析统计。

---

## 常见问题

### Q: 后端启动失败
```bash
# 检查依赖
pip install -r requirements.txt

# 检查 API Key
python test_api_simple.py
```

### Q: 前端无法连接后端
```bash
# 确保后端在运行
# 检查端口 8000 是否被占用
```

### Q: 没有抓取到新闻
```bash
# 手动触发抓取
cd backend
python fetch_now.py
```

### Q: Docker 启动失败
```bash
# 检查 Docker 是否运行
docker --version

# 查看日志
docker-compose logs
```

---

## 下一步

- 📖 阅读 [使用指南](USAGE.md)
- 🚀 查看 [部署指南](DEPLOYMENT.md)
- ⚙️ 自定义 [配置文件](backend/config.py)

---

## 获取帮助

- 查看文档: [README.md](README.md)
- 提交问题: GitHub Issues
- 查看示例: [USAGE.md](USAGE.md)
