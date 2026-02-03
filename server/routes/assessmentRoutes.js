import express from 'express';
import { AssessmentService } from '../services/assessmentService.js';

const router = express.Router();

// Get all assessment questions
router.get('/questions', (req, res) => {
  const questions = AssessmentService.getQuestions();
  res.json({
    success: true,
    data: questions
  });
});

// Get questions by category
router.get('/questions/category/:category', (req, res) => {
  const { category } = req.params;
  const questions = AssessmentService.getQuestionsByCategory(category);
  res.json({
    success: true,
    data: questions
  });
});

// Get all categories
router.get('/categories', (req, res) => {
  const categories = AssessmentService.getCategories();
  res.json({
    success: true,
    data: categories
  });
});

// Get specific question
router.get('/question/:id', (req, res) => {
  const { id } = req.params;
  const question = AssessmentService.getQuestionById(parseInt(id));
  
  if (!question) {
    return res.status(404).json({
      success: false,
      error: 'Question not found'
    });
  }

  res.json({
    success: true,
    data: question
  });
});

export default router;
