# messages.py - Mental Health Symptom Questions (based on WHO mhGAP)

QUESTIONS = {
    "Sadness": "Have you been feeling sad, empty, or depressed most of the day, nearly every day? (yes/no)",
    "LossInterest": "Have you lost interest or pleasure in activities you used to enjoy? (yes/no)",
    "SleepIssues": "Do you have trouble sleeping (difficulty falling/staying asleep or sleeping too much)? (yes/no)",
    "AppetiteChanges": "Have you noticed significant changes in your appetite or weight? (yes/no)",
    "Fatigue": "Do you feel tired or have low energy most days? (yes/no)",
    "Worthlessness": "Do you feel worthless or guilty about things? (yes/no)",
    "Concentration": "Do you have trouble concentrating or making decisions? (yes/no)",
    "Anxiety": "Do you feel anxious, worried, or on edge frequently? (yes/no)",
    "PanicAttacks": "Have you experienced sudden episodes of intense fear or panic? (yes/no)",
    "PhysicalSymptoms": "Do you have physical symptoms like racing heart, sweating, or trembling when anxious? (yes/no)",
    "Avoidance": "Do you avoid situations because of fear or anxiety? (yes/no)",
    "Hopelessness": "Do you feel hopeless about the future? (yes/no)",
    "SelfHarm": "Have you had thoughts of harming yourself or ending your life? (yes/no)",
    "SubstanceUse": "Have you been using alcohol, drugs, or medications to cope with your feelings? (yes/no)",
    "SocialWithdrawal": "Have you been withdrawing from friends, family, or social activities? (yes/no)",
    "Irritability": "Have you felt unusually irritable or angry? (yes/no)",
    "Restlessness": "Do you feel restless or unable to sit still? (yes/no)",
    "Paranoia": "Do you feel that others are out to harm you or mistrust others excessively? (yes/no)",
    "Hallucinations": "Do you hear voices or see things that others don't? (yes/no)",
    "MoodSwings": "Do you experience extreme mood swings (from very high/energetic to very low)? (yes/no)"
}

# Self-harm assessment follow-up (if SelfHarm = yes)
SELF_HARM_FOLLOWUP = "Do you have a specific plan or intent to harm yourself? (yes/no)"

ADVICE = {
    "NoConcerns": "✅ **No Significant Concerns Detected**\n\n• Maintain healthy routines\n• Stay connected with loved ones\n• Practice self-care\n• Reach out if things change",
    
    "Mild": "🟢 **Mild Concerns Detected**\n\n• Practice self-care and stress management\n• Maintain regular sleep and exercise\n• Talk to someone you trust\n• Consider counseling if symptoms persist\n• Monitor your symptoms",
    
    "Moderate": "🟡 **Moderate Concerns Detected**\n\n• Consider speaking with a mental health professional\n• Contact a counselor or psychologist\n• Join support groups\n• Practice coping strategies\n• Don't isolate yourself",
    
    "Severe": "🔴 **SEVERE CONCERNS DETECTED**\n\n• Seek professional help immediately\n• Contact a mental health crisis line\n• Reach out to a trusted person\n• Do not wait - help is available",
    
    "Crisis": "🚨 **IMMEDIATE CRISIS - URGENT HELP NEEDED** 🚨\n\n• Call emergency services immediately (999/112)\n• Go to nearest hospital emergency room\n• Do NOT stay alone\n• Tell someone you trust immediately\n• Help is available - you are not alone"
}

DISCLAIMER = (
    "⚠️ **Important Disclaimer:**\n"
    "This chatbot provides preliminary mental health screening only "
    "and is NOT a substitute for professional mental health assessment. "
    "It cannot diagnose conditions or replace care from qualified mental health professionals. "
    "If you're in crisis, please contact emergency services immediately."
)

# Symptom order for assessment
SYMPTOM_ORDER = [
    "Sadness",
    "LossInterest",
    "SleepIssues",
    "AppetiteChanges",
    "Fatigue",
    "Worthlessness",
    "Concentration",
    "Anxiety",
    "PanicAttacks",
    "PhysicalSymptoms",
    "Avoidance",
    "Hopelessness",
    "SelfHarm",
    "SubstanceUse",
    "SocialWithdrawal",
    "Irritability",
    "Restlessness",
    "Paranoia",
    "Hallucinations",
    "MoodSwings"
]