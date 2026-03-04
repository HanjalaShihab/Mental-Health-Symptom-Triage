"""
URL configuration for mental_health_project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Google OAuth & allauth URLs
    path('', include('triage_app.urls')),
]
