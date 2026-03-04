from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Assessment

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name (optional)'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name (optional)'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = [
            'sadness', 'loss_interest', 'sleep_issues', 'appetite_changes',
            'fatigue', 'worthlessness', 'concentration', 'anxiety',
            'panic_attacks', 'physical_symptoms', 'avoidance', 'hopelessness',
            'self_harm', 'substance_use', 'social_withdrawal', 'irritability',
            'restlessness', 'paranoia', 'hallucinations', 'mood_swings'
        ]
        widgets = {
            'sadness': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'loss_interest': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'sleep_issues': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'appetite_changes': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'fatigue': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'worthlessness': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'concentration': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'anxiety': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'panic_attacks': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'physical_symptoms': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'avoidance': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'hopelessness': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'self_harm': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox', 'id': 'self_harm'}),
            'substance_use': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'social_withdrawal': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'irritability': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'restlessness': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'paranoia': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'hallucinations': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
            'mood_swings': forms.CheckboxInput(attrs={'class': 'form-check-input symptom-checkbox'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Define symptom labels and descriptions
        self.fields['sadness'].label = 'Sadness'
        self.fields['sadness'].help_text = 'Have you been feeling sad, empty, or depressed most of the day?'
        
        self.fields['loss_interest'].label = 'Loss of Interest'
        self.fields['loss_interest'].help_text = 'Have you lost interest in activities you used to enjoy?'
        
        self.fields['sleep_issues'].label = 'Sleep Issues'
        self.fields['sleep_issues'].help_text = 'Do you have trouble sleeping or sleeping too much?'
        
        self.fields['appetite_changes'].label = 'Appetite Changes'
        self.fields['appetite_changes'].help_text = 'Have you noticed significant changes in appetite or weight?'
        
        self.fields['fatigue'].label = 'Fatigue'
        self.fields['fatigue'].help_text = 'Do you feel tired or have low energy most days?'
        
        self.fields['worthlessness'].label = 'Worthlessness'
        self.fields['worthlessness'].help_text = 'Do you feel worthless or guilty about things?'
        
        self.fields['concentration'].label = 'Concentration Issues'
        self.fields['concentration'].help_text = 'Do you have trouble concentrating or making decisions?'
        
        self.fields['anxiety'].label = 'Anxiety'
        self.fields['anxiety'].help_text = 'Do you feel anxious, worried, or on edge frequently?'
        
        self.fields['panic_attacks'].label = 'Panic Attacks'
        self.fields['panic_attacks'].help_text = 'Have you experienced sudden episodes of intense fear or panic?'
        
        self.fields['physical_symptoms'].label = 'Physical Symptoms'
        self.fields['physical_symptoms'].help_text = 'Racing heart, sweating, or trembling when anxious?'
        
        self.fields['avoidance'].label = 'Avoidance'
        self.fields['avoidance'].help_text = 'Do you avoid situations because of fear or anxiety?'
        
        self.fields['hopelessness'].label = 'Hopelessness'
        self.fields['hopelessness'].help_text = 'Do you feel hopeless about the future?'
        
        self.fields['self_harm'].label = 'Self-Harm Thoughts'
        self.fields['self_harm'].help_text = 'Have you had thoughts of harming yourself or ending your life?'
        
        self.fields['substance_use'].label = 'Substance Use'
        self.fields['substance_use'].help_text = 'Have you been using alcohol or drugs to cope?'
        
        self.fields['social_withdrawal'].label = 'Social Withdrawal'
        self.fields['social_withdrawal'].help_text = 'Have you been withdrawing from friends or family?'
        
        self.fields['irritability'].label = 'Irritability'
        self.fields['irritability'].help_text = 'Have you felt unusually irritable or angry?'
        
        self.fields['restlessness'].label = 'Restlessness'
        self.fields['restlessness'].help_text = 'Do you feel restless or unable to sit still?'
        
        self.fields['paranoia'].label = 'Paranoia'
        self.fields['paranoia'].help_text = 'Feel that others are out to harm you or mistrust others?'
        
        self.fields['hallucinations'].label = 'Hallucinations'
        self.fields['hallucinations'].help_text = 'Do you hear voices or see things others don\'t?'
        
        self.fields['mood_swings'].label = 'Mood Swings'
        self.fields['mood_swings'].help_text = 'Experience extreme mood swings from very high to very low?'


class SelfHarmFollowupForm(forms.Form):
    self_harm_plan = forms.BooleanField(
        label='Self-Harm Plan',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    self_harm_plan.help_text = 'Do you have a specific plan or intent to harm yourself?'
