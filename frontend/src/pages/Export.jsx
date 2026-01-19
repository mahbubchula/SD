import { useState, useEffect } from 'react'
import { FiDownload, FiFile, FiCheckCircle, FiAlertCircle } from 'react-icons/fi'
import axios from 'axios'
import { toast } from 'react-toastify'

const Export = () => {
  const [generatedData, setGeneratedData] = useState(null)
  const [validation, setValidation] = useState(null)
  const [constructs, setConstructs] = useState({})
  const [exporting, setExporting] = useState(null)

  const formats = [
    {
      name: 'CSV',
      value: 'csv',
      description: 'Universal format for all software',
      icon: '📊',
      features: ['Compatible with Excel, SPSS, R, Python', 'Lightweight file size', 'Easy to share']
    },
    {
      name: 'Excel',
      value: 'excel',
      description: 'Multiple sheets with metadata',
      icon: '📗',
      features: ['Multiple sheets', 'Validation results included', 'Professional formatting']
    },
    {
      name: 'SPSS',
      value: 'spss',
      description: 'SPSS-compatible with syntax',
      icon: '📈',
      features: ['Variable labels', 'Value labels', 'Syntax file for import']
    },
    {
      name: 'SmartPLS',
      value: 'smartpls',
      description: 'Direct import to SmartPLS 4.0',
      icon: '🎯',
      features: ['Ready for PLS-SEM analysis', 'Model specification included', 'Quick-start guide']
    },
    {
      name: 'JSON',
      value: 'json',
      description: 'Full metadata and validation results',
      icon: '📋',
      features: ['Complete data structure', 'Programmatic access', 'All metadata included']
    },
  ]

  // Load data from localStorage on mount
  useEffect(() => {
    const savedData = localStorage.getItem('generated_data')
    const savedValidation = localStorage.getItem('validation_results')
    const savedConstructs = localStorage.getItem('constructs')

    console.log('=== EXPORT PAGE LOADING ===')
    console.log('Raw Constructs from localStorage:', savedConstructs)

    if (savedData) {
      const parsedData = JSON.parse(savedData)
      setGeneratedData(parsedData)
      console.log('Loaded Data - Columns:', Object.keys(parsedData[0] || {}))
      console.log('Total Items in Data:', Object.keys(parsedData[0] || {}).length)
    }
    
    if (savedValidation) setValidation(JSON.parse(savedValidation))
    
    if (savedConstructs) {
      const parsedConstructs = JSON.parse(savedConstructs)
      console.log('Parsed Constructs:', parsedConstructs)
      
      // 🔧 FIX: Convert array format to dict format for backend
      if (Array.isArray(parsedConstructs)) {
        const constructsDict = {}
        parsedConstructs.forEach(c => {
          constructsDict[c.name] = {
            items: c.items
          }
        })
        console.log('Converted to Dict Format:', constructsDict)
        setConstructs(constructsDict)
      } else {
        setConstructs(parsedConstructs)
      }
    }
    console.log('===========================')
  }, [])

  const handleExport = async (format) => {
    if (!generatedData || generatedData.length === 0) {
      toast.error('No data available to export. Please generate data first.')
      return
    }

    setExporting(format.value)

    try {
      const token = localStorage.getItem('token')
      const exportData = {
        data: generatedData,
        format: format.value,
        filename: `survey_data_${new Date().toISOString().split('T')[0]}`,
        include_metadata: true,
        constructs: constructs,
        validation_results: validation || {}
      }

      const response = await axios.post(
        `${API_URL}/api/export/download`,
        exportData,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          responseType: 'blob'
        }
      )

      // Create download link
      const blob = new Blob([response.data], {
        type: response.headers['content-type']
      })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url

      // Extract filename from content-disposition or use default
      const contentDisposition = response.headers['content-disposition']
      let filename = exportData.filename + '.' + format.value
      if (contentDisposition) {
        const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition)
        if (matches != null && matches[1]) {
          filename = matches[1].replace(/['"]/g, '')
        }
      }

      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)

      toast.success(`Successfully exported data as ${format.name}!`)
    } catch (error) {
      console.error('Export error:', error)
      toast.error(error.response?.data?.detail || `Failed to export as ${format.name}`)
    } finally {
      setExporting(null)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Export Data
          </h1>
          <p className="text-gray-600">
            Download your generated survey data in multiple formats
          </p>
        </div>

        {/* Data Status */}
        <div className={`mb-6 p-4 rounded-lg border-l-4 ${
          generatedData && generatedData.length > 0
            ? 'bg-green-50 border-green-500'
            : 'bg-yellow-50 border-yellow-500'
        }`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              {generatedData && generatedData.length > 0 ? (
                <>
                  <FiCheckCircle className="text-green-500 text-xl mr-3" />
                  <div>
                    <p className="font-semibold text-green-900">
                      Data Ready for Export
                    </p>
                    <p className="text-sm text-green-700">
                      {generatedData.length} samples • {Object.keys(constructs).length} constructs • {
                        Object.keys(generatedData[0] || {}).filter(k => !k.startsWith('DEM_')).length
                      } items
                    </p>
                  </div>
                </>
              ) : (
                <>
                  <FiAlertCircle className="text-yellow-500 text-xl mr-3" />
                  <div>
                    <p className="font-semibold text-yellow-900">
                      No Data Available
                    </p>
                    <p className="text-sm text-yellow-700">
                      Please generate data first using the Generator page
                    </p>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Show what will be exported */}
        {generatedData && generatedData.length > 0 && (
          <div className="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <h3 className="font-semibold text-blue-900 mb-2">📋 Export Preview:</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-blue-800"><strong>Samples:</strong> {generatedData.length}</p>
                <p className="text-blue-800"><strong>Constructs:</strong> {Object.keys(constructs).length}</p>
              </div>
              <div>
                <p className="text-blue-800"><strong>Total Columns:</strong> {Object.keys(generatedData[0] || {}).length}</p>
                <p className="text-blue-800"><strong>Item Columns:</strong> {
                  Object.keys(generatedData[0] || {}).filter(k => !k.startsWith('DEM_')).length
                }</p>
              </div>
            </div>
            <div className="mt-3 pt-3 border-t border-blue-300">
              <p className="font-semibold text-blue-900 mb-1">Item Names:</p>
              <div className="flex flex-wrap gap-1">
                {Object.keys(generatedData[0] || {})
                  .filter(k => !k.startsWith('DEM_'))
                  .map(item => (
                    <span key={item} className="px-2 py-1 bg-white text-blue-700 rounded text-xs font-mono border border-blue-300">
                      {item}
                    </span>
                  ))}
              </div>
            </div>
          </div>
        )}

        {/* Export Formats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {formats.map((format) => (
            <div
              key={format.value}
              className="bg-white rounded-xl shadow-lg p-6 border border-gray-200 hover:shadow-xl transition-shadow"
            >
              <div className="text-5xl mb-4">{format.icon}</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">{format.name}</h3>
              <p className="text-gray-600 mb-4">{format.description}</p>

              <div className="mb-4">
                <p className="text-sm font-semibold text-gray-700 mb-2">Features:</p>
                <ul className="text-sm text-gray-600 space-y-1">
                  {format.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-green-500 mr-2">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              <button
                onClick={() => handleExport(format)}
                disabled={!generatedData || generatedData.length === 0 || exporting === format.value}
                className={`w-full py-3 px-4 rounded-lg font-semibold flex items-center justify-center transition-colors ${
                  !generatedData || generatedData.length === 0
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : exporting === format.value
                    ? 'bg-gray-400 text-white cursor-wait'
                    : 'bg-orange-500 text-white hover:bg-orange-600'
                }`}
              >
                {exporting === format.value ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Exporting...
                  </>
                ) : (
                  <>
                    <FiDownload className="mr-2" />
                    Export as {format.name}
                  </>
                )}
              </button>
            </div>
          ))}
        </div>

        {/* Additional Information */}
        <div className="mt-8 bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">Export Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
            <div>
              <p className="font-semibold mb-2">What's Included:</p>
              <ul className="space-y-1">
                <li>• All generated survey data</li>
                <li>• Construct definitions</li>
                <li>• Item specifications</li>
                <li>• Validation results</li>
              </ul>
            </div>
            <div>
              <p className="font-semibold mb-2">File Formats:</p>
              <ul className="space-y-1">
                <li>• CSV: .csv file</li>
                <li>• Excel: .xlsx with multiple sheets</li>
                <li>• SPSS: .zip with .csv and .sps syntax</li>
                <li>• SmartPLS: .zip with data and guide</li>
                <li>• JSON: .json with complete metadata</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Export
