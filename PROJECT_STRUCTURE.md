# 项目结构说明

```
trace_money/
├── .github/
│   └── workflows/
│       ├── deploy.yml          # GitHub Pages 自动部署
│       └── test.yml            # 自动测试
│
├── backend/                    # 后端服务
│   ├── main.py                # FastAPI 主程序
│   ├── database.py            # 数据库模型（SQLAlchemy）
│   ├── config.py              # 配置文件（人物、新闻源）
│   ├── scheduler.py           # 定时任务调度器
│   ├── news_crawler.py        # 新闻爬虫（RSS + Google News）
│   ├── deepseek_analyzer.py   # DeepSeek AI 分析器
│   ├── requirements.txt       # Python 依赖
│   ├── .env.example          # 环境变量示例
│   ├── .env                  # 环境变量（需创建）
│   │
│   └── 工具脚本/
│       ├── fetch_now.py       # 手动触发抓取
│       ├── reanalyze.py       # 重新分析失败记录
│       ├── stats.py           # 查看统计信息
│       ├── check_data.py      # 检查数据库
│       ├── test_api_simple.py # 测试 API 连接
│       └── test_crawler.py    # 测试爬虫
│
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── pages/            # 页面组件
│   │   │   ├── Dashboard.tsx      # 仪表盘
│   │   │   ├── NewsList.tsx       # 新闻列表
│   │   │   └── AnalysisList.tsx   # 分析列表
│   │   ├── components/       # 通用组件
│   │   │   └── AppHeader.tsx      # 顶部导航
│   │   ├── api/              # API 接口
│   │   │   └── index.ts           # API 封装
│   │   ├── App.tsx           # 主应用
│   │   ├── main.tsx          # 入口文件
│   │   └── index.css         # 全局样式
│   │
│   ├── public/               # 静态资源
│   ├── index.html            # HTML 模板
│   ├── package.json          # 依赖配置
│   ├── vite.config.ts        # Vite 配置
│   ├── tsconfig.json         # TypeScript 配置
│   ├── .env.development      # 开发环境变量
│   └── .env.production       # 生产环境变量
│
├── 部署配置/
│   ├── Dockerfile            # Docker 镜像配置
│   ├── docker-compose.yml    # Docker Compose 配置
│   ├── nginx.conf            # Nginx 配置
│   ├── railway.json          # Railway 部署配置
│   ├── render.yaml           # Render 部署配置
│   └── vercel.json           # Vercel 部署配置
│
├── 部署脚本/
│   ├── deploy.sh             # Linux/Mac 部署脚本
│   ├── deploy.bat            # Windows 部署脚本
│   ├── start-all.sh          # 启动所有服务
│   ├── start-backend.bat     # 启动后端
│   └── start-frontend.bat    # 启动前端
│
├── 文档/
│   ├── README.md             # 项目说明
│   ├── QUICKSTART.md         # 快速开始
│   ├── DEPLOYMENT.md         # 部署指南
│   ├── USAGE.md              # 使用指南
│   └── PROJECT_STRUCTURE.md  # 本文件
│
└── 配置文件/
    ├── .gitignore            # Git 忽略文件
    └── .dockerignore         # Docker 忽略文件
```

## 核心模块说明

### 后端模块

#### 1. main.py
- FastAPI 应用主程序
- 定义 API 路由
- 启动定时任务
- 提供健康检查接口

#### 2. database.py
- SQLAlchemy ORM 模型
- 数据库表定义（NewsItem, Analysis）
- 数据库连接管理

#### 3. config.py
- 追踪人物配置（20+ 位）
- 新闻源配置（13+ 个 RSS）
- 金融领域定义
- 环境变量加载

#### 4. scheduler.py
- APScheduler 定时任务
- 每 30 分钟自动抓取
- 新闻保存和分析流程

#### 5. news_crawler.py
- RSS 新闻抓取
- Google News 搜索
- 内容清洗和去重
- 人物匹配算法

#### 6. deepseek_analyzer.py
- DeepSeek API 调用
- 金融影响分析
- JSON 解析和容错
- 评分计算

### 前端模块

#### 1. Dashboard.tsx
- 仪表盘页面
- 统计数据展示
- 高影响力事件列表

#### 2. NewsList.tsx
- 新闻列表页面
- 按人物筛选
- 新闻详情查看

#### 3. AnalysisList.tsx
- 分析列表页面
- 按评分筛选
- 影响分析详情

#### 4. api/index.ts
- Axios 封装
- API 接口定义
- 请求/响应拦截器

## 数据流

```
1. 定时任务触发
   ↓
2. news_crawler 抓取新闻
   ├─ RSS 源
   └─ Google News
   ↓
3. 保存到数据库 (NewsItem)
   ↓
4. deepseek_analyzer 分析
   ↓
5. 保存分析结果 (Analysis)
   ↓
6. 前端通过 API 获取
   ↓
7. 展示在页面上
```

## API 端点

### 新闻相关
- `GET /api/news` - 获取新闻列表
- `GET /api/news/{id}` - 获取新闻详情

### 分析相关
- `GET /api/analysis` - 获取分析列表
- `GET /api/analysis/{id}` - 获取分析详情

### 仪表盘
- `GET /api/dashboard` - 获取仪表盘数据

### 文档
- `GET /docs` - API 文档（Swagger UI）

## 数据库表结构

### news_items
- id: 主键
- figure_name: 人物名称
- title: 新闻标题
- content: 新闻内容
- source: 新闻来源
- url: 原文链接
- published_at: 发布时间
- created_at: 创建时间

### analyses
- id: 主键
- news_id: 关联新闻 ID
- figure_name: 人物名称
- summary: 摘要
- financial_impact: 金融影响分析
- affected_sectors: 受影响领域
- impact_score: 影响评分（0-10）
- recommendation: 投资建议
- created_at: 创建时间

## 技术栈

### 后端
- **框架**: FastAPI
- **数据库**: SQLite + SQLAlchemy
- **任务调度**: APScheduler
- **HTTP 客户端**: httpx
- **RSS 解析**: feedparser
- **HTML 解析**: BeautifulSoup4

### 前端
- **框架**: React 18
- **路由**: React Router v6
- **UI 库**: Ant Design 5
- **HTTP 客户端**: Axios
- **构建工具**: Vite
- **语言**: TypeScript

### 部署
- **容器化**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **静态托管**: GitHub Pages
- **后端托管**: Railway / Render / Vercel

## 开发工作流

1. **本地开发**
   ```bash
   # 后端
   cd backend && python main.py
   
   # 前端
   cd frontend && npm run dev
   ```

2. **测试**
   ```bash
   # 后端测试
   cd backend && python test_api_simple.py
   
   # 前端构建测试
   cd frontend && npm run build
   ```

3. **提交代码**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push
   ```

4. **自动部署**
   - GitHub Actions 自动构建和部署

## 扩展建议

### 功能扩展
- [ ] 添加用户认证
- [ ] 添加邮件通知
- [ ] 添加 Webhook 推送
- [ ] 添加更多数据源
- [ ] 添加数据可视化图表
- [ ] 添加移动端适配

### 性能优化
- [ ] 添加 Redis 缓存
- [ ] 数据库索引优化
- [ ] API 响应缓存
- [ ] 前端代码分割
- [ ] CDN 加速

### 监控运维
- [ ] 添加日志系统
- [ ] 添加错误追踪
- [ ] 添加性能监控
- [ ] 添加告警系统
