import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import { FiMail, FiLock, FiDatabase } from 'react-icons/fi'
import axios from 'axios'
import API_URL from '../config'

const Login = ({ setIsAuthenticated }) => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/api/auth/login`, formData)

      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))

        setIsAuthenticated(true)
        toast.success('Login successful!')
        navigate('/dashboard')
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-pale via-white to-primary-pale/50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-br from-primary to-primary-dark rounded-2xl flex items-center justify-center shadow-orange-glow">
              <FiDatabase className="text-white text-3xl" />
            </div>
          </div>
          <h2 className="text-4xl font-display font-bold gradient-text mb-2">
            Welcome Back
          </h2>
          <p className="text-neutral-darkGray">
            Sign in to generate synthetic survey data
          </p>
        </div>

        {/* Login Card */}
        <div className="card shadow-xl">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email */}
            <div>
              <label className="label">
                Email Address
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiMail className="text-neutral-darkGray" />
                </div>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="input pl-10"
                  placeholder="your@email.com"
                  required
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="label">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiLock className="text-neutral-darkGray" />
                </div>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="input pl-10"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary w-full text-lg"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                  Signing in...
                </div>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-neutral-gray"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-neutral-darkGray">
                  New to Survey Data Generator?
                </span>
              </div>
            </div>
          </div>

          {/* Sign Up Link */}
          <div className="mt-6 text-center">
            <Link
              to="/register"
              className="text-primary hover:text-primary-dark font-medium transition-colors"
            >
              Create an account
            </Link>
          </div>
        </div>

        {/* Info */}
        <div className="mt-6 text-center text-sm text-neutral-darkGray">
          <p>
            Generate statistically validated synthetic survey data for research and teaching
          </p>
        </div>
      </div>
    </div>
  )
}

export default Login
