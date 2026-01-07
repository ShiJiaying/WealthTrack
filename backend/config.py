import os
from dotenv import load_dotenv

load_dotenv()

# API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")

# 服务器配置
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# 追踪的名人列表
TRACKED_FIGURES = [
    # 政治人物
    {
        "name": "特朗普",
        "name_en": "Donald Trump",
        "twitter": "realDonaldTrump",
        "keywords": ["Trump", "特朗普", "Donald Trump"],
        "category": "政治"
    },
    {
        "name": "拜登",
        "name_en": "Joe Biden",
        "twitter": "POTUS",
        "keywords": ["Biden", "拜登", "Joe Biden", "President Biden"],
        "category": "政治"
    },
    {
        "name": "习近平",
        "name_en": "Xi Jinping",
        "twitter": "",
        "keywords": ["Xi Jinping", "习近平", "President Xi", "中国主席"],
        "category": "政治"
    },
    {
        "name": "普京",
        "name_en": "Vladimir Putin",
        "twitter": "",
        "keywords": ["Putin", "普京", "Vladimir Putin", "Russia"],
        "category": "政治"
    },
    
    # 科技领袖
    {
        "name": "马斯克",
        "name_en": "Elon Musk",
        "twitter": "elonmusk",
        "keywords": ["Elon Musk", "马斯克", "Tesla", "SpaceX", "Musk"],
        "category": "科技"
    },
    {
        "name": "黄仁勋",
        "name_en": "Jensen Huang",
        "twitter": "",
        "keywords": ["Jensen Huang", "黄仁勋", "Nvidia", "英伟达"],
        "category": "科技"
    },
    {
        "name": "萨姆·奥特曼",
        "name_en": "Sam Altman",
        "twitter": "sama",
        "keywords": ["Sam Altman", "奥特曼", "OpenAI", "Altman"],
        "category": "科技"
    },
    {
        "name": "扎克伯格",
        "name_en": "Mark Zuckerberg",
        "twitter": "",
        "keywords": ["Zuckerberg", "扎克伯格", "Meta", "Facebook"],
        "category": "科技"
    },
    {
        "name": "贝索斯",
        "name_en": "Jeff Bezos",
        "twitter": "JeffBezos",
        "keywords": ["Bezos", "贝索斯", "Amazon", "亚马逊"],
        "category": "科技"
    },
    
    # 投资大师
    {
        "name": "巴菲特",
        "name_en": "Warren Buffett",
        "twitter": "",
        "keywords": ["Warren Buffett", "巴菲特", "Berkshire", "伯克希尔"],
        "category": "投资"
    },
    {
        "name": "芒格",
        "name_en": "Charlie Munger",
        "twitter": "",
        "keywords": ["Charlie Munger", "芒格", "Munger"],
        "category": "投资"
    },
    {
        "name": "段永平",
        "name_en": "Duan Yongping",
        "twitter": "",
        "keywords": ["段永平", "Duan Yongping"],
        "category": "投资"
    },
    {
        "name": "达里奥",
        "name_en": "Ray Dalio",
        "twitter": "RayDalio",
        "keywords": ["Ray Dalio", "达里奥", "Bridgewater", "桥水"],
        "category": "投资"
    },
    {
        "name": "索罗斯",
        "name_en": "George Soros",
        "twitter": "",
        "keywords": ["Soros", "索罗斯", "George Soros"],
        "category": "投资"
    },
    
    # 金融机构领导人
    {
        "name": "美联储",
        "name_en": "Federal Reserve",
        "twitter": "federalreserve",
        "keywords": ["Federal Reserve", "美联储", "Fed", "Powell", "鲍威尔", "Jerome Powell"],
        "category": "金融"
    },
    {
        "name": "斯科特·贝森特",
        "name_en": "Scott Bessent",
        "twitter": "",
        "keywords": ["Scott Bessent", "斯科特·贝森特", "Bessent"],
        "category": "金融"
    },
    {
        "name": "耶伦",
        "name_en": "Janet Yellen",
        "twitter": "",
        "keywords": ["Yellen", "耶伦", "Janet Yellen", "Treasury"],
        "category": "金融"
    },
    {
        "name": "拉加德",
        "name_en": "Christine Lagarde",
        "twitter": "",
        "keywords": ["Lagarde", "拉加德", "ECB", "欧洲央行"],
        "category": "金融"
    },
    
    # 能源/大宗商品
    {
        "name": "沙特王储",
        "name_en": "Mohammed bin Salman",
        "twitter": "",
        "keywords": ["MBS", "Mohammed bin Salman", "沙特", "Saudi", "OPEC"],
        "category": "能源"
    }
]

# 新闻源RSS（扩展更多来源）
NEWS_FEEDS = [
    # 综合财经
    "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    "https://feeds.bloomberg.com/markets/news.rss",
    "https://www.ft.com/rss/home",
    "https://www.reuters.com/rssfeed/businessNews",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://www.wsj.com/xml/rss/3_7085.xml",
    
    # 科技
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    
    # 加密货币
    "https://cointelegraph.com/rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    
    # 能源
    "https://oilprice.com/rss/main",
    
    # 中文财经
    "https://cn.wsj.com/zh-hans/rss",
]

# 金融领域
FINANCIAL_SECTORS = [
    "股市",
    "金价",
    "油气",
    "加密货币",
    "债券",
    "外汇",
    "大宗商品"
]
