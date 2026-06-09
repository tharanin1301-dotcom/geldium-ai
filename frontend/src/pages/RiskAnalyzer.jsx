import { useState } from 'react'
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
