from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    last_assessment = models.DateTimeField(null=True, blank=True)
    total_assessments = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Assessment(models.Model):
    SEVERITY_CHOICES = [
        ('NoConcerns', 'No Significant Concerns'),
        ('Mild', 'Mild Concerns'),
        ('Moderate', 'Moderate Concerns'),
        ('Severe', 'Severe Concerns'),
        ('Crisis', 'Immediate Crisis'),
    ]
    
    # User (allow null for existing assessments, will be enforced in forms)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessments', null=True, blank=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Symptoms (Boolean for each)
    sadness = models.BooleanField(default=False)
    loss_interest = models.BooleanField(default=False)
    sleep_issues = models.BooleanField(default=False)
    appetite_changes = models.BooleanField(default=False)
    fatigue = models.BooleanField(default=False)
    worthlessness = models.BooleanField(default=False)
    concentration = models.BooleanField(default=False)
    anxiety = models.BooleanField(default=False)
    panic_attacks = models.BooleanField(default=False)
    physical_symptoms = models.BooleanField(default=False)
    avoidance = models.BooleanField(default=False)
    hopelessness = models.BooleanField(default=False)
    self_harm = models.BooleanField(default=False)
    self_harm_plan = models.BooleanField(default=False, null=True, blank=True)
    substance_use = models.BooleanField(default=False)
    social_withdrawal = models.BooleanField(default=False)
    irritability = models.BooleanField(default=False)
    restlessness = models.BooleanField(default=False)
    paranoia = models.BooleanField(default=False)
    hallucinations = models.BooleanField(default=False)
    mood_swings = models.BooleanField(default=False)
    
    # Results
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True)
    ml_confidence = models.FloatField(null=True, blank=True)
    prediction_method = models.CharField(max_length=20, default='rules')  # 'rules' or 'ml'
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Assessment {self.id} - {self.severity} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
    
    def get_symptom_count(self):
        """Count number of positive symptoms"""
        return sum([
            self.sadness, self.loss_interest, self.sleep_issues, self.appetite_changes,
            self.fatigue, self.worthlessness, self.concentration, self.anxiety,
            self.panic_attacks, self.physical_symptoms, self.avoidance, self.hopelessness,
            self.self_harm, self.substance_use, self.social_withdrawal, self.irritability,
            self.restlessness, self.paranoia, self.hallucinations, self.mood_swings
        ])
