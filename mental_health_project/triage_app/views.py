from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Assessment, UserProfile
from .forms import AssessmentForm, SelfHarmFollowupForm, RegistrationForm, LoginForm
from .rules import determine_severity

# ML model is optional in cloud deployments where the file may be unavailable.
try:
    from ml_model import MentalHealthMLPredictor
except Exception:
    MentalHealthMLPredictor = None

# Initialize ML predictor
ml_predictor = None
ml_enabled = False
if MentalHealthMLPredictor:
    try:
        ml_predictor = MentalHealthMLPredictor()
        ml_enabled = ml_predictor.load_model()
    except Exception:
        ml_enabled = False


# ============ Authentication Views ============

@require_http_methods(["GET", "POST"])
def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully! Welcome {user.username}!')
            # Specify the backend to use for authentication
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegistrationForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Specify the backend to use for authentication
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, 'login.html', context)


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('index')


@login_required(login_url='login')
def profile(request):
    """User profile with assessment history"""
    user = request.user
    profile = user.profile
    assessments = user.assessments.all()
    
    context = {
        'user': user,
        'profile': profile,
        'assessments': assessments,
        'severity_choices': Assessment.SEVERITY_CHOICES,
    }
    return render(request, 'profile.html', context)


# ============ Main Application Views ============

def index(request):
    """Home page"""
    if request.user.is_authenticated:
        # Show user's recent assessments
        recent_assessments = request.user.assessments.all()[:5]
        last_assessment = request.user.profile.last_assessment
    else:
        recent_assessments = []
        last_assessment = None
    
    context = {
        'recent_assessments': recent_assessments,
        'last_assessment': last_assessment,
    }
    return render(request, 'index.html', context)


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def assessment(request):
    """Mental health assessment form"""
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment_obj = form.save(commit=False)
            assessment_obj.user = request.user  # Assign user
            
            # Check if self-harm was reported
            if assessment_obj.self_harm:
                assessment_obj.save()  # Save first to get ID
                request.session['assessment_id'] = assessment_obj.id
                return redirect('self_harm_followup')
            else:
                # Calculate severity
                severity = calculate_severity(assessment_obj)
                assessment_obj.severity = severity
                assessment_obj.save()
                
                # Update user profile
                request.user.profile.last_assessment = assessment_obj.created_at
                request.user.profile.total_assessments = request.user.assessments.count()
                request.user.profile.save()
                
                return redirect('results', assessment_id=assessment_obj.id)
    else:
        form = AssessmentForm()
    
    context = {
        'form': form,
    }
    return render(request, 'assessment.html', context)


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def self_harm_followup(request):
    """Follow-up for self-harm risk assessment"""
    assessment_id = request.session.get('assessment_id')
    
    if not assessment_id:
        return redirect('assessment')
    
    try:
        assessment_obj = Assessment.objects.get(id=assessment_id, user=request.user)
    except Assessment.DoesNotExist:
        messages.error(request, 'Assessment not found.')
        return redirect('assessment')
    
    if request.method == 'POST':
        form = SelfHarmFollowupForm(request.POST)
        if form.is_valid():
            assessment_obj.self_harm_plan = form.cleaned_data['self_harm_plan']
            severity = calculate_severity(assessment_obj)
            assessment_obj.severity = severity
            assessment_obj.save()
            
            # Update user profile
            request.user.profile.last_assessment = assessment_obj.created_at
            request.user.profile.total_assessments = request.user.assessments.count()
            request.user.profile.save()
            
            del request.session['assessment_id']
            return redirect('results', assessment_id=assessment_obj.id)
    else:
        form = SelfHarmFollowupForm()
    
    context = {
        'form': form,
        'assessment': assessment_obj,
    }
    return render(request, 'self_harm_followup.html', context)


@login_required(login_url='login')
def results(request, assessment_id):
    """Display assessment results"""
    try:
        assessment_obj = Assessment.objects.get(id=assessment_id, user=request.user)
    except Assessment.DoesNotExist:
        messages.error(request, 'Assessment not found.')
        return redirect('assessment')
    
    context = {
        'assessment': assessment_obj,
        'severity_details': get_severity_details(assessment_obj.severity),
        'symptom_count': assessment_obj.get_symptom_count(),
    }
    return render(request, 'results.html', context)


@login_required(login_url='login')
def history(request):
    """View assessment history"""
    assessments = request.user.assessments.all()
    
    # Simple filtering
    severity_filter = request.GET.get('severity')
    if severity_filter:
        assessments = assessments.filter(severity=severity_filter)
    
    context = {
        'assessments': assessments,
        'severity_choices': Assessment.SEVERITY_CHOICES,
    }
    return render(request, 'history.html', context)


def about(request):
    """About page"""
    return render(request, 'about.html')


def calculate_severity(assessment_obj):
    """Calculate severity based on symptoms"""
    # Build symptom dictionary for rules engine
    symptoms_dict = {
        "Sadness": int(assessment_obj.sadness),
        "LossInterest": int(assessment_obj.loss_interest),
        "SleepIssues": int(assessment_obj.sleep_issues),
        "AppetiteChanges": int(assessment_obj.appetite_changes),
        "Fatigue": int(assessment_obj.fatigue),
        "Worthlessness": int(assessment_obj.worthlessness),
        "Concentration": int(assessment_obj.concentration),
        "Anxiety": int(assessment_obj.anxiety),
        "PanicAttacks": int(assessment_obj.panic_attacks),
        "PhysicalSymptoms": int(assessment_obj.physical_symptoms),
        "Avoidance": int(assessment_obj.avoidance),
        "Hopelessness": int(assessment_obj.hopelessness),
        "SelfHarm": int(assessment_obj.self_harm),
        "SelfHarmPlan": int(assessment_obj.self_harm_plan) if assessment_obj.self_harm_plan else 0,
        "SubstanceUse": int(assessment_obj.substance_use),
        "SocialWithdrawal": int(assessment_obj.social_withdrawal),
        "Irritability": int(assessment_obj.irritability),
        "Restlessness": int(assessment_obj.restlessness),
        "Paranoia": int(assessment_obj.paranoia),
        "Hallucinations": int(assessment_obj.hallucinations),
        "MoodSwings": int(assessment_obj.mood_swings),
    }
    
    # Use rules engine to determine severity
    severity = determine_severity(symptoms_dict)
    
    # Try ML model if enabled
    ml_confidence = None
    if ml_enabled:
        try:
            ml_severity, confidence = ml_predictor.predict_severity(symptoms_dict)
            assessment_obj.ml_confidence = confidence
            assessment_obj.prediction_method = 'ml'
            # Optionally use ML result instead of rules
            # severity = ml_severity
        except:
            pass
    
    return severity


def get_severity_details(severity):
    """Get detailed information about severity level"""
    details = {
        'NoConcerns': {
            'name': 'No Significant Concerns',
            'icon': '✅',
            'color': 'success',
            'advice': [
                'Maintain healthy routines and habits',
                'Stay connected with loved ones',
                'Practice self-care and stress management',
                'Reach out if symptoms change',
                'Continue regular physical activity and healthy diet',
            ],
            'resources': []
        },
        'Mild': {
            'name': 'Mild Concerns',
            'icon': '🟢',
            'color': 'info',
            'advice': [
                'Practice self-care and stress management',
                'Maintain regular sleep and exercise',
                'Talk to someone you trust',
                'Consider counseling if symptoms persist',
                'Monitor your symptoms for any changes',
            ],
            'resources': [
                'Mental health self-help resources',
                'Meditation and mindfulness apps',
                'Community support groups',
            ]
        },
        'Moderate': {
            'name': 'Moderate Concerns',
            'icon': '🟡',
            'color': 'warning',
            'advice': [
                'Consider speaking with a mental health professional',
                'Contact a counselor or psychologist',
                'Join support groups for similar concerns',
                'Practice coping strategies and self-care',
                'Do not isolate yourself',
            ],
            'resources': [
                'Professional mental health services',
                'Therapy and counseling providers',
                'Support hotlines',
                'Group therapy sessions',
            ]
        },
        'Severe': {
            'name': 'Severe Concerns',
            'icon': '🔴',
            'color': 'danger',
            'advice': [
                'Seek professional help immediately',
                'Contact a mental health crisis line',
                'Reach out to a trusted person',
                'Do not wait - help is available',
                'Consider hospitalization if needed',
            ],
            'resources': [
                'Mental Health Crisis Hotline',
                'Local emergency mental health services',
                'Hospital psychiatric departments',
                '24/7 counselor support',
            ]
        },
        'Crisis': {
            'name': 'Immediate Crisis - Urgent Help Needed',
            'icon': '🚨',
            'color': 'danger',
            'advice': [
                'Call emergency services immediately (999/112)',
                'Go to the nearest hospital emergency room',
                'Do NOT stay alone',
                'Tell someone you trust immediately',
                'Help is available - you are not alone',
            ],
            'resources': [
                'Emergency Services (999/112)',
                'National Suicide Prevention Lifeline',
                'Crisis Text Line',
                'Nearest Hospital Emergency Room',
            ]
        }
    }
    return details.get(severity, {})
