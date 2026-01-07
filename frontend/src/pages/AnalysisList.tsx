import { useEffect, useState } from 'react'
import { Card, List, Tag, Space, Select, Button, Modal, Slider, Spin } from 'antd'
import { ReloadOutlined } from '@ant-design/icons'
import { getAnalyses, getAnalysisDetail, Analysis } from '../api'

const figures = [
  '特朗普', '拜登', '习近平', '普京',
  '马斯克', '黄仁勋', '萨姆·奥特曼', '扎克伯格', '贝索斯',
  '巴菲特', '芒格', '段永平', '达里奥', '索罗斯',
  '美联储', '斯科特·贝森特', '耶伦', '拉加德',
  '沙特王储'
]

export default function AnalysisList() {
  const [loading, setLoading] = useState(true)
  const [analyses, setAnalyses] = useState<Analysis[]>([])
  const [selectedFigure, setSelectedFigure] = useState<string>()
  const [minScore, setMinScore] = useState(0)
  const [selectedAnalysis, setSelectedAnalysis] = useState<any>(null)
  const [modalVisible, setModalVisible] = useState(false)

  useEffect(() => {
    loadAnalyses()
  }, [selectedFigure, minScore])

  const loadAnalyses = async () => {
    setLoading(true)
    try {
      const result = await getAnalyses({
        figure_name: selectedFigure,
        min_score: minScore,
        days: 7,
        limit: 50
      })
      setAnalyses(result.analyses)
    } catch (error) {
      console.error('加载分析失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const showDetail = async (id: number) => {
    try {
      const detail = await getAnalysisDetail(id)
      setSelectedAnalysis(detail)
      setModalVisible(true)
    } catch (error) {
      console.error('加载详情失败:', error)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'red'
    if (score >= 6) return 'orange'
    if (score >= 4) return 'gold'
    return 'blue'
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1>影响分析</h1>
        <Space>
          <Select
            style={{ width: 200 }}
            placeholder="选择人物"
            allowClear
            value={selectedFigure}
            onChange={setSelectedFigure}
          >
            {figures.map(f => (
              <Select.Option key={f} value={f}>{f}</Select.Option>
            ))}
          </Select>
          <Button icon={<ReloadOutlined />} onClick={loadAnalyses}>刷新</Button>
        </Space>
      </div>

      <Card style={{ marginBottom: 16 }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <span style={{ marginRight: 16 }}>最低影响评分：</span>
          <Slider
            style={{ flex: 1, maxWidth: 300 }}
            min={0}
            max={10}
            step={0.5}
            value={minScore}
            onChange={setMinScore}
            marks={{ 0: '0', 5: '5', 10: '10' }}
          />
          <span style={{ marginLeft: 16, fontWeight: 'bold' }}>{minScore}</span>
        </div>
      </Card>

      <Card>
        {loading ? (
          <div style={{ textAlign: 'center', padding: '50px' }}><Spin /></div>
        ) : (
          <List
            dataSource={analyses}
            renderItem={(item) => (
              <List.Item
                actions={[
                  <Button type="link" onClick={() => showDetail(item.id)}>查看详情</Button>
                ]}
              >
                <List.Item.Meta
                  title={
                    <Space>
                      <Tag color="blue">{item.figure_name}</Tag>
                      <Tag color={getScoreColor(item.impact_score)}>
                        影响评分：{item.impact_score.toFixed(1)}
                      </Tag>
                      <span>{item.summary}</span>
                    </Space>
                  }
                  description={
                    <div>
                      <div style={{ marginBottom: 8 }}>
                        <strong>受影响领域：</strong>
                        {item.affected_sectors.map(sector => (
                          <Tag key={sector}>{sector}</Tag>
                        ))}
                      </div>
                      <div style={{ marginBottom: 8 }}>
                        <strong>金融影响：</strong>{item.financial_impact.substring(0, 150)}...
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
        )}
      </Card>

      <Modal
        title="分析详情"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setModalVisible(false)}>关闭</Button>
        ]}
        width={900}
      >
        {selectedAnalysis && (
          <div>
            <Space style={{ marginBottom: 16 }}>
              <Tag color="blue">{selectedAnalysis.figure_name}</Tag>
              <Tag color={getScoreColor(selectedAnalysis.impact_score)}>
                影响评分：{selectedAnalysis.impact_score.toFixed(1)}
              </Tag>
            </Space>

            {selectedAnalysis.news && (
              <Card size="small" title="相关新闻" style={{ marginBottom: 16 }}>
                <div><strong>{selectedAnalysis.news.title}</strong></div>
                <div style={{ marginTop: 8, color: '#999' }}>
                  来源：{selectedAnalysis.news.source} | 
                  <a href={selectedAnalysis.news.url} target="_blank" rel="noopener noreferrer"> 查看原文</a>
                </div>
              </Card>
            )}

            <Card size="small" title="摘要" style={{ marginBottom: 16 }}>
              {selectedAnalysis.summary}
            </Card>

            <Card size="small" title="金融影响分析" style={{ marginBottom: 16 }}>
              <div style={{ whiteSpace: 'pre-wrap' }}>{selectedAnalysis.financial_impact}</div>
            </Card>

            <Card size="small" title="受影响领域" style={{ marginBottom: 16 }}>
              {selectedAnalysis.affected_sectors.map((sector: string) => (
                <Tag key={sector} color="orange">{sector}</Tag>
              ))}
            </Card>

            <Card size="small" title="投资建议">
              {selectedAnalysis.recommendation}
            </Card>
          </div>
        )}
      </Modal>
    </div>
  )
}
