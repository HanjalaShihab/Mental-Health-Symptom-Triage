from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Main application
    path('', views.index, name='index'),
    path('assessment/', views.assessment, name='assessment'),
    path('self-harm-followup/', views.self_harm_followup, name='self_harm_followup'),
    path('results/<int:assessment_id>/', views.results, name='results'),
    path('history/', views.history, name='history'),
    path('about/', views.about, name='about'),
]
