// Triage scoring and recommendation logic
export class TriageService {
  static scoreAssessment(answers) {
    let totalScore = 0;
    let categoryScores = {};

    // Calculate total and category scores
    answers.forEach(answer => {
      totalScore += answer.value;
      if (!categoryScores[answer.category]) {
        categoryScores[answer.category] = 0;
      }
      categoryScores[answer.category] += answer.value;
    });

    return {
      totalScore,
      categoryScores,
      maxScore: answers.length * 3
    };
  }

  static calculateRiskLevel(scores) {
    const { totalScore, categoryScores, maxScore } = scores;
    const percentage = (totalScore / maxScore) * 100;

    let riskLevel = 'LOW';
    let severity = 0;

    // Critical risk indicators
    if (categoryScores.risk >= 2) {
      return {
        level: 'CRITICAL',
        severity: 4,
        description: 'Immediate risk of self-harm or harm to others detected',
        recommendation: 'EMERGENCY: Contact emergency services (911) or go to the nearest emergency room immediately',
        actions: ['Call 911', 'Go to emergency room', 'Contact crisis hotline: 988']
      };
    }

    // Determine risk level based on total score percentage
    if (percentage >= 70) {
      riskLevel = 'SEVERE';
      severity = 3;
    } else if (percentage >= 50) {
      riskLevel = 'MODERATE';
      severity = 2;
    } else if (percentage >= 25) {
      riskLevel = 'MILD';
      severity = 1;
    } else {
      riskLevel = 'LOW';
      severity = 0;
    }

    return {
      level: riskLevel,
      severity,
      score: totalScore,
      maxScore,
      percentage: percentage.toFixed(1),
      categoryBreakdown: categoryScores
    };
  }

  static generateRecommendations(riskAssessment) {
    const recommendations = [];
    const { level, categoryBreakdown } = riskAssessment;

    // General recommendations based on risk level
    const riskRecommendations = {
      CRITICAL: {
        description: 'URGENT CRISIS INTERVENTION NEEDED',
        actions: [
          'Call 911 or emergency services immediately',
          'Go to the nearest emergency room',
          'Call National Suicide Prevention Lifeline: 988',
          'Text "HELLO" to 741741 (Crisis Text Line)',
          'Inform a trusted family member or friend',
          'Remove access to means of self-harm if possible'
        ],
        timeframe: 'Immediate (within minutes)'
      },
      SEVERE: {
        description: 'Professional mental health intervention required',
        actions: [
          'Schedule urgent appointment with psychiatrist or psychologist',
          'Consider inpatient hospitalization evaluation',
          'Call crisis hotline for immediate support',
          'Develop a safety plan with a mental health professional',
          'Regular therapy sessions (multiple times per week)',
          'Medication evaluation may be necessary'
        ],
        timeframe: 'Within 24-48 hours'
      },
      MODERATE: {
        description: 'Professional mental health evaluation recommended',
        actions: [
          'Schedule appointment with mental health professional',
          'Begin weekly therapy sessions',
          'Consider medication evaluation',
          'Practice stress management and coping strategies',
          'Increase social support and connection',
          'Maintain regular sleep and exercise habits'
        ],
        timeframe: 'Within 1-2 weeks'
      },
      MILD: {
        description: 'Self-care and preventive mental health support recommended',
        actions: [
          'Consider speaking with a counselor or therapist',
          'Practice stress management techniques',
          'Maintain healthy lifestyle (sleep, exercise, nutrition)',
          'Build social connections and support network',
          'Use mindfulness or meditation apps',
          'Monitor symptoms for changes'
        ],
        timeframe: 'Within 1 month'
      },
      LOW: {
        description: 'Continue healthy lifestyle habits',
        actions: [
          'Maintain regular exercise and healthy diet',
          'Stay socially connected',
          'Practice stress management',
          'Get adequate sleep',
          'Monitor mental health regularly',
          'Seek help if symptoms worsen'
        ],
        timeframe: 'Ongoing maintenance'
      }
    };

    // Category-specific recommendations
    const categoryRecommendations = {
      mood: (score) => {
        if (score >= 6) return 'Mood symptoms are significant. Antidepressant medication and/or therapy are commonly recommended.';
        if (score >= 3) return 'Monitor mood changes. Consider speaking with a mental health professional.';
        return 'Mood appears stable. Continue healthy practices.';
      },
      anxiety: (score) => {
        if (score >= 6) return 'Anxiety symptoms are elevated. CBT and medication management may be beneficial.';
        if (score >= 3) return 'Some anxiety present. Relaxation techniques and therapy may help.';
        return 'Anxiety levels are manageable.';
      },
      sleep: (score) => {
        if (score >= 6) return 'Sleep disturbances are significant. Sleep hygiene and professional evaluation recommended.';
        if (score >= 3) return 'Sleep quality has declined. Establish consistent sleep schedule and routines.';
        return 'Sleep appears adequate.';
      },
      cognitive: (score) => {
        if (score >= 6) return 'Cognitive difficulties are impacting functioning. Professional assessment needed.';
        if (score >= 3) return 'Mild concentration issues. Break tasks into smaller steps and minimize distractions.';
        return 'Cognitive function appears intact.';
      },
      social: (score) => {
        if (score >= 6) return 'Social withdrawal is significant. Actively increase social engagement and support.';
        if (score >= 3) return 'Some social withdrawal noted. Schedule time with supportive friends and family.';
        return 'Social engagement is healthy.';
      },
      physical: (score) => {
        if (score >= 6) return 'Significant physical symptoms. Medical evaluation recommended to rule out physical causes.';
        if (score >= 3) return 'Some physical symptoms present. Discuss with healthcare provider.';
        return 'Physical health appears good.';
      }
    };

    // Add general recommendation
    const generalRec = riskRecommendations[level];
    recommendations.push({
      type: 'general',
      level: level,
      title: generalRec.description,
      actions: generalRec.actions,
      timeframe: generalRec.timeframe
    });

    // Add category-specific recommendations
    Object.entries(categoryBreakdown).forEach(([category, score]) => {
      const categoryRec = categoryRecommendations[category];
      if (categoryRec) {
        recommendations.push({
          type: 'category',
          category: category,
          description: categoryRec(score)
        });
      }
    });

    return recommendations;
  }

  static generateReport(patientData, answers) {
    const scores = this.scoreAssessment(answers);
    const riskAssessment = this.calculateRiskLevel(scores);
    const recommendations = this.generateRecommendations(riskAssessment);

    return {
      patientId: patientData.id,
      patientName: patientData.name,
      patientAge: patientData.age,
      completedAt: new Date().toISOString(),
      scores,
      riskAssessment,
      recommendations,
      nextSteps: this.getNextSteps(riskAssessment.level)
    };
  }

  static getNextSteps(riskLevel) {
    const steps = {
      CRITICAL: [
        { step: 1, action: 'Seek emergency care immediately' },
        { step: 2, action: 'Contact emergency services or go to ER' },
        { step: 3, action: 'Inform family members' },
        { step: 4, action: 'Follow hospital treatment plan' }
      ],
      SEVERE: [
        { step: 1, action: 'Contact mental health professional' },
        { step: 2, action: 'Schedule urgent appointment' },
        { step: 3, action: 'Begin treatment (therapy/medication)' },
        { step: 4, action: 'Establish support network' },
        { step: 5, action: 'Follow treatment plan consistently' }
      ],
      MODERATE: [
        { step: 1, action: 'Schedule therapy appointment' },
        { step: 2, action: 'Begin regular sessions' },
        { step: 3, action: 'Implement coping strategies' },
        { step: 4, action: 'Monitor progress' }
      ],
      MILD: [
        { step: 1, action: 'Maintain healthy habits' },
        { step: 2, action: 'Consider preventive counseling' },
        { step: 3, action: 'Monitor mental health' },
        { step: 4, action: 'Seek help if symptoms worsen' }
      ],
      LOW: [
        { step: 1, action: 'Continue healthy lifestyle' },
        { step: 2, action: 'Regular self-care' },
        { step: 3, action: 'Periodic check-ins' }
      ]
    };

    return steps[riskLevel] || steps.LOW;
  }
}
