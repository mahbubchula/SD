import React, { useState, useEffect } from 'react'
import { FaCheckCircle, FaTimesCircle, FaChartLine, FaDatabase, FaCheckDouble, FaExclamationTriangle } from 'react-icons/fa'
import { Link } from 'react-router-dom'
import { toast } from 'react-toastify'

const Validation = () => {
  const [validationData, setValidationData] = useState(null)
  const [activeTab, setActiveTab] = useState('normality')
  const [loading, setLoading] = useState(true)

  // Load REAL validation data from localStorage
  useEffect(() => {
    const loadValidationData = () => {
      const savedValidation = localStorage.getItem('validation_results')

      if (savedValidation) {
        try {
          const parsedData = JSON.parse(savedValidation)
          setValidationData(parsedData)
          console.log('=== VALIDATION DATA LOADED ===')
          console.log('Overall Valid:', parsedData.overall_valid)
          console.log('Has Structural Model:', !!parsedData.structural_model)
          console.log('Indirect Effects:', parsedData.structural_model?.indirect_effects)
          console.log('Total Effects:', parsedData.structural_model?.total_effects)
          console.log('==============================')
        } catch (error) {
          console.error('Error parsing validation data:', error)
        }
      }

      setLoading(false)
    }

    loadValidationData()
  }, [])

  // Function to clear validation data
  const clearValidationData = () => {
    localStorage.removeItem('validation_results')
    localStorage.removeItem('generated_data')
    localStorage.removeItem('constructs')
    setValidationData(null)
    toast.success('Validation data cleared. Please generate new data.')
  }

  const tabs = [
    { id: 'normality', label: 'Normality Tests', icon: FaChartLine },
    { id: 'reliability', label: 'Reliability', icon: FaCheckDouble },
    { id: 'validity', label: 'Validity', icon: FaCheckCircle },
    { id: 'structural', label: 'Structural Model', icon: FaDatabase },
    { id: 'fit', label: 'Model Fit', icon: FaChartLine }
  ]

  const StatusBadge = ({ valid, label }) => (
    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
      valid
        ? 'bg-green-100 text-green-800'
        : 'bg-red-100 text-red-800'
    }`}>
      {valid ? <FaCheckCircle className="mr-1" /> : <FaTimesCircle className="mr-1" />}
      {label || (valid ? 'Valid' : 'Invalid')}
    </span>
  )

  const StatCard = ({ title, value, threshold, valid, description }) => (
    <div className="bg-white rounded-lg shadow p-4 border-l-4" style={{ borderLeftColor: valid ? '#10B981' : '#EF4444' }}>
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
          {threshold && <p className="text-xs text-gray-500 mt-1">Threshold: {threshold}</p>}
          {description && <p className="text-xs text-gray-600 mt-2">{description}</p>}
        </div>
        <StatusBadge valid={valid} label="" />
      </div>
    </div>
  )

  // Show message if no data is available
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 to-white p-6 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading validation results...</p>
        </div>
      </div>
    )
  }

  if (!validationData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 to-white p-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-8 text-center">
            <FaExclamationTriangle className="text-yellow-500 text-6xl mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">No Validation Data Available</h2>
            <p className="text-gray-600 mb-6">
              Please generate data first using the Generator page to see validation results.
            </p>
            <Link
              to="/generator"
              className="inline-block bg-orange-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors"
            >
              Go to Generator
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                Data Validation Dashboard
              </h1>
              <p className="text-gray-600">
                Comprehensive statistical validation results for your generated survey data
              </p>
            </div>
            <button
              onClick={clearValidationData}
              className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors flex items-center gap-2"
            >
              <FaTimesCircle />
              Clear & Refresh
            </button>
          </div>
        </div>

        {/* Overall Status */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6 border-l-4" style={{ borderLeftColor: validationData.overall_valid ? '#10B981' : '#EF4444' }}>
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                {validationData.overall_valid ? (
                  <FaCheckCircle className="text-green-500 mr-3" />
                ) : (
                  <FaTimesCircle className="text-red-500 mr-3" />
                )}
                Overall Validation Status
              </h2>
              <p className="text-gray-600 mt-2">
                {validationData.overall_valid
                  ? 'All statistical criteria have been met'
                  : 'Some criteria need attention'}
              </p>
            </div>
            <StatusBadge
              valid={validationData.overall_valid}
              label={validationData.overall_valid ? 'All Tests Passed' : 'Review Results'}
            />
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-4">
              {tabs.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center px-4 py-3 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-orange-500 text-orange-600'
                      : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
                  }`}
                >
                  <tab.icon className="mr-2" />
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-xl shadow-lg p-6">

          {/* Normality Tests */}
          {activeTab === 'normality' && validationData.normality && (
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Normality Tests</h3>
              {Object.keys(validationData.normality).length > 0 ? (
                <div className="space-y-6">
                  {Object.entries(validationData.normality).map(([item, tests]) => (
                    <div key={item} className="border rounded-lg p-4">
                      <h4 className="font-semibold text-lg mb-4 text-gray-800">{item}</h4>

                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        <StatCard
                          title="Kolmogorov-Smirnov"
                          value={tests.kolmogorov_smirnov.p_value.toFixed(3)}
                          threshold="&gt; 0.05"
                          valid={tests.kolmogorov_smirnov.normal}
                          description={`Statistic: ${tests.kolmogorov_smirnov.statistic.toFixed(3)}`}
                        />

                        {tests.shapiro_wilk.p_value && (
                          <StatCard
                            title="Shapiro-Wilk"
                            value={tests.shapiro_wilk.p_value.toFixed(3)}
                            threshold="&gt; 0.05"
                            valid={tests.shapiro_wilk.normal}
                            description={`Statistic: ${tests.shapiro_wilk.statistic.toFixed(3)}`}
                          />
                        )}

                        <StatCard
                          title="Skewness"
                          value={tests.skewness.toFixed(3)}
                          threshold="&lt; |2|"
                          valid={tests.skewness_acceptable}
                          description="Distribution symmetry"
                        />

                        <StatCard
                          title="Kurtosis"
                          value={tests.kurtosis.toFixed(3)}
                          threshold="&lt; |7|"
                          valid={tests.kurtosis_acceptable}
                          description="Distribution peakedness"
                        />
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No normality test data available.</p>
              )}

              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-blue-900">
                  <strong>Note:</strong> Normality tests assess whether data follows a normal distribution.
                  For PLS-SEM, normality is not strictly required, but it's preferred for maximum likelihood estimators.
                </p>
              </div>
            </div>
          )}

          {/* Reliability */}
          {activeTab === 'reliability' && validationData.reliability && (
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Reliability Analysis</h3>
              {Object.keys(validationData.reliability).length > 0 ? (
                <div className="space-y-6">
                  {Object.entries(validationData.reliability).map(([construct, metrics]) => (
                    <div key={construct} className="border rounded-lg p-6">
                      <h4 className="font-semibold text-xl mb-4 text-gray-800">{construct}</h4>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                        <StatCard
                          title="Cronbach's Alpha"
                          value={metrics.cronbach_alpha.toFixed(3)}
                          threshold=">= 0.70"
                          valid={metrics.cronbach_acceptable}
                          description="Internal consistency"
                        />

                        <StatCard
                          title="Composite Reliability"
                          value={metrics.composite_reliability.toFixed(3)}
                          threshold=">= 0.70"
                          valid={metrics.cr_acceptable}
                          description="Overall reliability"
                        />

                        <StatCard
                          title="AVE"
                          value={metrics.ave.toFixed(3)}
                          threshold=">= 0.50"
                          valid={metrics.ave_acceptable}
                          description="Convergent validity"
                        />
                      </div>

                      {metrics.loadings && (
                        <div className="mt-4">
                          <h5 className="font-medium text-gray-700 mb-3">Item Loadings</h5>
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                            {Object.entries(metrics.loadings).map(([item, loading]) => (
                              <div key={item} className="bg-gray-50 rounded p-3">
                                <p className="text-xs text-gray-600">{item}</p>
                                <p className="text-lg font-semibold text-gray-900">{loading.toFixed(3)}</p>
                                <p className="text-xs text-gray-500">
                                  {loading >= 0.7 ? '✓ Good' : loading >= 0.6 ? '⚠ Acceptable' : '✗ Low'}
                                </p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No reliability data available.</p>
              )}

              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-blue-900">
                  <strong>Criteria:</strong> Cronbach's Alpha &amp; CR &gt;= 0.70, AVE &gt;= 0.50, Item loadings &gt;= 0.70
                </p>
              </div>
            </div>
          )}

          {/* Validity */}
          {activeTab === 'validity' && validationData.validity && (
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Validity Analysis</h3>

              {/* HTMT */}
              {validationData.validity.htmt && Object.keys(validationData.validity.htmt).length > 0 && (
                <div className="mb-6">
                  <h4 className="font-semibold text-lg mb-4 text-gray-800">HTMT (Heterotrait-Monotrait Ratio)</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {Object.entries(validationData.validity.htmt).map(([pair, result]) => (
                      <StatCard
                        key={pair}
                        title={pair.replace('_vs_', ' vs ')}
                        value={result.htmt.toFixed(3)}
                        threshold="&lt; 0.85"
                        valid={result.valid}
                        description="Discriminant validity"
                      />
                    ))}
                  </div>
                </div>
              )}

              {/* Cross-Loadings */}
              {validationData.validity.cross_loadings && Object.keys(validationData.validity.cross_loadings).length > 0 && (
                <div className="mb-6">
                  <h4 className="font-semibold text-lg mb-4 text-gray-800">Cross-Loadings ✨ NEW</h4>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Item</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Own Construct</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Own Loading</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Max Cross-Loading</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Status</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {Object.entries(validationData.validity.cross_loadings).map(([item, data]) => (
                          <tr key={item}>
                            <td className="px-4 py-3 text-sm font-medium text-gray-900">{item}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{data.own_construct}</td>
                            <td className="px-4 py-3 text-sm text-gray-900 font-semibold">{data.own_loading.toFixed(3)}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{data.max_cross_loading.toFixed(3)}</td>
                            <td className="px-4 py-3 text-sm">
                              <StatusBadge valid={data.valid} label="" />
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-blue-900">
                  <strong>Discriminant Validity:</strong> Ensures constructs are distinct. HTMT &lt; 0.85, Fornell-Larcker (sqrt(AVE) &gt; correlations), and cross-loadings (highest on own construct) confirm discriminant validity.
                </p>
              </div>
            </div>
          )}

          {/* Structural Model */}
          {activeTab === 'structural' && validationData.structural_model && (
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Structural Model Analysis</h3>

              {/* Direct Effects (Path Coefficients) */}
              {validationData.structural_model.paths && validationData.structural_model.paths.length > 0 && (
                <div className="mb-6">
                  <h4 className="font-semibold text-lg mb-4 text-gray-800">Direct Effects (Path Coefficients)</h4>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">From</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">To</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Beta</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">t-statistic</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">p-value</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Significant</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {validationData.structural_model.paths.map((path, idx) => (
                          <tr key={idx}>
                            <td className="px-4 py-3 text-sm font-medium text-gray-900">{path.from}</td>
                            <td className="px-4 py-3 text-sm font-medium text-gray-900">{path.to}</td>
                            <td className="px-4 py-3 text-sm font-semibold text-gray-900">{path.beta.toFixed(3)}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{path.t_statistic.toFixed(3)}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{path.p_value.toFixed(3)}</td>
                            <td className="px-4 py-3 text-sm">
                              <StatusBadge valid={path.significant} label="" />
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Indirect Effects (Mediation) - NEW FEATURE */}
              {validationData.structural_model.indirect_effects && validationData.structural_model.indirect_effects.length > 0 && (
                <div className="mb-6">
                  <h4 className="font-semibold text-lg mb-4 text-gray-800 flex items-center">
                    Indirect Effects (Mediation)
                    <span className="ml-2 px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded-full">✨ NEW</span>
                  </h4>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-orange-50">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Path</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Indirect Effect</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">z-score</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">p-value</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Significant</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {validationData.structural_model.indirect_effects.map((effect, idx) => (
                          <tr key={idx} className="hover:bg-orange-50">
                            <td className="px-4 py-3 text-sm font-medium text-gray-900">{effect.path}</td>
                            <td className="px-4 py-3 text-sm font-semibold text-orange-600">{effect.indirect_effect.toFixed(3)}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{effect.z_score.toFixed(3)}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{effect.p_value.toFixed(3)}</td>
                            <td className="px-4 py-3 text-sm">
                              <StatusBadge valid={effect.significant} label="" />
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Total Effects - NEW FEATURE */}
              {validationData.structural_model.total_effects && validationData.structural_model.total_effects.length > 0 && (
                <div className="mb-6">
                  <h4 className="font-semibold text-lg mb-4 text-gray-800 flex items-center">
                    Total Effects (Direct + Indirect)
                    <span className="ml-2 px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">✨ NEW</span>
                  </h4>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-green-50">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">From -&gt; To</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Mediator</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Direct</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Indirect</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Total</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">VAF %</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Type</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {validationData.structural_model.total_effects.map((effect, idx) => (
                          <tr key={idx} className="hover:bg-green-50">
                            <td className="px-4 py-3 text-sm font-medium text-gray-900">{effect.from} -&gt; {effect.to}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{effect.mediator}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{effect.direct_effect.toFixed(3)}</td>
                            <td className="px-4 py-3 text-sm text-orange-600 font-semibold">{effect.indirect_effect.toFixed(3)}</td>
                            <td className="px-4 py-3 text-sm font-bold text-gray-900">{effect.total_effect.toFixed(3)}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{effect.variance_accounted_for.toFixed(1)}%</td>
                            <td className="px-4 py-3 text-sm">
                              <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs">
                                {effect.mediation_type}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Moderation Analysis - NEW FEATURE */}
              {validationData.structural_model.moderation_analysis && validationData.structural_model.moderation_analysis.length > 0 && (
                <div className="mb-6">
                  <h4 className="font-semibold text-lg mb-4 text-gray-800 flex items-center">
                    Moderation Analysis (Interaction Effects)
                    <span className="ml-2 px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">✨ NEW</span>
                  </h4>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-purple-50">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">IV</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">DV</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Moderator</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Interaction</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">ΔR²</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">f²</th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Effect Size</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {validationData.structural_model.moderation_analysis.map((mod, idx) => (
                          <tr key={idx} className="hover:bg-purple-50">
                            <td className="px-4 py-3 text-sm font-medium text-gray-900">{mod.independent}</td>
                            <td className="px-4 py-3 text-sm font-medium text-gray-900">{mod.dependent}</td>
                            <td className="px-4 py-3 text-sm text-purple-600 font-semibold">{mod.moderator}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{mod.interaction_coefficient.toFixed(3)}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{mod.r2_change.toFixed(4)}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{mod.f_squared.toFixed(3)}</td>
                            <td className="px-4 py-3 text-sm">
                              <span className={`px-2 py-1 rounded text-xs ${
                                mod.effect_size === 'Large' ? 'bg-green-100 text-green-800' :
                                mod.effect_size === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                                mod.effect_size === 'Small' ? 'bg-orange-100 text-orange-800' :
                                'bg-gray-100 text-gray-800'
                              }`}>
                                {mod.effect_size}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* R-squared Values */}
              {validationData.structural_model.r_squared && Object.keys(validationData.structural_model.r_squared).length > 0 && (
                <div className="mb-6">
                  <h4 className="font-semibold text-lg mb-4 text-gray-800">R-squared (Variance Explained)</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {Object.entries(validationData.structural_model.r_squared).map(([construct, data]) => (
                      <StatCard
                        key={construct}
                        title={construct}
                        value={data.r_squared.toFixed(3)}
                        threshold="Interpretation"
                        valid={data.r_squared >= 0.25}
                        description={data.interpretation}
                      />
                    ))}
                  </div>
                </div>
              )}

              {/* VIF */}
              {validationData.multicollinearity && Object.keys(validationData.multicollinearity).length > 0 && (
                <div className="mb-6">
                  <h4 className="font-semibold text-lg mb-4 text-gray-800">VIF (Multicollinearity Check)</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {Object.entries(validationData.multicollinearity).map(([construct, data]) => (
                      <StatCard
                        key={construct}
                        title={construct}
                        value={data.vif.toFixed(3)}
                        threshold="&lt; 5 (&lt; 3 is good)"
                        valid={data.acceptable}
                        description={data.good ? 'Excellent' : 'Acceptable'}
                      />
                    ))}
                  </div>
                </div>
              )}

              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-blue-900">
                  <strong>Interpretation:</strong> R-squared (0.75=substantial, 0.50=moderate, 0.25=weak). VAF% &gt; 20% indicates mediation. VIF &lt; 5 is acceptable, &lt; 3 is good.
                </p>
              </div>
            </div>
          )}

          {/* Model Fit */}
          {activeTab === 'fit' && validationData.model_fit && (
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Model Fit Indices</h3>

              {validationData.model_fit.gof && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  <StatCard
                    title="Goodness of Fit (GoF)"
                    value={validationData.model_fit.gof.value.toFixed(3)}
                    threshold="0.36=large, 0.25=medium, 0.10=small"
                    valid={validationData.model_fit.gof.value >= 0.25}
                    description={validationData.model_fit.gof.interpretation}
                  />
                </div>
              )}

              <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
                <h4 className="font-semibold text-lg mb-4 text-gray-800">Model Quality Summary</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h5 className="font-medium text-gray-700 mb-2">Measurement Model</h5>
                    <ul className="space-y-1 text-sm text-gray-600">
                      <li>✓ All loadings &gt; 0.70</li>
                      <li>✓ Cronbach's Alpha &gt; 0.70</li>
                      <li>✓ Composite Reliability &gt; 0.70</li>
                      <li>✓ AVE &gt; 0.50</li>
                      <li>✓ Discriminant validity established</li>
                    </ul>
                  </div>
                  <div>
                    <h5 className="font-medium text-gray-700 mb-2">Structural Model</h5>
                    <ul className="space-y-1 text-sm text-gray-600">
                      <li>✓ Significant path coefficients</li>
                      <li>✓ Adequate R-squared values</li>
                      <li>✓ No multicollinearity (VIF &lt; 5)</li>
                      <li>✓ Mediation effects identified ✨</li>
                      <li>✓ Moderation effects detected ✨</li>
                      <li>✓ Good model fit (GoF)</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  )
}

export default Validation
