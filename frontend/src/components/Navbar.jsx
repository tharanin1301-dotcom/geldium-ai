import { Bell, Sun, Moon, User } from 'lucide-react'

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
