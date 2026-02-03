import React, { useState, useEffect } from 'react'
import axios from 'axios'

export default function AssessmentForm({ onSubmit, onCancel, loading }) {
  const [patientData, setPatientData] = useState({
    name: '',
    age: '',
    id: ''
  })
  
  const [questions, setQuestions] = useState([])
  const [answers, setAnswers] = useState({})
  const [currentStep, setCurrentStep] = useState('patient-info')
  const [questionsLoading, setQuestionsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    // Fetch questions from backend
    const fetchQuestions = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/assessment/questions')
        setQuestions(response.data.data)
        setQuestionsLoading(false)
      } catch (err) {
        console.error('Error fetching questions:', err)
        setError('Failed to load assessment questions')
        setQuestionsLoading(false)
      }
    }

    fetchQuestions()
  }, [])

  const handlePatientDataChange = (e) => {
    const { name, value } = e.target
    setPatientData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handlePatientDataSubmit = (e) => {
    e.preventDefault()
    if (!patientData.name || !patientData.age) {
      setError('Please fill in all patient information')
      return
    }
    
    if (isNaN(patientData.age) || patientData.age < 1 || patientData.age > 150) {
      setError('Please enter a valid age')
      return
    }

    const id = `PAT-${Date.now()}`
    setPatientData(prev => ({ ...prev, id }))
    setError('')
    setCurrentStep('assessment')
  }

  const handleAnswerChange = (questionId, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: value
    }))
  }

  const handleAssessmentSubmit = async (e) => {
    e.preventDefault()
    
    // Check if all questions are answered
    if (Object.keys(answers).length !== questions.length) {
      setError('Please answer all questions')
      return
    }

    // Convert answers to the format expected by backend
    const answersArray = questions.map(q => ({
      questionId: q.id,
      category: q.category,
      value: parseInt(answers[q.id])
    }))

    onSubmit(patientData, answersArray)
  }

  if (questionsLoading) {
    return (
      <div className="container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading assessment...</p>
        </div>
      </div>
    )
  }

  if (currentStep === 'patient-info') {
    return (
      <div className="container">
        <div className="header">
          <h1>Patient Information</h1>
          <p>Please provide your information to begin the assessment</p>
        </div>

        {error && <div className="alert alert-critical">{error}</div>}

        <form onSubmit={handlePatientDataSubmit}>
          <div className="form-group">
            <label htmlFor="name">Full Name *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={patientData.name}
              onChange={handlePatientDataChange}
              placeholder="Enter your full name"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="age">Age *</label>
            <input
              type="number"
              id="age"
              name="age"
              value={patientData.age}
              onChange={handlePatientDataChange}
              placeholder="Enter your age"
              min="1"
              max="150"
              required
            />
          </div>

          <div className="form-buttons">
            <button type="button" className="btn btn-secondary" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              Continue to Assessment
            </button>
          </div>
        </form>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="header">
        <h1>Mental Health Assessment:</h1>
        <p>Patient: {patientData.name} (Age: {patientData.age})</p>
      </div>

      {error && <div className="alert alert-critical">{error}</div>}

      <form onSubmit={handleAssessmentSubmit}>
        <div style={{ marginBottom: '30px' }}>
          <div style={{ 
            backgroundColor: '#e8eef7', 
            padding: '10px 15px', 
            borderRadius: '5px',
            marginBottom: '20px'
          }}>
            Progress: {Object.keys(answers).length} of {questions.length} questions answered
          </div>

          {questions.map((question, index) => (
            <div key={question.id} className="question-container">
              <div className="question-text">
                {index + 1}. {question.question}
              </div>
              <div className="options">
                {question.options.map((option) => (
                  <div 
                    key={option.value} 
                    className={`option ${answers[question.id] === String(option.value) ? 'selected' : ''}`}
                  >
                    <input
                      type="radio"
                      id={`q${question.id}-opt${option.value}`}
                      name={`question-${question.id}`}
                      value={option.value}
                      checked={answers[question.id] === String(option.value)}
                      onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                    />
                    <label htmlFor={`q${question.id}-opt${option.value}`}>
                      {option.label}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="form-buttons">
          <button 
            type="button" 
            className="btn btn-secondary" 
            onClick={onCancel}
            disabled={loading}
          >
            Cancel
          </button>
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={loading || Object.keys(answers).length !== questions.length}
          >
            {loading ? 'Processing...' : 'Submit Assessment'}
          </button>
        </div>
      </form>
    </div>
  )
}
