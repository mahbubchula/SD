import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { FiDatabase, FiCheckCircle, FiDownload, FiTrendingUp, FiUsers, FiBarChart2, FiArrowRight } from 'react-icons/fi'

const Dashboard = () => {
  const [user, setUser] = useState(null)

  useEffect(() => {
    const userData = localStorage.getItem('user')
    if (userData) {
      setUser(JSON.parse(userData))
    }
  }, [])

  const features = [
    {
      icon: <FiDatabase className="text-3xl" />,
      title: 'Data Generation',
      description: 'Generate statistically validated synthetic survey data with full control over parameters',
      link: '/generator',
      color: 'from-primary to-primary-dark',
    },
    {
      icon: <FiCheckCircle className="text-3xl" />,
      title: 'Pre-Validation',
      description: 'Validate your data against SmartPLS, SEM, and fsQCA criteria before generation',
      link: '/validation',
      color: 'from-success to-success-dark',
    },
    {
      icon: <FiDownload className="text-3xl" />,
      title: 'Export Data',
      description: 'Export in multiple formats: SPSS, Excel, CSV, SmartPLS, and JSON',
      link: '/export',
      color: 'from-primary-dark to-primary',
    },
  ]

  const stats = [
    {
      label: 'Sample Size Range',
      value: '100 - 10,000',
      icon: <FiUsers />,
      color: 'bg-orange-500',
    },
    {
      label: 'Statistical Methods',
      value: 'PLS-SEM, fsQCA',
      icon: <FiBarChart2 />,
      color: 'bg-green-500',
    },
    {
      label: 'Export Formats',
      value: '5 Formats',
      icon: <FiDownload />,
      color: 'bg-blue-500',
    },
    {
      label: 'Validation Tests',
      value: '20+ Tests',
      icon: <FiTrendingUp />,
      color: 'bg-purple-500',
    },
  ]

  const validationTests = [
    'Normality (Kolmogorov-Smirnov, Shapiro-Wilk)',
    'Reliability (Cronbach Alpha, CR, AVE)',
    'Validity (Fornell-Larcker, HTMT, Cross-Loadings)',
    'Direct Effects (Path Coefficients)',
    'Indirect Effects (Mediation Analysis)',
    'Total Effects (Direct + Indirect)',
    'Moderation Analysis (Interaction Effects)',
    'Model Fit (R², f², VIF < 5, GoF)',
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-pale/30 via-white to-primary-pale/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Header */}
        <div className="mb-8 slide-up">
          <h1 className="text-4xl font-display font-bold text-neutral-darker mb-2">
            Welcome back, <span className="gradient-text">{user?.full_name || 'User'}</span>
          </h1>
          <p className="text-lg text-neutral-darkGray">
            Generate statistically validated synthetic survey data for your research
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <div
              key={index}
              className="card card-hover fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-neutral-darkGray mb-1">{stat.label}</p>
                  <p className="text-2xl font-bold text-neutral-darker">{stat.value}</p>
                </div>
                <div className={`${stat.color} text-white p-3 rounded-lg`}>
                  {stat.icon}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Main Features */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {features.map((feature, index) => (
            <Link
              key={index}
              to={feature.link}
              className="card card-hover group fade-in"
              style={{ animationDelay: `${index * 0.15}s` }}
            >
              <div className={`w-14 h-14 bg-gradient-to-br ${feature.color} rounded-xl flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform`}>
                {feature.icon}
              </div>
              <h3 className="text-xl font-display font-semibold text-neutral-darker mb-2">
                {feature.title}
              </h3>
              <p className="text-neutral-darkGray mb-4">
                {feature.description}
              </p>
              <div className="flex items-center text-primary font-medium group-hover:translate-x-2 transition-transform">
                Get started <FiArrowRight className="ml-2" />
              </div>
            </Link>
          ))}
        </div>

        {/* Information Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Validation Tests */}
          <div className="card fade-in">
            <div className="flex items-center mb-4">
              <div className="w-10 h-10 bg-success/10 rounded-lg flex items-center justify-center mr-3">
                <FiCheckCircle className="text-success text-xl" />
              </div>
              <h3 className="text-xl font-display font-semibold text-neutral-darker">
                Statistical Validation
              </h3>
            </div>
            <ul className="space-y-2">
              {validationTests.map((test, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-primary mr-2">✓</span>
                  <span className="text-sm text-neutral-darkGray">{test}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Quick Start Guide */}
          <div className="card fade-in bg-gradient-to-br from-primary-pale to-white border-l-4 border-primary">
            <div className="flex items-center mb-4">
              <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center mr-3">
                <FiTrendingUp className="text-primary text-xl" />
              </div>
              <h3 className="text-xl font-display font-semibold text-neutral-darker">
                Quick Start Guide
              </h3>
            </div>
            <ol className="space-y-3">
              <li className="flex items-start">
                <span className="bg-primary text-white w-6 h-6 rounded-full flex items-center justify-center text-sm mr-3 flex-shrink-0 mt-0.5">
                  1
                </span>
                <div>
                  <p className="font-medium text-neutral-darker">Define Your Model</p>
                  <p className="text-sm text-neutral-darkGray">Create constructs and items for your research model</p>
                </div>
              </li>
              <li className="flex items-start">
                <span className="bg-primary text-white w-6 h-6 rounded-full flex items-center justify-center text-sm mr-3 flex-shrink-0 mt-0.5">
                  2
                </span>
                <div>
                  <p className="font-medium text-neutral-darker">Set Parameters</p>
                  <p className="text-sm text-neutral-darkGray">Customize mean, SD, skewness, kurtosis for each item</p>
                </div>
              </li>
              <li className="flex items-start">
                <span className="bg-primary text-white w-6 h-6 rounded-full flex items-center justify-center text-sm mr-3 flex-shrink-0 mt-0.5">
                  3
                </span>
                <div>
                  <p className="font-medium text-neutral-darker">Validate & Generate</p>
                  <p className="text-sm text-neutral-darkGray">Pre-check criteria, then generate your dataset</p>
                </div>
              </li>
              <li className="flex items-start">
                <span className="bg-primary text-white w-6 h-6 rounded-full flex items-center justify-center text-sm mr-3 flex-shrink-0 mt-0.5">
                  4
                </span>
                <div>
                  <p className="font-medium text-neutral-darker">Export & Analyze</p>
                  <p className="text-sm text-neutral-darkGray">Download in your preferred format for analysis</p>
                </div>
              </li>
            </ol>
          </div>
        </div>

        {/* Supported Software */}
        <div className="card fade-in bg-gradient-to-r from-primary to-primary-dark text-white">
          <h3 className="text-2xl font-display font-semibold mb-4">
            Compatible with Leading Statistical Software
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {['SmartPLS 4.0', 'SPSS/AMOS', 'R/RStudio', 'fsQCA', 'Excel'].map((software, index) => (
              <div key={index} className="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center hover:bg-white/20 transition-colors">
                <p className="font-medium">{software}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Educational Notice */}
        <div className="mt-6 card bg-warning/10 border-l-4 border-warning fade-in">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <div className="w-10 h-10 bg-warning/20 rounded-lg flex items-center justify-center">
                <span className="text-xl">📚</span>
              </div>
            </div>
            <div className="ml-4">
              <h4 className="font-semibold text-neutral-darker mb-1">Educational Purpose Only</h4>
              <p className="text-sm text-neutral-darkGray">
                This tool generates synthetic data for teaching and learning statistical methods.
                Not intended for actual research publication or academic dishonesty.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
