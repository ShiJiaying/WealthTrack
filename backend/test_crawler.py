"""测试新闻爬虫（不需要数据库）"""
import asyncio
import sys
sys.path.insert(0, '.')

from news_crawler import NewsCrawler

async def test():
    crawler = NewsCrawler()
    
    print("测试 RSS 抓取...")
    rss_news = await crawler.fetch_rss_news()
    print(f"\nRSS 抓取结果: {len(rss_news)} 条")
    
    if rss_news:
        print("\n示例新闻:")
        for i, news in enumerate(rss_news[:3], 1):
            print(f"\n{i}. [{news['figure_name']}] {news['title'][:60]}...")
            print(f"   来源: {news['source']}")
    
    print("\n" + "="*60)
    print("测试 Google News 搜索...")
    google_news = await crawler.fetch_google_news()
    print(f"\nGoogle News 结果: {len(google_news)} 条")
    
    if google_news:
        print("\n示例新闻:")
        for i, news in enumerate(google_news[:3], 1):
            print(f"\n{i}. [{news['figure_name']}] {news['title'][:60]}...")
    
    print("\n" + "="*60)
    print(f"总计: {len(rss_news) + len(google_news)} 条新闻")

if __name__ == "__main__":
    asyncio.run(test())
