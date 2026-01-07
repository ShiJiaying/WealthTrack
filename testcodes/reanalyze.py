"""重新分析所有未成功分析的新闻"""
import asyncio
import sys
from database import SessionLocal, NewsItem, Analysis
from deepseek_analyzer import DeepSeekAnalyzer

async def reanalyze_failed():
    db = SessionLocal()
    analyzer = DeepSeekAnalyzer()
    
    try:
        # 查找所有分析失败的记录（impact_score = 0）
        failed_analyses = db.query(Analysis).filter(Analysis.impact_score == 0.0).all()
        
        print(f"找到 {len(failed_analyses)} 条需要重新分析的记录\n")
        
        for analysis in failed_analyses:
            # 获取对应的新闻
            news = db.query(NewsItem).filter(NewsItem.id == analysis.news_id).first()
            if not news:
                continue
            
            print(f"正在分析: {news.title[:50]}...")
            
            # 重新分析
            result = await analyzer.analyze_news(
                news.figure_name,
                news.title,
                news.content
            )
            
            # 更新分析结果
            analysis.summary = result.get('summary', '')
            analysis.financial_impact = result.get('financial_impact', '')
            analysis.affected_sectors = ','.join(result.get('affected_sectors', []))
            analysis.impact_score = result.get('impact_score', 0.0)
            analysis.recommendation = result.get('recommendation', '')
            
            db.commit()
            print(f"✅ 分析完成 - 评分: {analysis.impact_score}\n")
        
        print(f"\n完成！成功重新分析 {len(failed_analyses)} 条记录")
        
    except Exception as e:
        print(f"错误: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(reanalyze_failed())
