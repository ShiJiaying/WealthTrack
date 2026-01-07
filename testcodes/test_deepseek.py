import asyncio
import httpx
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL

async def test_deepseek():
    print("=== 测试 DeepSeek API ===\n")
    print(f"API URL: {DEEPSEEK_API_URL}")
    print(f"API Key: {DEEPSEEK_API_KEY[:20]}..." if DEEPSEEK_API_KEY else "未配置")
    print()
    
    if not DEEPSEEK_API_KEY:
        print("❌ 错误: DEEPSEEK_API_KEY 未配置")
        return
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                DEEPSEEK_API_URL,
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "user", "content": "你好，请回复'测试成功'"}
                    ],
                    "max_tokens": 50
                }
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                print(f"✅ API 调用成功!")
                print(f"回复: {content}")
            else:
                print(f"❌ API 调用失败")
                print(f"响应: {response.text}")
                
    except Exception as e:
        print(f"❌ 错误: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_deepseek())
