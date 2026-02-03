import React from 'react'

export default function HomePage({ onStartAssessment }) {
  return (
    <div className="container">
      <div className="header">
        <h1>Mental Health Symptom Triage</h1>
        <p>Professional Assessment Tool</p>
      </div>

      <div className="section">
        <h2 className="section-title">Welcome</h2>
        <p style={{ fontSize: '1.1em', color: '#666', lineHeight: '1.6', marginBottom: '20px' }}>
          This assessment tool is designed to help evaluate your mental health symptoms and provide 
          personalized recommendations for appropriate care levels. Your responses are confidential 
          and will help you understand your current mental health status.
        </p>
      </div>

      <div className="section">
        <h2 className="section-title">What to Expect</h2>
        <div style={{ marginBottom: '15px' }}>
          <h3 style={{ color: '#667eea', marginBottom: '10px' }}>Assessment Questions</h3>
          <p style={{ color: '#666' }}>
            You'll answer 10 questions about your mood, anxiety, sleep, and overall functioning. 
            The assessment takes approximately 5-10 minutes to complete.
          </p>
        </div>
        <div style={{ marginBottom: '15px' }}>
          <h3 style={{ color: '#667eea', marginBottom: '10px' }}>Risk Assessment</h3>
          <p style={{ color: '#666' }}>
            Based on your responses, we'll calculate your risk level and determine the appropriate 
            level of care (Low, Mild, Moderate, Severe, or Critical).
          </p>
        </div>
        <div>
          <h3 style={{ color: '#667eea', marginBottom: '10px' }}>Personalized Recommendations</h3>
          <p style={{ color: '#666' }}>
            You'll receive specific recommendations for mental health care, resources, and next steps 
            based on your assessment results.
          </p>
        </div>
      </div>

      <div className="section">
        <h2 className="section-title">Important Information</h2>
        <div className="alert alert-critical">
          <strong>⚠️ Crisis Support:</strong> If you're in immediate danger or having thoughts of 
          self-harm, please call 911 or the National Suicide Prevention Lifeline at 988.
        </div>
        <p style={{ color: '#666', marginTop: '15px' }}>
          This assessment tool is not a substitute for professional medical advice, diagnosis, or treatment. 
          Always consult with a qualified mental health professional for proper evaluation and care.
        </p>
      </div>

      <div style={{ textAlign: 'center', marginTop: '40px' }}>
        <button className="btn btn-primary" onClick={onStartAssessment}>
          Start Assessment
        </button>
      </div>

      <div style={{ marginTop: '30px', padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
        <h3 style={{ color: '#667eea', marginBottom: '10px' }}>Emergency Resources</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '15px' }}>
          <div>
            <strong style={{ color: '#333' }}>National Suicide Prevention Lifeline</strong>
            <p style={{ color: '#666', margin: '5px 0' }}>Call or text: <strong>988</strong></p>
          </div>
          <div>
            <strong style={{ color: '#333' }}>Crisis Text Line</strong>
            <p style={{ color: '#666', margin: '5px 0' }}>Text: <strong>HELLO to 741741</strong></p>
          </div>
          <div>
            <strong style={{ color: '#333' }}>Emergency Services</strong>
            <p style={{ color: '#666', margin: '5px 0' }}>Call: <strong>911</strong></p>
          </div>
        </div>
      </div>
    </div>
  )
}
