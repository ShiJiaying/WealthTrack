# 部署指南

本项目支持多种部署方式，包括 GitHub Pages、Docker、Railway、Render 等。

## 目录

- [快速部署](#快速部署)
- [GitHub Pages 部署（前端）](#github-pages-部署)
- [Docker 部署（完整）](#docker-部署)
- [Railway 部署](#railway-部署)
- [Render 部署](#render-部署)
- [Vercel 部署](#vercel-部署)
- [本地开发](#本地开发)

---

## 快速部署

### 使用部署脚本

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh [github|docker|railway|render]
```

**Windows:**
```bash
deploy.bat [github|docker]
```

---

## GitHub Pages 部署

### 前端部署到 GitHub Pages

1. **推送代码到 GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/trace_money.git
   git push -u origin main
   ```

2. **启用 GitHub Pages**
   - 进入仓库 Settings → Pages
   - Source 选择 "GitHub Actions"

3. **配置仓库名称**
   - 如果仓库名不是 `trace_money`，修改 `frontend/vite.config.ts` 中的 `base` 路径

4. **自动部署**
   - 推送代码后，GitHub Actions 会自动构建和部署
   - 访问 `https://YOUR_USERNAME.github.io/trace_money/`

### 后端部署

前端部署到 GitHub Pages 后，后端需要单独部署到其他服务（见下文）。

部署后，更新 `frontend/.env.production` 中的 API 地址：
```env
VITE_API_URL=https://your-backend-api.com
```

---

## Docker 部署

### 完整部署（前端 + 后端）

1. **准备环境**
   ```bash
   # 安装 Docker 和 Docker Compose
   # Windows: https://docs.docker.com/desktop/install/windows-install/
   # Mac: https://docs.docker.com/desktop/install/mac-install/
   # Linux: https://docs.docker.com/engine/install/
   ```

2. **配置环境变量**
   ```bash
   cd backend
   cp .env.example .env
   # 编辑 .env，填入 DEEPSEEK_API_KEY
   ```

3. **构建前端**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

4. **启动服务**
   ```bash
   docker-compose up -d
   ```

5. **访问应用**
   - 前端: http://localhost
   - 后端: http://localhost:8000
   - API 文档: http://localhost:8000/docs

6. **查看日志**
   ```bash
   docker-compose logs -f
   ```

7. **停止服务**
   ```bash
   docker-compose down
   ```

---

## Railway 部署

Railway 提供免费额度，适合部署后端服务。

### 步骤

1. **安装 Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **登录**
   ```bash
   railway login
   ```

3. **初始化项目**
   ```bash
   railway init
   ```

4. **设置环境变量**
   ```bash
   railway variables set DEEPSEEK_API_KEY=your_api_key_here
   railway variables set DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
   ```

5. **部署**
   ```bash
   railway up
   ```

6. **获取 URL**
   ```bash
   railway domain
   ```

7. **更新前端配置**
   - 将获取的 URL 填入 `frontend/.env.production`

---

## Render 部署

Render 提供免费的 Web Service，适合部署后端。

### 步骤

1. **推送代码到 GitHub**

2. **在 Render 创建 Web Service**
   - 访问 https://render.com/
   - 点击 "New +" → "Web Service"
   - 连接 GitHub 仓库

3. **配置服务**
   - Name: `celebrity-tracker-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && python main.py`

4. **设置环境变量**
   - `DEEPSEEK_API_KEY`: 你的 API Key
   - `DEEPSEEK_API_URL`: `https://api.deepseek.com/v1/chat/completions`
   - `HOST`: `0.0.0.0`
   - `PORT`: `8000`

5. **部署**
   - 点击 "Create Web Service"
   - 等待部署完成

6. **获取 URL**
   - 复制 Render 提供的 URL（如 `https://celebrity-tracker-backend.onrender.com`）

7. **更新前端配置**
   - 将 URL 填入 `frontend/.env.production`

---

## Vercel 部署

Vercel 适合部署 Serverless 后端（有限制）。

### 步骤

1. **安装 Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **登录**
   ```bash
   vercel login
   ```

3. **部署**
   ```bash
   vercel
   ```

4. **设置环境变量**
   ```bash
   vercel env add DEEPSEEK_API_KEY
   ```

5. **生产部署**
   ```bash
   vercel --prod
   ```

**注意**: Vercel 的 Serverless 函数有执行时间限制（免费版 10 秒），可能不适合长时间运行的任务。

---

## 本地开发

### 追踪的名人

在 `backend/config.py` 中的 `TRACKED_FIGURES` 列表可以添加或修改追踪的名人：

```python
TRACKED_FIGURES = [
    {
        "name": "名字",
        "name_en": "English Name",
        "twitter": "twitter_handle",
        "keywords": ["关键词1", "关键词2"],
        "category": "分类"
    }
]
```

### 新闻源

在 `backend/config.py` 中的 `NEWS_FEEDS` 列表可以添加 RSS 新闻源：

```python
NEWS_FEEDS = [
    "https://example.com/rss",
]
```

### 抓取频率

在 `backend/scheduler.py` 中修改抓取间隔（默认30分钟）：

```python
trigger=IntervalTrigger(minutes=30)  # 修改这里
```

## 生产环境部署

### 使用 Docker（推荐）

创建 `docker-compose.yml`：

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    volumes:
      - ./data:/app/data
  
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

启动：
```bash
docker-compose up -d
```

### 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

## 数据备份

数据库文件位于 `backend/celebrity_tracker.db`，定期备份此文件即可。

## 监控与日志

- 后端日志：查看控制台输出
- 数据库查询：使用 SQLite 工具查看 `celebrity_tracker.db`
- API 文档：访问 http://localhost:8000/docs

## 常见问题

### Q: DeepSeek API 调用失败
A: 检查 API Key 是否正确，账户是否有余额

### Q: 抓取不到新闻
A: 检查 RSS 源是否可访问，关键词是否匹配

### Q: 前端无法连接后端
A: 检查后端是否启动，端口是否正确

## 扩展功能

### 添加 Twitter 数据源

1. 获取 Twitter API Bearer Token
2. 在 `.env` 中配置 `TWITTER_BEARER_TOKEN`
3. 在 `news_crawler.py` 中实现 Twitter 抓取逻辑

### 添加邮件通知

安装 `python-email` 库，在高影响力事件时发送邮件提醒

### 添加 Webhook

在检测到重要事件时，通过 Webhook 推送到其他系统


### 后端

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY
python main.py
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000

---

## 配置说明

### 环境变量

**后端 (`backend/.env`):**
```env
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
HOST=0.0.0.0
PORT=8000
```

**前端 (`frontend/.env.production`):**
```env
VITE_API_URL=https://your-backend-api.com
```

### 追踪的名人

在 `backend/config.py` 中的 `TRACKED_FIGURES` 列表可以添加或修改。

### 新闻源

在 `backend/config.py` 中的 `NEWS_FEEDS` 列表可以添加 RSS 源。

### 抓取频率

在 `backend/scheduler.py` 中修改（默认 30 分钟）：
```python
trigger=IntervalTrigger(minutes=30)
```

---

## 数据备份

数据库文件位于 `backend/celebrity_tracker.db`，定期备份此文件。

```bash
# 备份
cp backend/celebrity_tracker.db backup/celebrity_tracker_$(date +%Y%m%d).db

# 恢复
cp backup/celebrity_tracker_20240107.db backend/celebrity_tracker.db
```

---

## 监控与日志

### 查看日志

**Docker:**
```bash
docker-compose logs -f backend
```

**本地:**
查看控制台输出

### 数据库查询

```bash
cd backend
python stats.py
```

### API 文档

访问 http://your-backend-url/docs

---

## 常见问题

### Q: GitHub Pages 部署后 API 调用失败
A: 需要单独部署后端，并在 `frontend/.env.production` 中配置后端 URL

### Q: Docker 容器无法启动
A: 检查 `.env` 文件是否存在，端口是否被占用

### Q: DeepSeek API 调用失败
A: 检查 API Key 是否正确，账户是否有余额

### Q: 抓取不到新闻
A: 检查 RSS 源是否可访问，网络连接是否正常

### Q: Railway/Render 免费额度用完
A: 考虑升级到付费计划，或使用其他服务

---

## 性能优化

### 数据库优化

```bash
# 清理旧数据（保留最近 30 天）
cd backend
python -c "
from database import SessionLocal, NewsItem, Analysis
from datetime import datetime, timedelta
db = SessionLocal()
cutoff = datetime.utcnow() - timedelta(days=30)
db.query(NewsItem).filter(NewsItem.created_at < cutoff).delete()
db.query(Analysis).filter(Analysis.created_at < cutoff).delete()
db.commit()
print('清理完成')
"
```

### 缓存配置

在 nginx.conf 中已配置静态资源缓存。

### CDN 加速

可以使用 Cloudflare 等 CDN 服务加速访问。

---

## 安全建议

1. **保护 API Key**: 不要将 `.env` 文件提交到 Git
2. **使用 HTTPS**: 生产环境必须使用 HTTPS
3. **限流**: 在 nginx 中配置请求限流
4. **定期更新**: 及时更新依赖包
5. **备份数据**: 定期备份数据库

---

## 扩展功能

### 添加邮件通知

安装依赖:
```bash
pip install python-email
```

在高影响力事件时发送邮件提醒。

### 添加 Webhook

在检测到重要事件时，通过 Webhook 推送到其他系统（如 Slack、Discord）。

### 添加更多数据源

在 `backend/news_crawler.py` 中添加更多抓取逻辑。

---

## 技术支持

如有问题，请查看：
- [README.md](README.md) - 项目说明
- [USAGE.md](USAGE.md) - 使用指南
- GitHub Issues - 提交问题

---

## 许可证

本项目仅供学习和研究使用。
