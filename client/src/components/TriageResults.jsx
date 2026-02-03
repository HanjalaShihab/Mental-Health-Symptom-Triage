import React from 'react'

const getRiskLevelClass = (level) => {
  const levels = {
    CRITICAL: 'alert-critical',
    SEVERE: 'alert-severe',
    MODERATE: 'alert-moderate',
    MILD: 'alert-mild',
    LOW: 'alert-low'
  }
  return levels[level] || 'alert-low'
}

const getRiskLevelColor = (level) => {
  const colors = {
    CRITICAL: '#d32f2f',
    SEVERE: '#f57c00',
    MODERATE: '#1976d2',
    MILD: '#7b1fa2',
    LOW: '#388e3c'
  }
  return colors[level] || '#388e3c'
}

export default function TriageResults({ results, onNewAssessment, onBackToHome }) {
  const { riskAssessment, recommendations, nextSteps, patientName, patientAge } = results

  return (
    <div className="container">
      <div className="header">
        <h1>Assessment Results</h1>
        <p>Patient: {patientName} (Age: {patientAge})</p>
      </div>

      {/* Risk Level Alert */}
      <div className={`alert ${getRiskLevelClass(riskAssessment.level)}`}>
        <h2 style={{ marginBottom: '10px' }}>
          Risk Level: {riskAssessment.level}
        </h2>
        <p style={{ marginBottom: '10px' }}>
          {riskAssessment.description}
        </p>
        {riskAssessment.recommendation && (
          <p style={{ fontWeight: 'bold' }}>
            {riskAssessment.recommendation}
          </p>
        )}
      </div>

      {/* Critical Actions */}
      {riskAssessment.actions && riskAssessment.actions.length > 0 && (
        <div className="section">
          <h2 className="section-title">Immediate Actions</h2>
          <ul style={{ paddingLeft: '20px' }}>
            {riskAssessment.actions.map((action, idx) => (
              <li key={idx} style={{ marginBottom: '10px', color: '#333' }}>
                {action}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Severity Score */}
      <div className="section">
        <h2 className="section-title">Assessment Score</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
          <div style={{ padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
            <div style={{ fontSize: '0.9em', color: '#666' }}>Total Score</div>
            <div style={{ fontSize: '1.8em', fontWeight: 'bold', color: getRiskLevelColor(riskAssessment.level) }}>
              {riskAssessment.score}/{riskAssessment.maxScore}
            </div>
          </div>
          <div style={{ padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
            <div style={{ fontSize: '0.9em', color: '#666' }}>Severity Percentage</div>
            <div style={{ fontSize: '1.8em', fontWeight: 'bold', color: getRiskLevelColor(riskAssessment.level) }}>
              {riskAssessment.percentage}%
            </div>
          </div>
        </div>
      </div>

      {/* Category Breakdown */}
      <div className="section">
        <h2 className="section-title">Category Breakdown</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '15px' }}>
          {Object.entries(riskAssessment.categoryBreakdown).map(([category, score]) => (
            <div key={category} style={{ 
              padding: '15px', 
              backgroundColor: '#f8f9fa', 
              borderRadius: '5px',
              borderLeft: `4px solid ${getRiskLevelColor(riskAssessment.level)}`
            }}>
              <div style={{ fontSize: '0.9em', color: '#666', textTransform: 'capitalize' }}>
                {category}
              </div>
              <div style={{ fontSize: '1.5em', fontWeight: 'bold', color: '#333' }}>
                {score}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendations */}
      <div className="section">
        <h2 className="section-title">Recommendations</h2>
        {recommendations.map((rec, idx) => (
          <div key={idx} style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
            <h3 style={{ color: '#667eea', marginBottom: '10px', textTransform: 'capitalize' }}>
              {rec.type === 'general' ? '🎯 ' : '📋 '}
              {rec.type === 'general' ? rec.title : `${rec.category} - ${rec.description}`}
            </h3>
            {rec.type === 'general' && rec.actions && (
              <div>
                <div style={{ fontWeight: '600', marginBottom: '10px', color: '#666' }}>
                  Recommended Actions:
                </div>
                <ul style={{ paddingLeft: '20px' }}>
                  {rec.actions.map((action, i) => (
                    <li key={i} style={{ marginBottom: '8px', color: '#555' }}>
                      {action}
                    </li>
                  ))}
                </ul>
                {rec.timeframe && (
                  <div style={{ marginTop: '10px', fontStyle: 'italic', color: '#666' }}>
                    <strong>Timeframe:</strong> {rec.timeframe}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Next Steps */}
      <div className="section">
        <h2 className="section-title">Next Steps</h2>
        <div style={{ 
          backgroundColor: '#e8eef7', 
          padding: '20px', 
          borderRadius: '5px',
          borderLeft: `4px solid ${getRiskLevelColor(riskAssessment.level)}`
        }}>
          <ol style={{ paddingLeft: '20px' }}>
            {nextSteps.map((step) => (
              <li key={step.step} style={{ marginBottom: '12px', color: '#333' }}>
                <strong>Step {step.step}:</strong> {step.action}
              </li>
            ))}
          </ol>
        </div>
      </div>

      {/* Emergency Resources for Critical Cases */}
      {riskAssessment.level === 'CRITICAL' && (
        <div className="section">
          <h2 className="section-title">Crisis Resources</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '15px' }}>
            <div style={{ padding: '15px', border: '2px solid #d32f2f', borderRadius: '5px', backgroundColor: '#ffe0e0' }}>
              <div style={{ fontWeight: 'bold', color: '#d32f2f', marginBottom: '5px' }}>
                National Suicide Prevention Lifeline
              </div>
              <div style={{ fontSize: '1.3em', color: '#d32f2f', fontWeight: 'bold' }}>
                988
              </div>
              <div style={{ fontSize: '0.9em', color: '#666', marginTop: '5px' }}>
                Available 24/7, free and confidential
              </div>
            </div>
            <div style={{ padding: '15px', border: '2px solid #d32f2f', borderRadius: '5px', backgroundColor: '#ffe0e0' }}>
              <div style={{ fontWeight: 'bold', color: '#d32f2f', marginBottom: '5px' }}>
                Crisis Text Line
              </div>
              <div style={{ fontSize: '1.3em', color: '#d32f2f', fontWeight: 'bold' }}>
                TEXT: HELLO to 741741
              </div>
              <div style={{ fontSize: '0.9em', color: '#666', marginTop: '5px' }}>
                24/7 text-based crisis support
              </div>
            </div>
            <div style={{ padding: '15px', border: '2px solid #d32f2f', borderRadius: '5px', backgroundColor: '#ffe0e0' }}>
              <div style={{ fontWeight: 'bold', color: '#d32f2f', marginBottom: '5px' }}>
                Emergency Services
              </div>
              <div style={{ fontSize: '1.3em', color: '#d32f2f', fontWeight: 'bold' }}>
                911
              </div>
              <div style={{ fontSize: '0.9em', color: '#666', marginTop: '5px' }}>
                Call immediately if in danger
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="form-buttons">
        <button className="btn btn-secondary" onClick={onBackToHome}>
          Back to Home
        </button>
        <button className="btn btn-primary" onClick={onNewAssessment}>
          New Assessment
        </button>
      </div>

      {/* Disclaimer */}
      <div style={{ 
        marginTop: '30px', 
        padding: '20px', 
        backgroundColor: '#f8f9fa', 
        borderRadius: '5px',
        borderLeft: '4px solid #667eea',
        color: '#666'
      }}>
        <h3 style={{ color: '#667eea', marginBottom: '10px' }}>Important Disclaimer</h3>
        <p>
          This assessment tool provides a preliminary screening and is not a substitute for a professional 
          mental health evaluation. The results should be reviewed and discussed with a qualified mental health 
          professional. This tool does not provide medical diagnosis or treatment recommendations.
        </p>
        <p style={{ marginTop: '10px' }}>
          If you are in crisis or having thoughts of self-harm, please seek immediate help by calling 911 
          or contacting the National Suicide Prevention Lifeline at 988.
        </p>
      </div>
    </div>
  )
}
