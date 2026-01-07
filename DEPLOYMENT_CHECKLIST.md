# 部署检查清单

## 部署前准备

### ✅ 必需项

- [ ] 已获取 DeepSeek API Key
- [ ] 已安装 Git
- [ ] 已创建 GitHub 账号
- [ ] 已安装 Node.js 16+
- [ ] 已安装 Python 3.8+

### ✅ 可选项

- [ ] 已安装 Docker（用于 Docker 部署）
- [ ] 已注册 Railway/Render 账号（用于后端部署）

---

## GitHub Pages 部署清单

### 1. 准备代码

- [ ] 克隆或下载项目
- [ ] 配置 `backend/.env` 文件
- [ ] 测试本地运行正常

### 2. 推送到 GitHub

```bash
# 初始化 Git 仓库
git init
git add .
git commit -m "Initial commit"

# 创建 GitHub 仓库后
git remote add origin https://github.com/YOUR_USERNAME/trace_money.git
git branch -M main
git push -u origin main
```

- [ ] 代码已推送到 GitHub
- [ ] 仓库设置为 Public（或 Private with GitHub Pro）

### 3. 配置 GitHub Pages

- [ ] 进入仓库 Settings → Pages
- [ ] Source 选择 "GitHub Actions"
- [ ] 等待 Actions 运行完成
- [ ] 访问 `https://YOUR_USERNAME.github.io/trace_money/`

### 4. 配置前端 API 地址

- [ ] 部署后端到 Railway/Render
- [ ] 获取后端 URL
- [ ] 更新 `frontend/.env.production`:
  ```env
  VITE_API_URL=https://your-backend-url.com
  ```
- [ ] 重新推送代码触发部署

---

## Railway 后端部署清单

### 1. 安装 CLI

```bash
npm i -g @railway/cli
```

- [ ] Railway CLI 已安装

### 2. 登录和初始化

```bash
railway login
railway init
```

- [ ] 已登录 Railway
- [ ] 项目已初始化

### 3. 配置环境变量

```bash
railway variables set DEEPSEEK_API_KEY=your_api_key_here
railway variables set DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
railway variables set HOST=0.0.0.0
railway variables set PORT=8000
```

- [ ] 环境变量已设置

### 4. 部署

```bash
railway up
```

- [ ] 部署成功
- [ ] 获取 URL: `railway domain`
- [ ] 测试 API: `https://your-app.railway.app/docs`

---

## Render 后端部署清单

### 1. 连接 GitHub

- [ ] 访问 https://render.com/
- [ ] 点击 "New +" → "Web Service"
- [ ] 连接 GitHub 仓库

### 2. 配置服务

- [ ] Name: `celebrity-tracker-backend`
- [ ] Environment: `Python 3`
- [ ] Build Command: `pip install -r backend/requirements.txt`
- [ ] Start Command: `cd backend && python main.py`

### 3. 设置环境变量

- [ ] `DEEPSEEK_API_KEY`: 你的 API Key
- [ ] `DEEPSEEK_API_URL`: `https://api.deepseek.com/v1/chat/completions`
- [ ] `HOST`: `0.0.0.0`
- [ ] `PORT`: `8000`

### 4. 部署

- [ ] 点击 "Create Web Service"
- [ ] 等待部署完成
- [ ] 测试 API: `https://your-app.onrender.com/docs`

---

## Docker 部署清单

### 1. 安装 Docker

- [ ] Docker 已安装
- [ ] Docker Compose 已安装

### 2. 配置环境

- [ ] 创建 `backend/.env` 文件
- [ ] 填入 `DEEPSEEK_API_KEY`

### 3. 构建前端

```bash
cd frontend
npm install
npm run build
cd ..
```

- [ ] 前端构建成功

### 4. 启动服务

```bash
docker-compose up -d
```

- [ ] 容器启动成功
- [ ] 访问 http://localhost
- [ ] 访问 http://localhost:8000/docs

---

## 部署后验证

### 前端验证

- [ ] 页面可以正常访问
- [ ] 仪表盘显示正常
- [ ] 新闻列表可以加载
- [ ] 分析列表可以加载
- [ ] 筛选功能正常
- [ ] 详情页可以打开

### 后端验证

- [ ] API 文档可以访问 (`/docs`)
- [ ] 健康检查正常 (`/`)
- [ ] 新闻接口返回数据 (`/api/news`)
- [ ] 分析接口返回数据 (`/api/analysis`)
- [ ] 仪表盘接口正常 (`/api/dashboard`)

### 功能验证

- [ ] 定时任务正常运行（查看日志）
- [ ] 新闻抓取正常
- [ ] AI 分析正常
- [ ] 数据库正常保存
- [ ] 评分计算正确

### 性能验证

- [ ] 页面加载速度 < 3 秒
- [ ] API 响应时间 < 1 秒
- [ ] 无明显错误日志
- [ ] 内存使用正常

---

## 常见问题排查

### 前端无法访问

- [ ] 检查 GitHub Actions 是否成功
- [ ] 检查 Pages 设置是否正确
- [ ] 检查 `vite.config.ts` 中的 `base` 路径

### API 调用失败

- [ ] 检查后端是否正常运行
- [ ] 检查 `.env.production` 中的 API URL
- [ ] 检查 CORS 配置
- [ ] 检查网络连接

### 后端启动失败

- [ ] 检查环境变量是否配置
- [ ] 检查依赖是否安装
- [ ] 检查端口是否被占用
- [ ] 查看错误日志

### 没有数据

- [ ] 手动触发抓取: `python fetch_now.py`
- [ ] 检查 API Key 是否有效
- [ ] 检查网络连接
- [ ] 查看抓取日志

### DeepSeek API 失败

- [ ] 检查 API Key 是否正确
- [ ] 检查账户余额
- [ ] 检查 API 限流
- [ ] 重新分析: `python reanalyze.py`

---

## 监控和维护

### 日常检查

- [ ] 每天检查系统运行状态
- [ ] 每周查看统计数据: `python stats.py`
- [ ] 每月备份数据库
- [ ] 定期更新依赖

### 数据维护

```bash
# 查看统计
python stats.py

# 清理旧数据（保留 30 天）
# 在 Python 中执行清理脚本

# 备份数据库
cp celebrity_tracker.db backup/celebrity_tracker_$(date +%Y%m%d).db
```

### 日志监控

```bash
# Docker 日志
docker-compose logs -f

# Railway 日志
railway logs

# Render 日志
# 在 Render 控制台查看
```

---

## 安全检查

- [ ] `.env` 文件未提交到 Git
- [ ] API Key 未暴露在代码中
- [ ] 使用 HTTPS（生产环境）
- [ ] 定期更新依赖
- [ ] 设置访问限流

---

## 优化建议

### 性能优化

- [ ] 启用 CDN
- [ ] 配置缓存
- [ ] 压缩静态资源
- [ ] 优化数据库查询

### 功能增强

- [ ] 添加用户认证
- [ ] 添加邮件通知
- [ ] 添加数据导出
- [ ] 添加移动端支持

---

## 完成！

恭喜！你的名人动态追踪系统已成功部署。

**访问地址：**
- 前端: https://YOUR_USERNAME.github.io/trace_money/
- 后端: https://your-backend-url.com
- API 文档: https://your-backend-url.com/docs

**下一步：**
- 📖 阅读 [使用指南](USAGE.md)
- ⚙️ 自定义配置
- 📊 查看数据统计
- 🔔 设置通知提醒
