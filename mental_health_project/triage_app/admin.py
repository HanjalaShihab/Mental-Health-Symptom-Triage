from django.contrib import admin
from .models import Assessment, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'last_assessment', 'total_assessments')
    list_filter = ('created_at', 'last_assessment')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'user')

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'severity', 'created_at', 'get_symptom_count')
    list_filter = ('severity', 'created_at', 'user', 'prediction_method')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'user')
    
    fieldsets = (
        ('User & Assessment Info', {
            'fields': ('user', 'created_at', 'updated_at', 'severity', 'prediction_method', 'ml_confidence')
        }),
        ('Mood & Cognition', {
            'fields': ('sadness', 'loss_interest', 'worthlessness', 'hopelessness', 'concentration')
        }),
        ('Sleep & Energy', {
            'fields': ('sleep_issues', 'appetite_changes', 'fatigue')
        }),
        ('Anxiety', {
            'fields': ('anxiety', 'panic_attacks', 'physical_symptoms', 'avoidance')
        }),
        ('Behavioral', {
            'fields': ('irritability', 'restlessness', 'social_withdrawal', 'substance_use')
        }),
        ('Psychotic & Risk', {
            'fields': ('paranoia', 'hallucinations', 'self_harm', 'self_harm_plan', 'mood_swings')
        }),
    )

