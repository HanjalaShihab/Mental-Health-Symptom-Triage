import { useState } from 'react'
import axios from 'axios'
import './App.css'
import AssessmentForm from './components/AssessmentForm'
import TriageResults from './components/TriageResults'
import HomePage from './components/HomePage'

function App() {
  const [currentPage, setCurrentPage] = useState('home')
  const [triageResults, setTriageResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleStartAssessment = () => {
    setCurrentPage('assessment')
  }

  const handleAssessmentSubmit = async (patientData, answers) => {
    setLoading(true)
    try {
      const response = await axios.post('http://localhost:5000/api/triage/submit', {
        patientData,
        answers
      })
      setTriageResults(response.data.data)
      setCurrentPage('results')
    } catch (error) {
      console.error('Error submitting assessment:', error)
      alert('Error submitting assessment. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleBackToHome = () => {
    setCurrentPage('home')
    setTriageResults(null)
  }

  const handleNewAssessment = () => {
    setTriageResults(null)
    setCurrentPage('assessment')
  }

  return (
    <div className="app">
      {currentPage === 'home' && (
        <HomePage onStartAssessment={handleStartAssessment} />
      )}
      {currentPage === 'assessment' && (
        <AssessmentForm 
          onSubmit={handleAssessmentSubmit}
          onCancel={handleBackToHome}
          loading={loading}
        />
      )}
      {currentPage === 'results' && triageResults && (
        <TriageResults 
          results={triageResults}
          onNewAssessment={handleNewAssessment}
          onBackToHome={handleBackToHome}
        />
      )}
    </div>
  )
}

export default App
