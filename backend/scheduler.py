from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, NewsItem, Analysis
from news_crawler import NewsCrawler
from deepseek_analyzer import DeepSeekAnalyzer

class TaskScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.crawler = NewsCrawler()
        self.analyzer = DeepSeekAnalyzer()
    
    def start(self):
        """启动定时任务"""
        # 每30分钟抓取一次新闻
        self.scheduler.add_job(
            self.fetch_and_analyze_news,
            trigger=IntervalTrigger(minutes=30),
            id='fetch_news',
            name='抓取并分析新闻',
            replace_existing=True
        )
        
        self.scheduler.start()
        print("定时任务已启动：每30分钟抓取一次新闻")
    
    async def fetch_and_analyze_news(self):
        """抓取新闻并进行分析"""
        print(f"\n{'='*60}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始抓取新闻")
        print(f"{'='*60}")
        
        # 抓取新闻（包括RSS和Google News）
        news_items = await self.crawler.fetch_all_news()
        print(f"\n总共获取 {len(news_items)} 条新闻")
        
        # 保存并分析
        db = SessionLocal()
        new_count = 0
        analyzed_count = 0
        
        try:
            for item in news_items:
                # 检查是否已存在
                existing = db.query(NewsItem).filter(
                    NewsItem.url == item['url']
                ).first()
                
                if not existing:
                    new_count += 1
                    # 保存新闻
                    news = NewsItem(**item)
                    db.add(news)
                    db.commit()
                    db.refresh(news)
                    
                    # AI分析
                    print(f"\n[{analyzed_count + 1}] 分析: {item['title'][:60]}...")
                    analysis_result = await self.analyzer.analyze_news(
                        item['figure_name'],
                        item['title'],
                        item['content']
                    )
                    
                    # 保存分析结果
                    analysis = Analysis(
                        news_id=news.id,
                        figure_name=item['figure_name'],
                        summary=analysis_result.get('summary', ''),
                        financial_impact=analysis_result.get('financial_impact', ''),
                        affected_sectors=','.join(analysis_result.get('affected_sectors', [])),
                        impact_score=analysis_result.get('impact_score', 0.0),
                        recommendation=analysis_result.get('recommendation', '')
                    )
                    db.add(analysis)
                    db.commit()
                    analyzed_count += 1
                    
                    print(f"    ✓ 已保存 - 评分: {analysis.impact_score}")
        
        except Exception as e:
            print(f"\n✗ 处理新闻时出错: {str(e)}")
            import traceback
            traceback.print_exc()
            db.rollback()
        finally:
            db.close()
        
        print(f"\n{'='*60}")
        print(f"抓取完成: 新增 {new_count} 条新闻，分析 {analyzed_count} 条")
        print(f"{'='*60}\n")
    
    def stop(self):
        """停止定时任务"""
        self.scheduler.shutdown()
