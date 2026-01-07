from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from database import init_db, get_db, NewsItem, Analysis
from scheduler import TaskScheduler
from config import HOST, PORT
import uvicorn

app = FastAPI(title="名人动态追踪系统")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
init_db()

# 定时任务调度器
scheduler = TaskScheduler()

@app.on_event("startup")
async def startup_event():
    """启动时执行"""
    print("=" * 50)
    print("启动名人动态追踪系统")
    print("=" * 50)
    
    # 检查配置
    from config import DEEPSEEK_API_KEY
    if not DEEPSEEK_API_KEY:
        print("⚠️  警告: DEEPSEEK_API_KEY 未配置，AI分析功能将不可用")
        print("请在 backend/.env 文件中配置 DEEPSEEK_API_KEY")
    else:
        print(f"✓ DeepSeek API 已配置")
    
    # 启动定时任务
    scheduler.start()
    
    # 立即执行一次抓取（异步执行，不阻塞启动）
    print("\n开始首次新闻抓取...")
    try:
        await scheduler.fetch_and_analyze_news()
    except Exception as e:
        print(f"首次抓取出错: {str(e)}")
    
    print("\n系统启动完成！")
    print("=" * 50)

@app.on_event("shutdown")
async def shutdown_event():
    """关闭时执行"""
    scheduler.stop()

@app.get("/")
async def root():
    return {"message": "名人动态追踪系统 API"}

@app.get("/api/news")
async def get_news(
    figure_name: Optional[str] = None,
    days: int = 7,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """获取新闻列表"""
    query = db.query(NewsItem)
    
    if figure_name:
        query = query.filter(NewsItem.figure_name == figure_name)
    
    # 只获取最近N天的新闻
    since_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(NewsItem.created_at >= since_date)
    
    news = query.order_by(NewsItem.published_at.desc()).limit(limit).all()
    
    return {
        "total": len(news),
        "news": [
            {
                "id": item.id,
                "figure_name": item.figure_name,
                "title": item.title,
                "content": item.content[:200] + "..." if len(item.content) > 200 else item.content,
                "source": item.source,
                "url": item.url,
                "published_at": item.published_at.isoformat() if item.published_at else None,
                "created_at": item.created_at.isoformat()
            }
            for item in news
        ]
    }

@app.get("/api/news/{news_id}")
async def get_news_detail(news_id: int, db: Session = Depends(get_db)):
    """获取新闻详情"""
    news = db.query(NewsItem).filter(NewsItem.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="新闻不存在")
    
    return {
        "id": news.id,
        "figure_name": news.figure_name,
        "title": news.title,
        "content": news.content,
        "source": news.source,
        "url": news.url,
        "published_at": news.published_at.isoformat() if news.published_at else None,
        "created_at": news.created_at.isoformat()
    }

@app.get("/api/analysis")
async def get_analyses(
    figure_name: Optional[str] = None,
    min_score: float = 0.0,
    days: int = 7,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """获取分析列表"""
    query = db.query(Analysis)
    
    if figure_name:
        query = query.filter(Analysis.figure_name == figure_name)
    
    if min_score > 0:
        query = query.filter(Analysis.impact_score >= min_score)
    
    since_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(Analysis.created_at >= since_date)
    
    analyses = query.order_by(Analysis.impact_score.desc()).limit(limit).all()
    
    return {
        "total": len(analyses),
        "analyses": [
            {
                "id": item.id,
                "news_id": item.news_id,
                "figure_name": item.figure_name,
                "summary": item.summary,
                "financial_impact": item.financial_impact,
                "affected_sectors": item.affected_sectors.split(',') if item.affected_sectors else [],
                "impact_score": item.impact_score,
                "recommendation": item.recommendation,
                "created_at": item.created_at.isoformat()
            }
            for item in analyses
        ]
    }

@app.get("/api/analysis/{analysis_id}")
async def get_analysis_detail(analysis_id: int, db: Session = Depends(get_db)):
    """获取分析详情"""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="分析不存在")
    
    # 获取关联的新闻
    news = db.query(NewsItem).filter(NewsItem.id == analysis.news_id).first()
    
    return {
        "id": analysis.id,
        "news_id": analysis.news_id,
        "figure_name": analysis.figure_name,
        "summary": analysis.summary,
        "financial_impact": analysis.financial_impact,
        "affected_sectors": analysis.affected_sectors.split(',') if analysis.affected_sectors else [],
        "impact_score": analysis.impact_score,
        "recommendation": analysis.recommendation,
        "created_at": analysis.created_at.isoformat(),
        "news": {
            "title": news.title,
            "url": news.url,
            "source": news.source
        } if news else None
    }

@app.get("/api/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    """获取仪表盘数据"""
    # 最近7天的统计
    since_date = datetime.utcnow() - timedelta(days=7)
    
    total_news = db.query(NewsItem).filter(NewsItem.created_at >= since_date).count()
    total_analyses = db.query(Analysis).filter(Analysis.created_at >= since_date).count()
    
    # 高影响力分析（评分>=7）
    high_impact = db.query(Analysis).filter(
        Analysis.created_at >= since_date,
        Analysis.impact_score >= 7.0
    ).order_by(Analysis.impact_score.desc()).limit(10).all()
    
    return {
        "stats": {
            "total_news": total_news,
            "total_analyses": total_analyses,
            "high_impact_count": len(high_impact)
        },
        "high_impact_analyses": [
            {
                "id": item.id,
                "figure_name": item.figure_name,
                "summary": item.summary,
                "impact_score": item.impact_score,
                "affected_sectors": item.affected_sectors.split(',') if item.affected_sectors else [],
                "recommendation": item.recommendation
            }
            for item in high_impact
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
