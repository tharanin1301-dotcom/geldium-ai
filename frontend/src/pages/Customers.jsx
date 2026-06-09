import { useEffect, useState } from 'react'
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
