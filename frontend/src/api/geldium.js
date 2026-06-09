import axios from 'axios'

const API_BASE = 'https://web-production-cb024.up.railway.app'

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
