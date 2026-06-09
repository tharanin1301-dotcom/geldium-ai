import { NavLink } from 'react-router-dom'
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
