import { useEffect, useState } from 'react'
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
