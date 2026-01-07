import { Layout, Menu } from 'antd'
import { DashboardOutlined, FileTextOutlined, BarChartOutlined } from '@ant-design/icons'
import { useNavigate, useLocation } from 'react-router-dom'

const { Header } = Layout

export default function AppHeader() {
  const navigate = useNavigate()
  const location = useLocation()

  const menuItems = [
    { key: '/', label: '仪表盘', icon: <DashboardOutlined /> },
    { key: '/news', label: '新闻动态', icon: <FileTextOutlined /> },
    { key: '/analysis', label: '影响分析', icon: <BarChartOutlined /> }
  ]

  return (
    <Header style={{ display: 'flex', alignItems: 'center', background: '#001529' }}>
      <div style={{ color: 'white', fontSize: '20px', fontWeight: 'bold', marginRight: '50px' }}>
        名人动态追踪系统
      </div>
      <Menu
        theme="dark"
        mode="horizontal"
        selectedKeys={[location.pathname]}
        items={menuItems}
        onClick={({ key }) => navigate(key)}
        style={{ flex: 1, minWidth: 0 }}
      />
    </Header>
  )
}
