import { Link, useNavigate, useLocation } from 'react-router-dom'
import { FiLogOut, FiHome, FiDatabase, FiCheckCircle, FiDownload } from 'react-icons/fi'

const Navbar = ({ setIsAuthenticated }) => {
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setIsAuthenticated(false)
    navigate('/login')
  }

  const isActive = (path) => location.pathname === path

  const navLinks = [
    { path: '/dashboard', icon: <FiHome />, label: 'Dashboard' },
    { path: '/generator', icon: <FiDatabase />, label: 'Generate Data' },
    { path: '/validation', icon: <FiCheckCircle />, label: 'Validation' },
    { path: '/export', icon: <FiDownload />, label: 'Export' },
  ]

  return (
    <nav className="bg-white shadow-md border-b-2 border-primary">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-primary-dark rounded-lg flex items-center justify-center">
              <FiDatabase className="text-white text-xl" />
            </div>
            <div>
              <h1 className="font-display text-xl font-bold gradient-text">
                Survey Data Generator
              </h1>
              <p className="text-xs text-neutral-darkGray">
                Statistical Research Tool
              </p>
            </div>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center space-x-1">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
                  isActive(link.path)
                    ? 'bg-primary text-white shadow-md'
                    : 'text-neutral-darkGray hover:bg-primary-pale hover:text-primary'
                }`}
              >
                <span className="text-lg">{link.icon}</span>
                <span className="hidden md:inline font-medium">{link.label}</span>
              </Link>
            ))}

            {/* Logout Button */}
            <button
              onClick={handleLogout}
              className="flex items-center space-x-2 px-4 py-2 ml-4 text-error hover:bg-error-light/10 rounded-lg transition-all"
            >
              <FiLogOut className="text-lg" />
              <span className="hidden md:inline font-medium">Logout</span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
