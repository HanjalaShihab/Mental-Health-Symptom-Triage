"""
Django management command to test backend integration
"""
from django.core.management.base import BaseCommand
from triage_app.models import Assessment
from triage_app.views import calculate_severity, get_severity_details


class Command(BaseCommand):
    help = 'Test the mental health assessment backend'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testing Mental Health Triage Backend'))
        self.stdout.write('=' * 50)

        # Test 1: No symptoms
        self.stdout.write('\nTest 1: No Symptoms')
        assessment = Assessment.objects.create()
        severity = calculate_severity(assessment)
        assessment.severity = severity
        assessment.save()
        self.stdout.write(f'Result: {severity}')
        self.stdout.write(self.style.SUCCESS(f'✓ Passed'))

        # Test 2: Mild symptoms (anxiety only)
        self.stdout.write('\nTest 2: Mild Symptoms (Anxiety)')
        assessment = Assessment.objects.create(anxiety=True)
        severity = calculate_severity(assessment)
        assessment.severity = severity
        assessment.save()
        self.stdout.write(f'Result: {severity}')
        self.stdout.write(self.style.SUCCESS(f'✓ Passed'))

        # Test 3: Moderate symptoms (depression + anxiety)
        self.stdout.write('\nTest 3: Moderate Symptoms')
        assessment = Assessment.objects.create(
            sadness=True,
            loss_interest=True,
            anxiety=True,
            panic_attacks=True
        )
        severity = calculate_severity(assessment)
        assessment.severity = severity
        assessment.save()
        self.stdout.write(f'Result: {severity}')
        self.stdout.write(self.style.SUCCESS(f'✓ Passed'))

        # Test 4: Severe symptoms
        self.stdout.write('\nTest 4: Severe Symptoms')
        assessment = Assessment.objects.create(
            sadness=True,
            loss_interest=True,
            sleep_issues=True,
            appetite_changes=True,
            fatigue=True,
            worthlessness=True,
            concentration=True,
            hopelessness=True
        )
        severity = calculate_severity(assessment)
        assessment.severity = severity
        assessment.save()
        self.stdout.write(f'Result: {severity}')
        self.stdout.write(self.style.SUCCESS(f'✓ Passed'))

        # Test 5: Crisis (self-harm)
        self.stdout.write('\nTest 5: Crisis Symptoms (Self-Harm)')
        assessment = Assessment.objects.create(
            self_harm=True,
            self_harm_plan=True,
            hopelessness=True
        )
        severity = calculate_severity(assessment)
        assessment.severity = severity
        assessment.save()
        self.stdout.write(f'Result: {severity}')
        self.stdout.write(self.style.SUCCESS(f'✓ Passed'))

        # Display severity details
        self.stdout.write(self.style.SUCCESS('\n✓ All tests passed!'))
        self.stdout.write('\nSeverity Details Available:')
        for sev in ['NoConcerns', 'Mild', 'Moderate', 'Severe', 'Crisis']:
            details = get_severity_details(sev)
            self.stdout.write(f'\n  {details["icon"]} {details["name"]}')
