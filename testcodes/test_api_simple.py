import os

print("=== 检查环境变量 ===\n")

# 读取 .env 文件
env_vars = {}
try:
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
except FileNotFoundError:
    print("❌ .env 文件不存在")
    exit(1)

api_key = env_vars.get('DEEPSEEK_API_KEY', '')
api_url = env_vars.get('DEEPSEEK_API_URL', '')

print(f"API URL: {api_url}")
print(f"API Key: {api_key[:20]}..." if api_key else "未配置")
print()

if not api_key or api_key == 'your_deepseek_api_key_here':
    print("❌ 错误: 请在 .env 文件中配置正确的 DEEPSEEK_API_KEY")
    print("\n请访问 https://platform.deepseek.com/ 获取 API Key")
else:
    print("✅ API Key 已配置")
    print("\n正在测试 API 连接...")
    
    # 测试 API
    import json
    try:
        import urllib.request
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "测试"}],
            "max_tokens": 10
        }
        
        req = urllib.request.Request(
            api_url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("✅ API 调用成功!")
            print(f"回复: {result['choices'][0]['message']['content']}")
            
    except Exception as e:
        print(f"❌ API 调用失败: {str(e)}")
        print("\n可能的原因:")
        print("1. API Key 无效或已过期")
        print("2. 账户余额不足")
        print("3. 网络连接问题")
        print("4. API URL 不正确")
