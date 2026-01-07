"""查看数据库统计信息"""
import sqlite3
from collections import Counter

conn = sqlite3.connect('celebrity_tracker.db')
cursor = conn.cursor()

print("=" * 60)
print("数据库统计信息")
print("=" * 60)

# 总体统计
cursor.execute('SELECT COUNT(*) FROM news_items')
total_news = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM analyses')
total_analyses = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM analyses WHERE impact_score >= 7')
high_impact = cursor.fetchone()[0]

print(f"\n总新闻数: {total_news}")
print(f"总分析数: {total_analyses}")
print(f"高影响力事件 (≥7分): {high_impact}")

# 按人物统计
print("\n" + "=" * 60)
print("按人物统计")
print("=" * 60)

cursor.execute('''
    SELECT figure_name, COUNT(*) as count 
    FROM news_items 
    GROUP BY figure_name 
    ORDER BY count DESC
''')

for row in cursor.fetchall():
    print(f"{row[0]:15s}: {row[1]:3d} 条新闻")

# 按来源统计
print("\n" + "=" * 60)
print("按新闻源统计")
print("=" * 60)

cursor.execute('''
    SELECT source, COUNT(*) as count 
    FROM news_items 
    GROUP BY source 
    ORDER BY count DESC
    LIMIT 10
''')

for row in cursor.fetchall():
    print(f"{row[0]:30s}: {row[1]:3d} 条")

# 影响评分分布
print("\n" + "=" * 60)
print("影响评分分布")
print("=" * 60)

cursor.execute('SELECT impact_score FROM analyses WHERE impact_score > 0')
scores = [row[0] for row in cursor.fetchall()]

if scores:
    print(f"平均评分: {sum(scores)/len(scores):.2f}")
    print(f"最高评分: {max(scores):.2f}")
    print(f"最低评分: {min(scores):.2f}")
    
    # 评分区间
    ranges = {
        '0-3分 (轻微)': len([s for s in scores if 0 <= s < 3]),
        '3-5分 (一般)': len([s for s in scores if 3 <= s < 5]),
        '5-7分 (中等)': len([s for s in scores if 5 <= s < 7]),
        '7-9分 (重大)': len([s for s in scores if 7 <= s < 9]),
        '9-10分 (极高)': len([s for s in scores if 9 <= s <= 10]),
    }
    
    print("\n评分区间分布:")
    for range_name, count in ranges.items():
        print(f"  {range_name}: {count} 条")

# 最新高影响力事件
print("\n" + "=" * 60)
print("最新高影响力事件 (评分≥7)")
print("=" * 60)

cursor.execute('''
    SELECT n.figure_name, n.title, a.impact_score, a.recommendation
    FROM analyses a
    JOIN news_items n ON a.news_id = n.id
    WHERE a.impact_score >= 7
    ORDER BY a.created_at DESC
    LIMIT 5
''')

for i, row in enumerate(cursor.fetchall(), 1):
    print(f"\n{i}. [{row[0]}] 评分: {row[2]:.1f}")
    print(f"   {row[1][:70]}...")
    print(f"   建议: {row[3]}")

conn.close()

print("\n" + "=" * 60)
