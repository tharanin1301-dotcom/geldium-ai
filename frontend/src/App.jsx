import { BrowserRouter, Routes, Route } from 'react-router-dom'
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
