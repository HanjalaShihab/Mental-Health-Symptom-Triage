import express from 'express';
import { v4 as uuidv4 } from 'uuid';
import { TriageService } from '../services/triageService.js';

const router = express.Router();

// Store reports in memory (in production, use database)
const triageReports = new Map();

// Submit assessment and get triage result
router.post('/submit', (req, res) => {
  try {
    const { patientData, answers } = req.body;

    // Validate input
    if (!patientData || !answers || !Array.isArray(answers)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid input: patientData and answers array are required'
      });
    }

    if (answers.length === 0) {
      return res.status(400).json({
        success: false,
        error: 'Assessment questions must be answered'
      });
    }

    // Generate report
    const report = TriageService.generateReport(patientData, answers);
    const reportId = uuidv4();
    
    // Store report
    triageReports.set(reportId, report);

    res.json({
      success: true,
      reportId,
      data: report
    });
  } catch (error) {
    console.error('Error submitting assessment:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to process assessment'
    });
  }
});

// Get triage report
router.get('/report/:reportId', (req, res) => {
  const { reportId } = req.params;
  const report = triageReports.get(reportId);

  if (!report) {
    return res.status(404).json({
      success: false,
      error: 'Report not found'
    });
  }

  res.json({
    success: true,
    data: report
  });
});

// Get emergency resources
router.get('/resources/emergency', (req, res) => {
  const emergencyResources = {
    hotlines: [
      {
        name: 'National Suicide Prevention Lifeline',
        number: '988',
        description: 'Free, confidential, 24/7'
      },
      {
        name: 'Crisis Text Line',
        number: 'Text HOME to 741741',
        description: '24/7 crisis support via text'
      },
      {
        name: 'SAMHSA National Helpline',
        number: '1-800-662-4357',
        description: 'Free, confidential, 24/7 substance abuse and mental health support'
      },
      {
        name: 'Veterans Crisis Line',
        number: '988, then press 1',
        description: 'For military veterans in crisis'
      }
    ],
    inPerson: [
      {
        type: 'Emergency Room',
        description: 'Go to nearest hospital emergency department',
        available: '24/7'
      },
      {
        type: 'Crisis Center',
        description: 'Local mental health crisis center or psychiatric urgent care',
        available: 'Check your area'
      },
      {
        type: 'Police',
        description: 'Call 911 if in immediate danger',
        available: '24/7'
      }
    ]
  };

  res.json({
    success: true,
    data: emergencyResources
  });
});

// Get mental health resources based on risk level
router.get('/resources/:riskLevel', (req, res) => {
  const { riskLevel } = req.params;

  const resources = {
    CRITICAL: {
      priority: 'EMERGENCY',
      resources: [
        { type: 'hotline', name: 'National Suicide Prevention Lifeline', number: '988' },
        { type: 'inPerson', name: 'Emergency Room', description: 'Seek immediate care' },
        { type: 'online', name: 'Crisis Text Line', number: '741741' }
      ]
    },
    SEVERE: {
      priority: 'URGENT',
      resources: [
        { type: 'provider', name: 'Psychiatrist', description: 'Urgent psychiatric evaluation' },
        { type: 'provider', name: 'Psychologist', description: 'Crisis counseling' },
        { type: 'facility', name: 'Psychiatric Hospital', description: 'Inpatient evaluation' },
        { type: 'hotline', name: 'Crisis Hotline', number: '988' }
      ]
    },
    MODERATE: {
      priority: 'HIGH',
      resources: [
        { type: 'provider', name: 'Therapist', description: 'Regular therapy sessions' },
        { type: 'provider', name: 'Psychiatrist', description: 'Medication evaluation' },
        { type: 'group', name: 'Support Groups', description: 'Peer support' },
        { type: 'selfCare', name: 'Counseling', description: 'Online counseling services' }
      ]
    },
    MILD: {
      priority: 'STANDARD',
      resources: [
        { type: 'provider', name: 'Counselor', description: 'General counseling' },
        { type: 'selfCare', name: 'Apps', description: 'Mental health apps (Headspace, Calm, etc.)' },
        { type: 'group', name: 'Support Groups', description: 'Online or in-person groups' },
        { type: 'selfCare', name: 'Wellness Programs', description: 'Workplace EAP programs' }
      ]
    },
    LOW: {
      priority: 'PREVENTIVE',
      resources: [
        { type: 'selfCare', name: 'Wellness', description: 'Regular exercise and nutrition' },
        { type: 'selfCare', name: 'Meditation', description: 'Mindfulness practices' },
        { type: 'community', name: 'Social Activities', description: 'Community engagement' },
        { type: 'checkup', name: 'Regular Checkups', description: 'Annual mental health screening' }
      ]
    }
  };

  const result = resources[riskLevel] || resources.LOW;

  res.json({
    success: true,
    data: result
  });
});

export default router;
