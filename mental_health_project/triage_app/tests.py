from django.test import TestCase
from .models import Assessment


class AssessmentModelTest(TestCase):
    def setUp(self):
        self.assessment = Assessment.objects.create(
            sadness=True,
            anxiety=True,
        )
    
    def test_assessment_creation(self):
        self.assertEqual(self.assessment.severity, None)
        self.assertEqual(self.assessment.get_symptom_count(), 2)
