// Mental health symptom assessment questions
export const assessmentQuestions = [
  {
    id: 1,
    category: 'mood',
    question: 'Over the past two weeks, how often have you felt down, depressed, or hopeless?',
    options: [
      { value: 0, label: 'Not at all' },
      { value: 1, label: 'Several days' },
      { value: 2, label: 'More than half the days' },
      { value: 3, label: 'Nearly every day' }
    ]
  },
  {
    id: 2,
    category: 'mood',
    question: 'Over the past two weeks, how often have you felt little interest or pleasure in doing things?',
    options: [
      { value: 0, label: 'Not at all' },
      { value: 1, label: 'Several days' },
      { value: 2, label: 'More than half the days' },
      { value: 3, label: 'Nearly every day' }
    ]
  },
  {
    id: 3,
    category: 'sleep',
    question: 'Have you experienced significant changes in your sleep patterns?',
    options: [
      { value: 0, label: 'No changes' },
      { value: 1, label: 'Mild changes' },
      { value: 2, label: 'Moderate changes' },
      { value: 3, label: 'Severe changes' }
    ]
  },
  {
    id: 4,
    category: 'anxiety',
    question: 'How often do you feel anxious or worried?',
    options: [
      { value: 0, label: 'Rarely' },
      { value: 1, label: 'Sometimes' },
      { value: 2, label: 'Often' },
      { value: 3, label: 'Most of the time' }
    ]
  },
  {
    id: 5,
    category: 'anxiety',
    question: 'Do you experience panic attacks or sudden intense fear?',
    options: [
      { value: 0, label: 'Never' },
      { value: 1, label: 'Rarely' },
      { value: 2, label: 'Sometimes' },
      { value: 3, label: 'Frequently' }
    ]
  },
  {
    id: 6,
    category: 'cognitive',
    question: 'How often do you have difficulty concentrating or making decisions?',
    options: [
      { value: 0, label: 'Never' },
      { value: 1, label: 'Occasionally' },
      { value: 2, label: 'Frequently' },
      { value: 3, label: 'Always' }
    ]
  },
  {
    id: 7,
    category: 'social',
    question: 'Have you withdrawn from social activities or friends?',
    options: [
      { value: 0, label: 'No withdrawal' },
      { value: 1, label: 'Mild withdrawal' },
      { value: 2, label: 'Moderate withdrawal' },
      { value: 3, label: 'Significant withdrawal' }
    ]
  },
  {
    id: 8,
    category: 'physical',
    question: 'Have you experienced unexplained physical symptoms (fatigue, pain, etc.)?',
    options: [
      { value: 0, label: 'No symptoms' },
      { value: 1, label: 'Mild symptoms' },
      { value: 2, label: 'Moderate symptoms' },
      { value: 3, label: 'Severe symptoms' }
    ]
  },
  {
    id: 9,
    category: 'risk',
    question: 'Have you had thoughts of harming yourself or others?',
    options: [
      { value: 0, label: 'Never' },
      { value: 1, label: 'Rarely' },
      { value: 2, label: 'Sometimes' },
      { value: 3, label: 'Frequently' }
    ]
  },
  {
    id: 10,
    category: 'functioning',
    question: 'How much do these symptoms affect your daily functioning?',
    options: [
      { value: 0, label: 'Not at all' },
      { value: 1, label: 'Minimal impact' },
      { value: 2, label: 'Moderate impact' },
      { value: 3, label: 'Severe impact' }
    ]
  }
];

// Assessment service
export class AssessmentService {
  static getQuestions() {
    return assessmentQuestions;
  }

  static getQuestionById(id) {
    return assessmentQuestions.find(q => q.id === id);
  }

  static getQuestionsByCategory(category) {
    return assessmentQuestions.filter(q => q.category === category);
  }

  static getCategories() {
    return [...new Set(assessmentQuestions.map(q => q.category))];
  }
}
