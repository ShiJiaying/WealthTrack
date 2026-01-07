"""立即执行一次新闻抓取和分析"""
import asyncio
from scheduler import TaskScheduler

async def main():
    print("开始手动抓取新闻...")
    scheduler = TaskScheduler()
    await scheduler.fetch_and_analyze_news()
    print("\n抓取完成！")

if __name__ == "__main__":
    asyncio.run(main())
