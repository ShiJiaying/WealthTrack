import { useEffect, useState } from 'react'
import { Card, Row, Col, Statistic, List, Tag, Space, Spin } from 'antd'
import { TrophyOutlined, FileTextOutlined, BarChartOutlined } from '@ant-design/icons'
import { getDashboard } from '../api'

export default function Dashboard() {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const result = await getDashboard()
      setData(result)
    } catch (error) {
      console.error('加载数据失败:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div style={{ textAlign: 'center', padding: '100px' }}><Spin size="large" /></div>
  }

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'red'
    if (score >= 6) return 'orange'
    return 'blue'
  }

  return (
    <div>
      <h1>仪表盘</h1>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Card>
            <Statistic
              title="最近7天新闻数"
              value={data?.stats?.total_news || 0}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="分析报告数"
              value={data?.stats?.total_analyses || 0}
              prefix={<BarChartOutlined />}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="高影响力事件"
              value={data?.stats?.high_impact_count || 0}
              prefix={<TrophyOutlined />}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
      </Row>

      <Card title="高影响力分析（评分≥7分）" style={{ marginTop: 24 }}>
        <List
          dataSource={data?.high_impact_analyses || []}
          renderItem={(item: any) => (
            <List.Item>
              <List.Item.Meta
                title={
                  <Space>
                    <Tag color="blue">{item.figure_name}</Tag>
                    <span>{item.summary}</span>
                  </Space>
                }
                description={
                  <div>
                    <div style={{ marginBottom: 8 }}>
                      <strong>影响评分：</strong>
                      <Tag color={getScoreColor(item.impact_score)}>
                        {item.impact_score.toFixed(1)}
                      </Tag>
                    </div>
                    <div style={{ marginBottom: 8 }}>
                      <strong>受影响领域：</strong>
                      {item.affected_sectors.map((sector: string) => (
                        <Tag key={sector}>{sector}</Tag>
                      ))}
                    </div>
                    <div>
                      <strong>建议：</strong>{item.recommendation}
                    </div>
                  </div>
                }
              />
            </List.Item>
          )}
        />
      </Card>
    </div>
  )
}
