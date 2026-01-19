import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import { FiPlus, FiTrash2, FiDatabase, FiCheckCircle, FiAlertCircle, FiDownload } from 'react-icons/fi'
import axios from 'axios'
import API_URL from '../config'

const Generator = () => {
  const [constructs, setConstructs] = useState([])
  const [paths, setPaths] = useState([])
  const [sampleSize, setSampleSize] = useState(300)
  const [likertScale, setLikertScale] = useState(7)
  const [generatedData, setGeneratedData] = useState(null)
  const [validation, setValidation] = useState(null)
  const [loading, setLoading] = useState(false)

  // Load template model (TAM example)
  const loadTemplate = (templateName) => {
    if (templateName === 'TAM') {
      const tamConstructs = [
        {
          id: Date.now(),
          name: 'PerceivedUsefulness',
          items: [
            { name: 'PU1', mean: 5.2, std: 1.1, skewness: -0.3, kurtosis: 0.1 },
            { name: 'PU2', mean: 5.0, std: 1.2, skewness: -0.2, kurtosis: 0.0 },
            { name: 'PU3', mean: 5.1, std: 1.0, skewness: -0.4, kurtosis: 0.2 },
            { name: 'PU4', mean: 5.3, std: 1.1, skewness: -0.3, kurtosis: 0.1 }
          ]
        },
        {
          id: Date.now() + 1,
          name: 'PerceivedEaseOfUse',
          items: [
            { name: 'PEOU1', mean: 4.8, std: 1.3, skewness: -0.1, kurtosis: 0.0 },
            { name: 'PEOU2', mean: 4.9, std: 1.2, skewness: -0.2, kurtosis: 0.1 },
            { name: 'PEOU3', mean: 5.0, std: 1.1, skewness: -0.3, kurtosis: 0.2 }
          ]
        },
        {
          id: Date.now() + 2,
          name: 'IntentionToUse',
          items: [
            { name: 'ITU1', mean: 4.7, std: 1.4, skewness: -0.1, kurtosis: 0.0 },
            { name: 'ITU2', mean: 4.8, std: 1.3, skewness: -0.2, kurtosis: 0.1 },
            { name: 'ITU3', mean: 4.9, std: 1.2, skewness: -0.3, kurtosis: 0.2 }
          ]
        }
      ]

      const tamPaths = [
        {
          id: Date.now(),
          from: 'PerceivedUsefulness',
          to: 'IntentionToUse',
          beta: 0.45,
          significant: true,
          path_type: 'direct'
        },
        {
          id: Date.now() + 1,
          from: 'PerceivedUsefulness',
          to: 'PerceivedEaseOfUse',
          beta: 0.38,
          significant: true,
          path_type: 'mediation'
        },
        {
          id: Date.now() + 2,
          from: 'PerceivedEaseOfUse',
          to: 'IntentionToUse',
          beta: 0.32,
          significant: true,
          path_type: 'mediation'
        }
      ]

      setConstructs(tamConstructs)
      setPaths(tamPaths)
      toast.success('TAM template loaded! This model will show indirect effects.')
    }
  }

  // Generate proper item name based on construct name
  const generateItemName = (constructName, itemIndex) => {
    // Convert construct name to abbreviation
    // Handle names like "Construct1" -> "C1", "Construct2" -> "C2"
    // Or "PerceivedUsefulness" -> "PU", "IntentionToUse" -> "ITU"
    
    // Check if it's a generic construct name (Construct1, Construct2, etc.)
    const genericMatch = constructName.match(/^Construct(\d+)$/i)
    if (genericMatch) {
      // Use construct number as prefix: C1_Item1, C1_Item2, C2_Item1, etc.
      const constructNum = genericMatch[1]
      return `C${constructNum}_${itemIndex + 1}`
    }
    
    // For named constructs, create abbreviation from capital letters or first letters
    const words = constructName.replace(/([A-Z])/g, ' $1').trim().split(/\s+/)
    let abbreviation = words.map(word => word[0].toUpperCase()).join('')
    
    // If abbreviation is too short, take first 2-4 chars of construct name
    if (abbreviation.length < 2) {
      abbreviation = constructName.substring(0, Math.min(4, constructName.length)).toUpperCase()
    }
    
    return `${abbreviation}${itemIndex + 1}`
  }

  // Regenerate all item names for a construct
  const regenerateItemNames = (construct) => {
    return {
      ...construct,
      items: construct.items.map((item, index) => ({
        ...item,
        name: generateItemName(construct.name, index)
      }))
    }
  }

  // Add new construct
  const addConstruct = () => {
    const constructNumber = constructs.length + 1
    const constructName = `Construct${constructNumber}`
    const newConstruct = {
      id: Date.now(),
      name: constructName,
      items: [
        { name: generateItemName(constructName, 0), mean: 4.0, std: 1.0, skewness: 0.0, kurtosis: 0.0 },
        { name: generateItemName(constructName, 1), mean: 4.0, std: 1.0, skewness: 0.0, kurtosis: 0.0 },
        { name: generateItemName(constructName, 2), mean: 4.0, std: 1.0, skewness: 0.0, kurtosis: 0.0 }
      ]
    }
    setConstructs([...constructs, newConstruct])
  }

  // Remove construct
  const removeConstruct = (id) => {
    setConstructs(constructs.filter(c => c.id !== id))
    // Remove related paths
    setPaths(paths.filter(p => {
      const construct = constructs.find(c => c.id === id)
      return p.from !== construct?.name && p.to !== construct?.name
    }))
  }

  // Update construct name and regenerate item names
  const updateConstructName = (id, name) => {
    setConstructs(constructs.map(c => {
      if (c.id === id) {
        const updatedConstruct = { ...c, name }
        return regenerateItemNames(updatedConstruct)
      }
      return c
    }))
    
    // Update paths that use this construct
    const oldConstruct = constructs.find(c => c.id === id)
    if (oldConstruct) {
      setPaths(paths.map(p => ({
        ...p,
        from: p.from === oldConstruct.name ? name : p.from,
        to: p.to === oldConstruct.name ? name : p.to
      })))
    }
  }

  // Add item to construct
  const addItem = (constructId) => {
    setConstructs(constructs.map(c => {
      if (c.id === constructId) {
        const newItemIndex = c.items.length
        return {
          ...c,
          items: [...c.items, {
            name: generateItemName(c.name, newItemIndex),
            mean: 4.0,
            std: 1.0,
            skewness: 0.0,
            kurtosis: 0.0
          }]
        }
      }
      return c
    }))
  }

  // Remove item and regenerate names
  const removeItem = (constructId, itemIndex) => {
    setConstructs(constructs.map(c => {
      if (c.id === constructId && c.items.length > 1) {
        const newItems = c.items.filter((_, i) => i !== itemIndex)
        // Regenerate all item names to maintain sequence
        return {
          ...c,
          items: newItems.map((item, index) => ({
            ...item,
            name: generateItemName(c.name, index)
          }))
        }
      }
      return c
    }))
  }

  // Update item
  const updateItem = (constructId, itemIndex, field, value) => {
    setConstructs(constructs.map(c => {
      if (c.id === constructId) {
        const newItems = [...c.items]
        newItems[itemIndex] = { ...newItems[itemIndex], [field]: parseFloat(value) || value }
        return { ...c, items: newItems }
      }
      return c
    }))
  }

  // Add path
  const addPath = () => {
    if (constructs.length < 2) {
      toast.error('Add at least 2 constructs first')
      return
    }
    setPaths([...paths, {
      id: Date.now(),
      from: constructs[0].name,
      to: constructs[1].name,
      beta: 0.3,
      significant: true
    }])
  }

  // Remove path
  const removePath = (id) => {
    setPaths(paths.filter(p => p.id !== id))
  }

  // Update path
  const updatePath = (id, field, value) => {
    setPaths(paths.map(p => {
      if (p.id === id) {
        return { ...p, [field]: field === 'beta' ? parseFloat(value) : value }
      }
      return p
    }))
  }

  // Generate data
  const generateData = async () => {
    if (constructs.length === 0) {
      toast.error('Please add at least one construct')
      return
    }

    if (constructs.some(c => c.items.length === 0)) {
      toast.error('Each construct must have at least one item')
      return
    }

    setLoading(true)

    try {
      const token = localStorage.getItem('token')
      
      if (!token) {
        toast.error('Please login again')
        navigate('/login')
        return
      }

      const requestData = {
        sample_size: sampleSize,
        constructs: constructs.map(c => ({
          name: c.name,
          items: c.items
        })),
        paths: paths.map(p => ({
          from: p.from,
          to: p.to,
          beta: p.beta,
          significant: p.significant,
          path_type: p.path_type || 'direct'
        })),
        likert_scale: likertScale,
        add_noise: true,
        noise_level: 0.05
      }

      // 🔍 DEBUG: Log request
      console.log('=== GENERATION REQUEST ===')
      console.log('Constructs Count:', requestData.constructs.length)
      console.log('Constructs:', requestData.constructs)
      console.log('Total Items:', requestData.constructs.reduce((sum, c) => sum + c.items.length, 0))
      console.log('Paths:', requestData.paths)
      console.log('=========================')

      const response = await axios.post(
        `${API_URL}/api/generate/generate`,
        requestData,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )

      // 🔍 DEBUG: Log full API response
      console.log('=== FULL API RESPONSE ===')
      console.log('Response Data Length:', response.data.data.length)
      console.log('First Row:', response.data.data[0])
      console.log('First Row Keys (All Columns):', Object.keys(response.data.data[0]))
      console.log('Column Count:', Object.keys(response.data.data[0]).length)
      console.log('Validation Structure:', Object.keys(response.data.validation))
      console.log('Structural Model:', response.data.validation.structural_model)
      console.log('Indirect Effects:', response.data.validation.structural_model?.indirect_effects)
      console.log('Total Effects:', response.data.validation.structural_model?.total_effects)
      
      // Check if we have all items
      const expectedItemNames = constructs.flatMap(c => c.items.map(i => i.name))
      const actualItemNames = Object.keys(response.data.data[0]).filter(k => !k.startsWith('DEM_'))
      console.log('Expected Item Names:', expectedItemNames)
      console.log('Actual Item Names in Data:', actualItemNames)
      console.log('Missing Items:', expectedItemNames.filter(name => !actualItemNames.includes(name)))
      console.log('=========================')

      setGeneratedData(response.data.data)
      setValidation(response.data.validation)

      // Save to localStorage for Export page
      localStorage.setItem('generated_data', JSON.stringify(response.data.data))
      localStorage.setItem('validation_results', JSON.stringify(response.data.validation))

      // 🔧 FIX: Save constructs as array with all item details
      localStorage.setItem('constructs', JSON.stringify(constructs))

      toast.success(`Generated ${response.data.data.length} samples successfully!`)

      // Scroll to results
      document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth' })

    } catch (error) {
      console.error('Generation error:', error)
      toast.error(error.response?.data?.detail || 'Failed to generate data')
    } finally {
      setLoading(false)
    }
  }

  // Export data
  const exportData = async (format) => {
    if (!generatedData) {
      toast.error('Generate data first')
      return
    }
    // 🔍 DEBUG: Check what we're sending
    console.log('=== EXPORT DEBUG ===')
    console.log('Generated Data Length:', generatedData.length)
    console.log('First Row Keys:', Object.keys(generatedData[0]))
    console.log('Constructs:', constructs)
    console.log('===================')
    try {
      const token = localStorage.getItem('token')

      const response = await axios.post(
        `${API_URL}/api/export/download`,
        {
          data: generatedData,
          format: format,
          filename: 'survey_data',
          constructs: constructs.reduce((acc, c) => {
            acc[c.name] = { items: c.items }
            return acc
          }, {}),
          validation_results: validation
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          responseType: 'blob'
        }
      )

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `survey_data.${format === 'excel' ? 'xlsx' : format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()

      toast.success(`Exported as ${format.toUpperCase()}`)
    } catch (error) {
      console.error('Export error:', error)
      toast.error('Failed to export data')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-pale/30 via-white to-primary-pale/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-display font-bold gradient-text mb-2">
            Generate Survey Data
          </h1>
          <p className="text-lg text-neutral-darkGray">
            Create statistically validated synthetic survey data for your research
          </p>
        </div>

        {/* Configuration Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Sample Size */}
          <div className="card">
            <label className="label">Sample Size</label>
            <input
              type="number"
              value={sampleSize}
              onChange={(e) => setSampleSize(parseInt(e.target.value))}
              className="input"
              min="100"
              max="10000"
            />
            <p className="text-xs text-neutral-darkGray mt-1">100 - 10,000 samples</p>
          </div>

          {/* Likert Scale */}
          <div className="card">
            <label className="label">Likert Scale</label>
            <select
              value={likertScale}
              onChange={(e) => setLikertScale(parseInt(e.target.value))}
              className="input"
            >
              <option value="5">5-point scale</option>
              <option value="7">7-point scale</option>
              <option value="10">10-point scale</option>
            </select>
            <p className="text-xs text-neutral-darkGray mt-1">Most common: 7-point</p>
          </div>

          {/* Quick Stats */}
          <div className="card bg-primary-pale">
            <div className="text-sm text-neutral-darkGray mb-1">Ready to Generate</div>
            <div className="text-2xl font-bold text-primary">
              {constructs.length} Constructs
            </div>
            <div className="text-sm text-neutral-darkGray mt-2">
              {constructs.reduce((sum, c) => sum + c.items.length, 0)} Items • {paths.length} Paths
            </div>
          </div>
        </div>

        {/* Constructs Section */}
        <div className="card mb-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-display font-semibold text-neutral-darker">
              Constructs & Items
            </h2>
            <div className="flex gap-2">
              <button 
                onClick={() => loadTemplate('TAM')} 
                className="btn bg-gradient-to-r from-purple-500 to-purple-600 text-white hover:from-purple-600 hover:to-purple-700"
              >
                📚 Load TAM Template
              </button>
              <button onClick={addConstruct} className="btn btn-primary">
                <FiPlus className="mr-2" /> Add Construct
              </button>
            </div>
          </div>

          {constructs.length === 0 ? (
            <div className="text-center py-12">
              <FiDatabase className="text-5xl mx-auto mb-4 text-primary/30" />
              <p className="text-neutral-darkGray mb-4">No constructs yet. Get started:</p>
              <div className="flex justify-center gap-4">
                <button onClick={() => loadTemplate('TAM')} className="btn bg-purple-500 text-white hover:bg-purple-600">
                  📚 Load Example (TAM Model)
                </button>
                <span className="text-neutral-darkGray self-center">or</span>
                <button onClick={addConstruct} className="btn btn-primary">
                  <FiPlus className="mr-2" /> Create From Scratch
                </button>
              </div>
              <div className="mt-6 p-4 bg-blue-50 rounded-lg text-left max-w-2xl mx-auto">
                <p className="font-semibold text-blue-900 mb-2">💡 TAM Template includes:</p>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>• 3 Constructs (Perceived Usefulness, Perceived Ease of Use, Intention to Use)</li>
                  <li>• 10 Items total (PU1-PU4, PEOU1-PEOU3, ITU1-ITU3)</li>
                  <li>• 3 Paths with mediation (shows indirect effects!)</li>
                  <li>• Proper item naming convention</li>
                </ul>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {constructs.map((construct, cIndex) => (
                <div key={construct.id} className="border border-neutral-gray rounded-lg p-4 bg-white">
                  {/* Construct Header */}
                  <div className="flex justify-between items-center mb-4">
                    <input
                      type="text"
                      value={construct.name}
                      onChange={(e) => updateConstructName(construct.id, e.target.value)}
                      className="text-xl font-semibold bg-transparent border-b-2 border-primary focus:outline-none"
                    />
                    <div className="flex gap-2">
                      <button
                        onClick={() => addItem(construct.id)}
                        className="btn btn-outline text-sm py-1 px-3"
                      >
                        <FiPlus className="mr-1" /> Add Item
                      </button>
                      <button
                        onClick={() => removeConstruct(construct.id)}
                        className="btn bg-error text-white hover:bg-error-dark text-sm py-1 px-3"
                      >
                        <FiTrash2 />
                      </button>
                    </div>
                  </div>

                  {/* Items */}
                  <div className="space-y-3">
                    {construct.items.map((item, iIndex) => (
                      <div key={iIndex} className="grid grid-cols-6 gap-3 items-center bg-neutral-offWhite p-3 rounded-lg">
                        <div>
                          <label className="text-xs text-neutral-darkGray">Item Name</label>
                          <input
                            type="text"
                            value={item.name}
                            readOnly
                            className="input text-sm bg-neutral-gray/50 cursor-not-allowed font-semibold text-primary"
                            title="Auto-generated based on construct name"
                          />
                        </div>
                        <div>
                          <label className="text-xs text-neutral-darkGray">Mean</label>
                          <input
                            type="number"
                            value={item.mean}
                            onChange={(e) => updateItem(construct.id, iIndex, 'mean', e.target.value)}
                            className="input text-sm"
                            step="0.1"
                            min="1"
                            max={likertScale}
                          />
                        </div>
                        <div>
                          <label className="text-xs text-neutral-darkGray">SD</label>
                          <input
                            type="number"
                            value={item.std}
                            onChange={(e) => updateItem(construct.id, iIndex, 'std', e.target.value)}
                            className="input text-sm"
                            step="0.1"
                            min="0.1"
                            max="3"
                          />
                        </div>
                        <div>
                          <label className="text-xs text-neutral-darkGray">Skewness</label>
                          <input
                            type="number"
                            value={item.skewness}
                            onChange={(e) => updateItem(construct.id, iIndex, 'skewness', e.target.value)}
                            className="input text-sm"
                            step="0.1"
                            min="-2"
                            max="2"
                          />
                        </div>
                        <div>
                          <label className="text-xs text-neutral-darkGray">Kurtosis</label>
                          <input
                            type="number"
                            value={item.kurtosis}
                            onChange={(e) => updateItem(construct.id, iIndex, 'kurtosis', e.target.value)}
                            className="input text-sm"
                            step="0.1"
                            min="-2"
                            max="7"
                          />
                        </div>
                        <button
                          onClick={() => removeItem(construct.id, iIndex)}
                          className="btn bg-error/10 text-error hover:bg-error hover:text-white text-sm py-2"
                          disabled={construct.items.length === 1}
                        >
                          <FiTrash2 />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Paths Section */}
        <div className="card mb-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-display font-semibold text-neutral-darker">
              Structural Paths
            </h2>
            <button
              onClick={addPath}
              className="btn btn-primary"
              disabled={constructs.length < 2}
            >
              <FiPlus className="mr-2" /> Add Path
            </button>
          </div>

          {paths.length === 0 ? (
            <div className="text-center py-8 text-neutral-darkGray">
              <p>No paths defined. Add paths to create relationships between constructs.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {paths.map((path) => (
                <div key={path.id} className="grid grid-cols-6 gap-3 items-center bg-neutral-offWhite p-3 rounded-lg">
                  <div>
                    <label className="text-xs text-neutral-darkGray">From</label>
                    <select
                      value={path.from}
                      onChange={(e) => updatePath(path.id, 'from', e.target.value)}
                      className="input text-sm"
                    >
                      {constructs.map(c => (
                        <option key={c.id} value={c.name}>{c.name}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="text-xs text-neutral-darkGray">To</label>
                    <select
                      value={path.to}
                      onChange={(e) => updatePath(path.id, 'to', e.target.value)}
                      className="input text-sm"
                    >
                      {constructs.map(c => (
                        <option key={c.id} value={c.name}>{c.name}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="text-xs text-neutral-darkGray">Beta (β)</label>
                    <input
                      type="number"
                      value={path.beta}
                      onChange={(e) => updatePath(path.id, 'beta', e.target.value)}
                      className="input text-sm"
                      step="0.1"
                      min="-1"
                      max="1"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-neutral-darkGray">Relationship</label>
                    <select
                      value={path.path_type || 'direct'}
                      onChange={(e) => updatePath(path.id, 'path_type', e.target.value)}
                      className="input text-sm"
                    >
                      <option value="direct">Direct</option>
                      <option value="mediation">Mediation</option>
                      <option value="moderation">Moderation</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-xs text-neutral-darkGray">Significant</label>
                    <select
                      value={path.significant}
                      onChange={(e) => updatePath(path.id, 'significant', e.target.value === 'true')}
                      className="input text-sm"
                    >
                      <option value="true">Yes</option>
                      <option value="false">No</option>
                    </select>
                  </div>
                  <button
                    onClick={() => removePath(path.id)}
                    className="btn bg-error/10 text-error hover:bg-error hover:text-white text-sm py-2"
                  >
                    <FiTrash2 />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Generate Button */}
        <div className="card bg-gradient-to-r from-primary to-primary-dark text-white mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-xl font-semibold mb-1">Ready to Generate?</h3>
              <p className="text-white/90">
                {sampleSize} samples • {constructs.length} constructs • {paths.length} paths
              </p>
            </div>
            <button
              onClick={generateData}
              disabled={loading || constructs.length === 0}
              className="btn bg-white text-primary hover:bg-neutral-offWhite disabled:opacity-50 text-lg px-8 py-3"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin mr-2"></div>
                  Generating...
                </>
              ) : (
                <>
                  <FiDatabase className="mr-2" /> Generate Data
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results Section */}
        {generatedData && (
          <div id="results-section" className="space-y-6">
            {/* Validation Results */}
            <div className="card">
              <h2 className="text-2xl font-display font-semibold text-neutral-darker mb-4">
                Validation Results
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {validation?.overall_valid ? (
                  <div className="flex items-center p-4 bg-success/10 rounded-lg border-l-4 border-success">
                    <FiCheckCircle className="text-success text-2xl mr-3" />
                    <div>
                      <div className="font-semibold text-success">All Validations Passed</div>
                      <div className="text-sm text-neutral-darkGray">Data is statistically valid</div>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-center p-4 bg-warning/10 rounded-lg border-l-4 border-warning">
                    <FiAlertCircle className="text-warning text-2xl mr-3" />
                    <div>
                      <div className="font-semibold text-warning">Some Validations Failed</div>
                      <div className="text-sm text-neutral-darkGray">Review results below</div>
                    </div>
                  </div>
                )}
              </div>

              {/* Reliability */}
              {validation?.reliability && (
                <div className="mt-6">
                  <h3 className="font-semibold text-lg mb-3">Reliability Assessment</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-neutral-offWhite">
                        <tr>
                          <th className="px-4 py-2 text-left">Construct</th>
                          <th className="px-4 py-2 text-center">Cronbach's α</th>
                          <th className="px-4 py-2 text-center">CR</th>
                          <th className="px-4 py-2 text-center">AVE</th>
                          <th className="px-4 py-2 text-center">Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(validation.reliability).map(([construct, metrics]) => (
                          <tr key={construct} className="border-t">
                            <td className="px-4 py-2 font-medium">{construct}</td>
                            <td className="px-4 py-2 text-center">{metrics.cronbach_alpha.toFixed(3)}</td>
                            <td className="px-4 py-2 text-center">{metrics.composite_reliability.toFixed(3)}</td>
                            <td className="px-4 py-2 text-center">{metrics.ave.toFixed(3)}</td>
                            <td className="px-4 py-2 text-center">
                              {metrics.cronbach_acceptable && metrics.cr_acceptable && metrics.ave_acceptable ? (
                                <span className="text-success">✓ Pass</span>
                              ) : (
                                <span className="text-error">✗ Fail</span>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>

            {/* Export Options */}
            <div className="card">
              <h2 className="text-2xl font-display font-semibold text-neutral-darker mb-4">
                Export Data
              </h2>
              
              {/* Show data structure */}
              <div className="mb-4 p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg border border-green-200">
                <h3 className="font-semibold text-green-900 mb-2">✓ Generated Data Structure:</h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-700"><strong>Total Samples:</strong> {generatedData.length}</p>
                    <p className="text-gray-700"><strong>Total Variables:</strong> {Object.keys(generatedData[0] || {}).length}</p>
                  </div>
                  <div>
                    <p className="text-gray-700"><strong>Constructs:</strong> {constructs.length}</p>
                    <p className="text-gray-700"><strong>Total Items:</strong> {constructs.reduce((sum, c) => sum + c.items.length, 0)}</p>
                  </div>
                </div>
                <div className="mt-3 pt-3 border-t border-green-300">
                  <p className="font-semibold text-green-900 mb-1">All Items Included:</p>
                  <div className="flex flex-wrap gap-2">
                    {constructs.map(c => c.items.map(item => (
                      <span key={item.name} className="px-2 py-1 bg-white text-green-700 rounded text-xs font-mono border border-green-300">
                        {item.name}
                      </span>
                    )))}
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                {['csv', 'excel', 'spss', 'smartpls', 'json'].map((format) => (
                  <button
                    key={format}
                    onClick={() => exportData(format)}
                    className="btn btn-outline group"
                  >
                    <FiDownload className="mr-2 group-hover:animate-bounce" />
                    {format.toUpperCase()}
                  </button>
                ))}
              </div>
              <div className="mt-4 p-4 bg-primary-pale rounded-lg">
                <p className="text-sm text-neutral-darkGray">
                  <strong>Note:</strong> All {constructs.reduce((sum, c) => sum + c.items.length, 0)} items will be exported as separate columns (e.g., PU1, PU2, PU3, PEOU1, PEOU2, ITU1, ITU2, etc.)
                </p>
              </div>
            </div>

            {/* Show Indirect Effects if they exist */}
            {validation?.structural_model?.indirect_effects && validation.structural_model.indirect_effects.length > 0 && (
              <div className="card bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-300">
                <h2 className="text-2xl font-display font-semibold text-purple-900 mb-4">
                  🎯 Indirect Effects Detected!
                </h2>
                <div className="space-y-3">
                  {validation.structural_model.indirect_effects.map((effect, index) => (
                    <div key={index} className="p-4 bg-white rounded-lg border border-purple-200">
                      <div className="flex justify-between items-center">
                        <div>
                          <p className="font-semibold text-purple-900">{effect.path}</p>
                          <p className="text-sm text-gray-600">
                            Indirect Effect: <span className="font-mono font-bold text-purple-700">{effect.indirect_effect.toFixed(3)}</span>
                            {effect.significant && <span className="ml-2 text-green-600">✓ Significant</span>}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-gray-500">z-score: {effect.z_score.toFixed(3)}</p>
                          <p className="text-xs text-gray-500">p-value: {effect.p_value.toFixed(4)}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-4 p-3 bg-purple-100 rounded">
                  <p className="text-sm text-purple-900">
                    💡 <strong>Mediation detected!</strong> These indirect effects will be included in your Excel export under the "Indirect_Effects" sheet.
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Generator
