import httpx
import json
import os
from typing import Dict, Any

class DeepSeekAnalyzer:
    def __init__(self):
        # 直接从环境变量读取，确保获取最新值
        from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
        self.api_key = DEEPSEEK_API_KEY
        self.api_url = DEEPSEEK_API_URL
        
        if not self.api_key:
            print("警告: DEEPSEEK_API_KEY 未配置")
        else:
            print(f"DeepSeek API 已配置: {self.api_key[:20]}...")
    
    async def analyze_news(self, figure_name: str, title: str, content: str) -> Dict[str, Any]:
        """使用DeepSeek分析新闻对金融市场的影响"""
        
        prompt = f"""
你是一位资深的金融分析师。请分析以下关于{figure_name}的新闻，评估其对金融市场的潜在影响。

新闻标题：{title}
新闻内容：{content}

请从以下几个方面进行分析：
1. 新闻摘要（100字以内）
2. 金融影响分析（可能影响哪些金融领域：股市、金价、油气、加密货币、债券、外汇等）
3. 影响程度评分（0-10分，10分为最高影响）
4. 受影响的具体行业或概念板块
5. 投资建议（关注、观望、规避等）

请以JSON格式返回结果：
{{
    "summary": "新闻摘要",
    "financial_impact": "详细的金融影响分析",
    "impact_score": 7.5,
    "affected_sectors": ["股市-科技板块", "加密货币"],
    "recommendation": "投资建议"
}}
"""
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": [
                            {"role": "system", "content": "你是一位专业的金融分析师，擅长分析新闻事件对金融市场的影响。"},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 2000
                    }
                )
                
                print(f"DeepSeek API 响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    # 尝试解析JSON
                    try:
                        # 提取JSON内容（可能包含在markdown代码块中）
                        if "```json" in content:
                            content = content.split("```json")[1].split("```")[0].strip()
                        elif "```" in content:
                            content = content.split("```")[1].split("```")[0].strip()
                        
                        analysis = json.loads(content)
                        print(f"✓ 分析成功 - 评分: {analysis.get('impact_score', 0)}")
                        return analysis
                    except json.JSONDecodeError as e:
                        print(f"JSON解析失败: {str(e)}")
                        # 如果返回的不是纯JSON，尝试提取
                        return {
                            "summary": content[:200],
                            "financial_impact": content,
                            "impact_score": 5.0,
                            "affected_sectors": [],
                            "recommendation": "需要进一步分析"
                        }
                else:
                    print(f"API错误响应: {response.text[:200]}")
                    return self._get_fallback_analysis()
                    
        except Exception as e:
            print(f"DeepSeek API调用失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._get_fallback_analysis()
    
    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """API失败时的备用分析"""
        return {
            "summary": "分析暂时不可用",
            "financial_impact": "API调用失败，请稍后重试",
            "impact_score": 0.0,
            "affected_sectors": [],
            "recommendation": "等待分析"
        }
