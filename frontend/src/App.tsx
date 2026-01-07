import { Routes, Route } from 'react-router-dom'
import { Layout } from 'antd'
import Dashboard from './pages/Dashboard'
import NewsList from './pages/NewsList'
import AnalysisList from './pages/AnalysisList'
import AppHeader from './components/AppHeader'

const { Content } = Layout

function App() {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <AppHeader />
      <Content style={{ padding: '24px 50px' }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/news" element={<NewsList />} />
          <Route path="/analysis" element={<AnalysisList />} />
        </Routes>
      </Content>
    </Layout>
  )
}

export default App
