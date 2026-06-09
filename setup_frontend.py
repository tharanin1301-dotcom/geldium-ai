import os

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"OK {path}")

write("frontend/vite.config.js", """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
""")

write("frontend/tailwind.config.js", """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: '#1E3A8A',
      }
    },
  },
  plugins: [],
}
""")

write("frontend/src/index.css", """@tailwind base;
@tailwind components;
@tailwind utilities;
""")

write("frontend/src/api/geldium.js", """import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getStats = async () => {
  const res = await api.get('/stats')
  return res.data
}

export const getCustomers = async () => {
  const res = await api.get('/customers')
  return res.data
}

export const getCustomer = async (customerId) => {
  const res = await api.get(`/customers/${customerId}`)
  return res.data
}

export const predictRisk = async (customerData) => {
  const res = await api.post('/predict', customerData)
  return res.data
}
""")

write("frontend/src/components/RiskBadge.jsx", """const RiskBadge = ({ risk }) => {
  const styles = {
    High: 'bg-red-100 text-red-700 border border-red-300',
    Medium: 'bg-orange-100 text-orange-700 border border-orange-300',
    Low: 'bg-green-100 text-green-700 border border-green-300',
  }
  const dots = {
    High: 'bg-red-500',
    Medium: 'bg-orange-500',
    Low: 'bg-green-500',
  }
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${styles[risk]}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dots[risk]}`} />
      {risk} Risk
    </span>
  )
}
export default RiskBadge
""")

write("frontend/src/components/KPICard.jsx", """const KPICard = ({ title, value, subtitle, icon, color }) => {
  const colors = {
    blue: 'bg-blue-50 text-blue-600',
    red: 'bg-red-50 text-red-600',
    green: 'bg-green-50 text-green-600',
    orange: 'bg-orange-50 text-orange-600',
  }
  return (
    <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-3">
        <p className="text-sm font-medium text-gray-500">{title}</p>
        <div className={`p-2 rounded-lg ${colors[color]}`}>{icon}</div>
      </div>
      <p className="text-2xl font-bold text-gray-800">{value}</p>
      {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
    </div>
  )
}
export default KPICard
""")

write("frontend/src/components/Sidebar.jsx", """import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Users, Brain, BarChart3, Shield, ChevronRight } from 'lucide-react'

const navItems = [
  { path: '/', label: 'Dashboard', icon: <LayoutDashboard size={18} /> },
  { path: '/customers', label: 'Customers', icon: <Users size={18} /> },
  { path: '/analyzer', label: 'Risk Analyzer', icon: <Brain size={18} /> },
  { path: '/reports', label: 'Reports', icon: <BarChart3 size={18} /> },
]

const Sidebar = () => {
  return (
    <div className="fixed left-0 top-0 h-screen w-64 bg-[#1E3A8A] flex flex-col z-50">
      <div className="px-6 py-5 border-b border-blue-700">
        <div className="flex items-center gap-2">
          <div className="bg-blue-400 p-1.5 rounded-lg">
            <Shield size={20} className="text-white" />
          </div>
          <div>
            <h1 className="text-white font-bold text-lg leading-none">Geldium</h1>
            <p className="text-blue-300 text-xs">AI Collections</p>
          </div>
        </div>
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) =>
              `flex items-center justify-between px-3 py-2.5 rounded-lg transition-all group ${
                isActive ? 'bg-blue-500 text-white' : 'text-blue-200 hover:bg-blue-700 hover:text-white'
              }`
            }
          >
            <div className="flex items-center gap-3">
              {item.icon}
              <span className="text-sm font-medium">{item.label}</span>
            </div>
            <ChevronRight size={14} className="opacity-0 group-hover:opacity-100 transition-opacity" />
          </NavLink>
        ))}
      </nav>
      <div className="px-4 py-4 border-t border-blue-700">
        <div className="bg-blue-700 rounded-lg px-3 py-2">
          <p className="text-blue-200 text-xs">AI Model Status</p>
          <div className="flex items-center gap-2 mt-1">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
            <p className="text-white text-xs font-medium">Active & Running</p>
          </div>
        </div>
      </div>
    </div>
  )
}
export default Sidebar
""")

write("frontend/src/components/Navbar.jsx", """import { Bell, Sun, Moon, User } from 'lucide-react'

const Navbar = ({ darkMode, setDarkMode }) => {
  return (
    <div className="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-6 fixed top-0 left-64 right-0 z-40 shadow-sm">
      <div>
        <p className="text-xs text-gray-400">Geldium AI Collections System</p>
      </div>
      <div className="flex items-center gap-3">
        <button onClick={() => setDarkMode(!darkMode)} className="p-2 rounded-lg hover:bg-gray-100 text-gray-500 transition-colors">
          {darkMode ? <Sun size={18} /> : <Moon size={18} />}
        </button>
        <button className="relative p-2 rounded-lg hover:bg-gray-100 text-gray-500 transition-colors">
          <Bell size={18} />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
        </button>
        <div className="flex items-center gap-2 pl-3 border-l border-gray-200">
          <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
            <User size={15} className="text-white" />
          </div>
          <div>
            <p className="text-xs font-semibold text-gray-700">Collections Team</p>
            <p className="text-xs text-gray-400">Admin</p>
          </div>
        </div>
      </div>
    </div>
  )
}
export default Navbar
""")

write("frontend/src/App.jsx", """import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Customers from './pages/Customers'
import RiskAnalyzer from './pages/RiskAnalyzer'
import Reports from './pages/Reports'

function App() {
  const [darkMode, setDarkMode] = useState(false)
  return (
    <BrowserRouter>
      <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
        <Sidebar />
        <div className="ml-64">
          <Navbar darkMode={darkMode} setDarkMode={setDarkMode} />
          <main className="pt-14 min-h-screen">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/customers" element={<Customers />} />
              <Route path="/analyzer" element={<RiskAnalyzer />} />
              <Route path="/reports" element={<Reports />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  )
}
export default App
""")

write("frontend/src/pages/Dashboard.jsx", """import { useEffect, useState } from 'react'
import { getStats, getCustomers } from '../api/geldium'
import KPICard from '../components/KPICard'
import RiskBadge from '../components/RiskBadge'
import { Users, AlertTriangle, TrendingUp, CheckCircle } from 'lucide-react'
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid } from 'recharts'

const COLORS = ['#EF4444', '#F59E0B', '#22C55E']

const monthlyData = [
  { month: 'Jan', delinquency: 32 },
  { month: 'Feb', delinquency: 28 },
  { month: 'Mar', delinquency: 35 },
  { month: 'Apr', delinquency: 30 },
  { month: 'May', delinquency: 22 },
  { month: 'Jun', delinquency: 18 },
]

const Dashboard = () => {
  const [stats, setStats] = useState(null)
  const [customers, setCustomers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [s, c] = await Promise.all([getStats(), getCustomers()])
        setStats(s)
        setCustomers(c.customers || [])
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) return (
    <div className="flex items-center justify-center h-96">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600" />
    </div>
  )

  const pieData = stats ? [
    { name: 'High Risk', value: stats.risk_distribution.High },
    { name: 'Medium Risk', value: stats.risk_distribution.Medium },
    { name: 'Low Risk', value: stats.risk_distribution.Low },
  ] : []

  const highRisk = customers.filter(c => c.risk_label === 'High').slice(0, 5)

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <p className="text-gray-500 text-sm mt-1">AI-powered delinquency risk overview</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Total Customers" value={stats?.total_customers ?? 0} subtitle="Monitored by AI" icon={<Users size={18} />} color="blue" />
        <KPICard title="High Risk" value={stats?.risk_distribution.High ?? 0} subtitle="Immediate attention" icon={<AlertTriangle size={18} />} color="red" />
        <KPICard title="Avg Risk Score" value={stats?.average_risk_score ?? 0} subtitle="Out of 100" icon={<TrendingUp size={18} />} color="orange" />
        <KPICard title="Low Risk" value={stats?.risk_distribution.Low ?? 0} subtitle="Healthy customers" icon={<CheckCircle size={18} />} color="green" />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
          <h2 className="text-base font-semibold text-gray-700 mb-4">Risk Distribution</h2>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={100} paddingAngle={3} dataKey="value">
                {pieData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
          <h2 className="text-base font-semibold text-gray-700 mb-4">Monthly Delinquency Trend</h2>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="month" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Line type="monotone" dataKey="delinquency" stroke="#1E3A8A" strokeWidth={2.5} dot={{ fill: '#1E3A8A', r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-gray-100">
        <div className="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
          <h2 className="text-base font-semibold text-gray-700">High Risk Alerts</h2>
          <span className="text-xs text-gray-400">Top 5 needing attention</span>
        </div>
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">ID</th>
              <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Name</th>
              <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Score</th>
              <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {highRisk.length === 0 ? (
              <tr><td colSpan={4} className="px-5 py-8 text-center text-gray-400 text-sm">No high risk customers yet - add via Risk Analyzer!</td></tr>
            ) : highRisk.map((c) => (
              <tr key={c.customer_id} className="hover:bg-gray-50">
                <td className="px-5 py-3 text-sm font-mono text-gray-600">{c.customer_id}</td>
                <td className="px-5 py-3 text-sm font-medium text-gray-800">{c.name}</td>
                <td className="px-5 py-3">
                  <div className="flex items-center gap-2">
                    <div className="w-24 bg-gray-100 rounded-full h-2">
                      <div className="bg-red-500 h-2 rounded-full" style={{ width: `${c.risk_score}%` }} />
                    </div>
                    <span className="text-sm font-semibold text-gray-700">{c.risk_score}</span>
                  </div>
                </td>
                <td className="px-5 py-3"><RiskBadge risk={c.risk_label} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
export default Dashboard
""")

write("frontend/src/pages/Customers.jsx", """import { useEffect, useState } from 'react'
import { getCustomers } from '../api/geldium'
import RiskBadge from '../components/RiskBadge'
import { Search } from 'lucide-react'

const Customers = () => {
  const [customers, setCustomers] = useState([])
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState('All')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getCustomers().then(data => {
      setCustomers(data.customers || [])
      setLoading(false)
    })
  }, [])

  const filtered = customers.filter(c => {
    const matchSearch = c.name?.toLowerCase().includes(search.toLowerCase()) || c.customer_id?.includes(search)
    const matchFilter = filter === 'All' || c.risk_label === filter
    return matchSearch && matchFilter
  })

  return (
    <div className="p-6 space-y-5">
      <div>
        <h1 className="text-2xl font-bold text-gray-800">Customers</h1>
        <p className="text-gray-500 text-sm mt-1">All customers with AI risk assessments</p>
      </div>
      <div className="flex gap-3 flex-wrap">
        <div className="relative flex-1 min-w-48">
          <Search size={16} className="absolute left-3 top-2.5 text-gray-400" />
          <input
            className="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Search by name or ID..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
        {['All', 'High', 'Medium', 'Low'].map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === f ? 'bg-blue-600 text-white' : 'bg-white border border-gray-200 text-gray-600 hover:bg-gray-50'
            }`}
          >
            {f}
          </button>
        ))}
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Customer</th>
              <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Credit Score</th>
              <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Income</th>
              <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Missed</th>
              <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Risk Score</th>
              <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {loading ? (
              <tr><td colSpan={6} className="px-5 py-8 text-center text-gray-400">Loading...</td></tr>
            ) : filtered.length === 0 ? (
              <tr><td colSpan={6} className="px-5 py-8 text-center text-gray-400">No customers found</td></tr>
            ) : filtered.map(c => (
              <tr key={c.customer_id} className="hover:bg-gray-50 transition-colors">
                <td className="px-5 py-3">
                  <p className="text-sm font-medium text-gray-800">{c.name}</p>
                  <p className="text-xs text-gray-400 font-mono">{c.customer_id}</p>
                </td>
                <td className="px-5 py-3 text-sm text-gray-700">{c.credit_score}</td>
                <td className="px-5 py-3 text-sm text-gray-700">Rs.{c.monthly_income?.toLocaleString()}</td>
                <td className="px-5 py-3 text-sm text-gray-700">{c.missed_payments}</td>
                <td className="px-5 py-3">
                  <div className="flex items-center gap-2">
                    <div className="w-20 bg-gray-100 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${c.risk_score > 65 ? 'bg-red-500' : c.risk_score > 35 ? 'bg-orange-400' : 'bg-green-500'}`}
                        style={{ width: `${c.risk_score}%` }}
                      />
                    </div>
                    <span className="text-sm font-semibold text-gray-700">{c.risk_score}</span>
                  </div>
                </td>
                <td className="px-5 py-3"><RiskBadge risk={c.risk_label} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
export default Customers
""")

write("frontend/src/pages/RiskAnalyzer.jsx", """import { useState } from 'react'
import { predictRisk } from '../api/geldium'
import RiskBadge from '../components/RiskBadge'
import { Brain, Send } from 'lucide-react'

const defaultForm = {
  name: '', age: '', monthly_income: '', credit_score: '',
  credit_utilization: '', debt_to_income_ratio: '',
  missed_payments: '', payment_history_score: ''
}

const RiskAnalyzer = () => {
  const [form, setForm] = useState(defaultForm)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async () => {
    setLoading(true)
    setError('')
    try {
      const payload = {
        name: form.name,
        age: parseInt(form.age),
        monthly_income: parseFloat(form.monthly_income),
        credit_score: parseInt(form.credit_score),
        credit_utilization: parseFloat(form.credit_utilization),
        debt_to_income_ratio: parseFloat(form.debt_to_income_ratio),
        missed_payments: parseInt(form.missed_payments),
        payment_history_score: parseInt(form.payment_history_score),
      }
      const data = await predictRisk(payload)
      setResult(data)
    } catch (err) {
      setError('Failed to get prediction. Make sure backend is running!')
    } finally {
      setLoading(false)
    }
  }

  const scoreColor = result
    ? result.risk_label === 'High' ? 'text-red-600' : result.risk_label === 'Medium' ? 'text-orange-500' : 'text-green-600'
    : ''

  const fields = [
    { name: 'name', label: 'Full Name', placeholder: 'e.g. Ravi Kumar', type: 'text' },
    { name: 'age', label: 'Age', placeholder: 'e.g. 28', type: 'number' },
    { name: 'monthly_income', label: 'Monthly Income (Rs)', placeholder: 'e.g. 35000', type: 'number' },
    { name: 'credit_score', label: 'Credit Score', placeholder: '300 - 850', type: 'number' },
    { name: 'credit_utilization', label: 'Credit Utilization (0-1)', placeholder: 'e.g. 0.75', type: 'number' },
    { name: 'debt_to_income_ratio', label: 'Debt-to-Income Ratio', placeholder: 'e.g. 0.45', type: 'number' },
    { name: 'missed_payments', label: 'Missed Payments', placeholder: 'e.g. 2', type: 'number' },
    { name: 'payment_history_score', label: 'Payment History Score', placeholder: '0 - 100', type: 'number' },
  ]

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-800">Risk Analyzer</h1>
        <p className="text-gray-500 text-sm mt-1">Enter customer details to get AI risk prediction</p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center gap-2 mb-5">
            <Brain size={20} className="text-blue-600" />
            <h2 className="text-base font-semibold text-gray-700">Customer Details</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {fields.map(f => (
              <div key={f.name}>
                <label className="block text-xs font-medium text-gray-500 mb-1">{f.label}</label>
                <input
                  type={f.type}
                  name={f.name}
                  value={form[f.name]}
                  onChange={handleChange}
                  placeholder={f.placeholder}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            ))}
          </div>
          {error && <p className="text-red-500 text-sm mt-3">{error}</p>}
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="mt-5 w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Analyze Risk'}
          </button>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h2 className="text-base font-semibold text-gray-700 mb-5">Prediction Result</h2>
          {!result ? (
            <div className="flex flex-col items-center justify-center h-64 text-gray-300">
              <Brain size={48} />
              <p className="mt-3 text-sm">Submit customer details to see prediction</p>
            </div>
          ) : (
            <div className="space-y-5">
              <div className="text-center py-4">
                <p className="text-sm text-gray-500 mb-1">Risk Score</p>
                <p className={`text-6xl font-bold ${scoreColor}`}>{result.risk_score}</p>
                <div className="mt-2 flex justify-center">
                  <RiskBadge risk={result.risk_label} />
                </div>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-3">
                <div
                  className={`h-3 rounded-full transition-all ${
                    result.risk_label === 'High' ? 'bg-red-500' : result.risk_label === 'Medium' ? 'bg-orange-400' : 'bg-green-500'
                  }`}
                  style={{ width: `${result.risk_score}%` }}
                />
              </div>
              <div className="space-y-3">
                <p className="text-xs font-semibold text-gray-500 uppercase">Probability Breakdown</p>
                {Object.entries(result.probabilities).map(([label, prob]) => (
                  <div key={label}>
                    <div className="flex justify-between text-xs text-gray-600 mb-1">
                      <span>{label} Risk</span><span>{prob}%</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${label === 'High' ? 'bg-red-500' : label === 'Medium' ? 'bg-orange-400' : 'bg-green-500'}`}
                        style={{ width: `${prob}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs text-gray-500">Customer ID</p>
                <p className="text-sm font-mono font-semibold text-gray-700">{result.customer_id}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
export default RiskAnalyzer
""")

write("frontend/src/pages/Reports.jsx", """import { useEffect, useState } from 'react'
import { getStats, getCustomers } from '../api/geldium'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const Reports = () => {
  const [stats, setStats] = useState(null)
  const [customers, setCustomers] = useState([])

  useEffect(() => {
    Promise.all([getStats(), getCustomers()]).then(([s, c]) => {
      setStats(s)
      setCustomers(c.customers || [])
    })
  }, [])

  const riskBarData = stats ? [
    { name: 'High Risk', count: stats.risk_distribution.High, fill: '#EF4444' },
    { name: 'Medium Risk', count: stats.risk_distribution.Medium, fill: '#F59E0B' },
    { name: 'Low Risk', count: stats.risk_distribution.Low, fill: '#22C55E' },
  ] : []

  const scoreRanges = [
    { range: '0-20', count: customers.filter(c => c.risk_score <= 20).length },
    { range: '21-40', count: customers.filter(c => c.risk_score > 20 && c.risk_score <= 40).length },
    { range: '41-60', count: customers.filter(c => c.risk_score > 40 && c.risk_score <= 60).length },
    { range: '61-80', count: customers.filter(c => c.risk_score > 60 && c.risk_score <= 80).length },
    { range: '81-100', count: customers.filter(c => c.risk_score > 80).length },
  ]

  const funnelData = [
    { name: 'Total Customers', value: customers.length, fill: '#1E3A8A' },
    { name: 'Flagged by AI', value: Math.round(customers.length * 0.7), fill: '#3B82F6' },
    { name: 'Contacted', value: Math.round(customers.length * 0.5), fill: '#F59E0B' },
    { name: 'Recovered', value: Math.round(customers.length * 0.3), fill: '#22C55E' },
  ]

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-800">Reports</h1>
        <p className="text-gray-500 text-sm mt-1">Collections performance and risk analytics</p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
          <h2 className="text-base font-semibold text-gray-700 mb-4">Risk Distribution</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={riskBarData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="count" radius={[4,4,0,0]}>
                {riskBarData.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
          <h2 className="text-base font-semibold text-gray-700 mb-4">Risk Score Distribution</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={scoreRanges}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="range" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="count" fill="#1E3A8A" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
        <h2 className="text-base font-semibold text-gray-700 mb-6">Collections Funnel</h2>
        <div className="flex justify-around items-end gap-4 h-40">
          {funnelData.map((item, i) => (
            <div key={i} className="flex flex-col items-center gap-2 flex-1">
              <p className="text-lg font-bold text-gray-800">{item.value}</p>
              <div
                className="w-full rounded-t-lg"
                style={{ backgroundColor: item.fill, height: `${Math.max((item.value / (funnelData[0].value || 1)) * 120, 10)}px` }}
              />
              <p className="text-xs text-gray-500 text-center">{item.name}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
export default Reports
""")

print("\nAll files created successfully!")
print("Now run: cd frontend && npm run dev")
