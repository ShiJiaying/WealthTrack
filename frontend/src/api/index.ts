import axios from 'axios'

// 开发环境使用代理，生产环境使用环境变量
const baseURL = import.meta.env.DEV 
  ? '/api'  // 开发环境通过 Vite 代理
  : (import.meta.env.VITE_API_URL || 'http://localhost:8000/api')  // 生产环境直接访问

const api = axios.create({
  baseURL,
  timeout: 10000
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.config?.url)
    return Promise.reject(error)
  }
)

export interface NewsItem {
  id: number
  figure_name: string
  title: string
  content: string
  source: string
  url: string
  published_at: string
  created_at: string
}

export interface Analysis {
  id: number
  news_id: number
  figure_name: string
  summary: string
  financial_impact: string
  affected_sectors: string[]
  impact_score: number
  recommendation: string
  created_at: string
}

export const getNews = async (params?: {
  figure_name?: string
  days?: number
  limit?: number
}) => {
  const response = await api.get('/news', { params })
  return response.data
}

export const getNewsDetail = async (id: number) => {
  const response = await api.get(`/news/${id}`)
  return response.data
}

export const getAnalyses = async (params?: {
  figure_name?: string
  min_score?: number
  days?: number
  limit?: number
}) => {
  const response = await api.get('/analysis', { params })
  return response.data
}

export const getAnalysisDetail = async (id: number) => {
  const response = await api.get(`/analysis/${id}`)
  return response.data
}

export const getDashboard = async () => {
  const response = await api.get('/dashboard')
  return response.data
}

export default api
