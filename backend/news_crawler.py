import feedparser
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Any
from urllib.parse import quote
from config import TRACKED_FIGURES, NEWS_FEEDS

class NewsCrawler:
    def __init__(self):
        self.figures = TRACKED_FIGURES
        self.feeds = NEWS_FEEDS
    
    async def fetch_all_news(self) -> List[Dict[str, Any]]:
        """抓取所有来源的新闻"""
        all_news = []
        
        # 1. RSS 源
        rss_news = await self.fetch_rss_news()
        all_news.extend(rss_news)
        
        # 2. Google News 搜索
        google_news = await self.fetch_google_news()
        all_news.extend(google_news)
        
        # 去重（基于URL）
        seen_urls = set()
        unique_news = []
        for news in all_news:
            if news['url'] not in seen_urls:
                seen_urls.add(news['url'])
                unique_news.append(news)
        
        print(f"\n去重后共 {len(unique_news)} 条新闻")
        return unique_news
    
    async def fetch_google_news(self) -> List[Dict[str, Any]]:
        """从 Google News RSS 搜索新闻"""
        news_items = []
        
        print("\n=== Google News 搜索 ===")
        
        # 为每个重要人物搜索
        priority_figures = [f for f in self.figures if f['category'] in ['政治', '金融', '投资']]
        
        for figure in priority_figures[:10]:  # 限制搜索数量，避免过多请求
            try:
                # 使用英文名搜索，结果更准确
                query = f"{figure['name_en']} finance OR economy OR market"
                encoded_query = quote(query)
                google_news_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
                
                print(f"搜索: {figure['name']} ({figure['name_en']})")
                
                feed = feedparser.parse(google_news_url)
                
                matched_count = 0
                for entry in feed.entries[:5]:  # 每个人物取5条
                    title = entry.get('title', '')
                    content = entry.get('summary', entry.get('description', ''))
                    
                    news_items.append({
                        'figure_name': figure['name'],
                        'title': title,
                        'content': self._clean_html(content),
                        'source': 'Google News',
                        'url': entry.get('link', ''),
                        'published_at': self._parse_date(entry.get('published', ''))
                    })
                    matched_count += 1
                
                print(f"  ✓ 找到 {matched_count} 条新闻")
                
            except Exception as e:
                print(f"  ✗ 搜索失败: {str(e)}")
        
        print(f"Google News 共获取 {len(news_items)} 条新闻")
        return news_items
    
    
    async def fetch_rss_news(self) -> List[Dict[str, Any]]:
        """从RSS源获取新闻"""
        news_items = []
        
        print("\n=== RSS 源抓取 ===")
        
        for feed_url in self.feeds:
            try:
                print(f"正在抓取: {feed_url}")
                feed = feedparser.parse(feed_url)
                
                # 检查是否成功获取
                if not hasattr(feed, 'entries') or len(feed.entries) == 0:
                    print(f"  ⚠️  未获取到内容")
                    continue
                
                matched_count = 0
                for entry in feed.entries[:20]:  # 每个源取最新20条
                    title = entry.get('title', '')
                    content = entry.get('summary', entry.get('description', ''))
                    
                    # 检查是否包含关注的人物
                    matched_figure = self._match_figure(title + ' ' + content)
                    if matched_figure:
                        matched_count += 1
                        news_items.append({
                            'figure_name': matched_figure['name'],
                            'title': title,
                            'content': self._clean_html(content),
                            'source': feed.feed.get('title', feed_url.split('/')[2]),
                            'url': entry.get('link', ''),
                            'published_at': self._parse_date(entry.get('published', ''))
                        })
                
                print(f"  ✓ 匹配到 {matched_count} 条相关新闻")
                
            except Exception as e:
                print(f"  ✗ RSS抓取失败: {str(e)}")
        
        print(f"RSS 源共抓取到 {len(news_items)} 条相关新闻")
        return news_items
    
    async def search_web_news(self, figure_name: str, keywords: List[str]) -> List[Dict[str, Any]]:
        """搜索网络新闻（简化版，实际可接入Google News API等）"""
        # 这里是示例实现，实际项目中可以接入：
        # - Google News API
        # - Bing News API
        # - 自定义爬虫
        news_items = []
        
        # 示例：模拟搜索结果
        return news_items
    
    def _match_figure(self, text: str) -> Dict[str, Any]:
        """匹配文本中是否包含关注的人物"""
        for figure in self.figures:
            for keyword in figure['keywords']:
                if keyword.lower() in text.lower():
                    return figure
        return None
    
    def _clean_html(self, html_content: str) -> str:
        """清理HTML标签"""
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text().strip()
    
    def _parse_date(self, date_str: str) -> datetime:
        """解析日期"""
        try:
            return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        except:
            return datetime.utcnow()
