import sqlite3

conn = sqlite3.connect('celebrity_tracker.db')
cursor = conn.cursor()

print("=== 数据库检查 ===\n")

# 检查新闻数量
cursor.execute('SELECT COUNT(*) FROM news_items')
news_count = cursor.fetchone()[0]
print(f"新闻数量: {news_count}")

# 检查分析数量
cursor.execute('SELECT COUNT(*) FROM analyses')
analysis_count = cursor.fetchone()[0]
print(f"分析数量: {analysis_count}\n")

# 查看最新的3条分析
print("=== 最新分析内容 ===\n")
cursor.execute('''
    SELECT id, figure_name, summary, financial_impact, impact_score 
    FROM analyses 
    ORDER BY created_at DESC 
    LIMIT 3
''')

for row in cursor.fetchall():
    print(f"ID: {row[0]}")
    print(f"人物: {row[1]}")
    print(f"摘要: {row[2][:100]}...")
    print(f"影响: {row[3][:100]}...")
    print(f"评分: {row[4]}")
    print("-" * 50)

conn.close()
