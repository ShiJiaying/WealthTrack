import { useEffect, useState } from 'react'
import { Card, List, Tag, Space, Select, Button, Modal, Spin } from 'antd'
import { LinkOutlined, ReloadOutlined } from '@ant-design/icons'
import { getNews, getNewsDetail, NewsItem } from '../api'

const figures = [
  '特朗普', '拜登', '习近平', '普京',
  '马斯克', '黄仁勋', '萨姆·奥特曼', '扎克伯格', '贝索斯',
  '巴菲特', '芒格', '段永平', '达里奥', '索罗斯',
  '美联储', '斯科特·贝森特', '耶伦', '拉加德',
  '沙特王储'
]

export default function NewsList() {
  const [loading, setLoading] = useState(true)
  const [news, setNews] = useState<NewsItem[]>([])
  const [selectedFigure, setSelectedFigure] = useState<string>()
  const [selectedNews, setSelectedNews] = useState<NewsItem | null>(null)
  const [modalVisible, setModalVisible] = useState(false)

  useEffect(() => {
    loadNews()
  }, [selectedFigure])

  const loadNews = async () => {
    setLoading(true)
    try {
      const result = await getNews({ figure_name: selectedFigure, days: 7, limit: 50 })
      setNews(result.news)
    } catch (error) {
      console.error('加载新闻失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const showDetail = async (id: number) => {
    try {
      const detail = await getNewsDetail(id)
      setSelectedNews(detail)
      setModalVisible(true)
    } catch (error) {
      console.error('加载详情失败:', error)
    }
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1>新闻动态</h1>
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
          <Button icon={<ReloadOutlined />} onClick={loadNews}>刷新</Button>
        </Space>
      </div>

      <Card>
        {loading ? (
          <div style={{ textAlign: 'center', padding: '50px' }}><Spin /></div>
        ) : (
          <List
            dataSource={news}
            renderItem={(item) => (
              <List.Item
                actions={[
                  <Button type="link" onClick={() => showDetail(item.id)}>查看详情</Button>,
                  <a href={item.url} target="_blank" rel="noopener noreferrer">
                    <LinkOutlined /> 原文
                  </a>
                ]}
              >
                <List.Item.Meta
                  title={
                    <Space>
                      <Tag color="blue">{item.figure_name}</Tag>
                      <span>{item.title}</span>
                    </Space>
                  }
                  description={
                    <div>
                      <div>{item.content}</div>
                      <div style={{ marginTop: 8, color: '#999' }}>
                        来源：{item.source} | 发布时间：{new Date(item.published_at).toLocaleString('zh-CN')}
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
        title="新闻详情"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setModalVisible(false)}>关闭</Button>,
          <Button key="link" type="primary" href={selectedNews?.url} target="_blank">
            查看原文
          </Button>
        ]}
        width={800}
      >
        {selectedNews && (
          <div>
            <h3>{selectedNews.title}</h3>
            <div style={{ marginBottom: 16, color: '#999' }}>
              <Tag color="blue">{selectedNews.figure_name}</Tag>
              来源：{selectedNews.source} | {new Date(selectedNews.published_at).toLocaleString('zh-CN')}
            </div>
            <div style={{ whiteSpace: 'pre-wrap' }}>{selectedNews.content}</div>
          </div>
        )}
      </Modal>
    </div>
  )
}
