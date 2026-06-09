import { useEffect, useState } from 'react'
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
