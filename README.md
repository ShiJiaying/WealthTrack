# 名人动态追踪与金融影响分析系统

实时追踪特朗普、马斯克、段永平、美联储、斯科特·贝森特等中外名人的采访、发言、行业动态，并使用 DeepSeek API 分析其对金融市场的潜在影响。

## 功能特性

- 🔍 多源信息抓取
  - 13+ RSS 新闻源（Bloomberg, Reuters, WSJ, CNBC, TechCrunch等）
  - Google News 智能搜索
  - 自动去重和内容清洗
- 👥 追踪20+重要人物
  - 政治：特朗普、拜登、习近平、普京
  - 科技：马斯克、黄仁勋、奥特曼、扎克伯格、贝索斯
  - 投资：巴菲特、芒格、段永平、达里奥、索罗斯
  - 金融：美联储、贝森特、耶伦、拉加德
  - 能源：沙特王储
- 🤖 DeepSeek AI 智能分析
- 📊 金融影响评估（股市、金价、油气、加密货币等）
- 🔔 实时通知与预警
- 📈 历史数据追踪与统计

## 技术栈

- 后端：Python + FastAPI
- 前端：React + TypeScript + Vite
- AI分析：DeepSeek API
- 数据库：SQLite
- 任务调度：APScheduler

## 快速开始

### 本地开发

**后端：**
```bash
cd backend
pip install -r requirements.txt

# 配置 DeepSeek API Key
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key

python main.py
```

**前端：**
```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000

### 部署到生产环境

**方式 1: GitHub Pages + Railway/Render**
```bash
# 1. 部署前端到 GitHub Pages
./deploy.sh github

# 2. 部署后端到 Railway 或 Render
# 详见 DEPLOYMENT.md
```

**方式 2: Docker 完整部署**
```bash
./deploy.sh docker
```

详细部署指南请查看 [DEPLOYMENT.md](DEPLOYMENT.md)

### 常用命令
```bash
# 手动触发抓取
cd backend
python fetch_now.py

# 查看统计信息
python stats.py

# 重新分析失败的记录
python reanalyze.py

# 检查数据
python check_data.py
```

## 配置

在 `backend/.env` 文件中配置：
- DEEPSEEK_API_KEY：DeepSeek API密钥
- TWITTER_BEARER_TOKEN：Twitter API令牌（可选）
