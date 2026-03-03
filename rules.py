# rules.py - WHO mhGAP Mental Health Classification Rules

def determine_severity(symptoms):
    """
    Determine mental health concern severity based on WHO mhGAP guidelines:
    
    Categories:
    - Crisis: Active self-harm with plan/intent, hallucinations/paranoia with risk
    - Severe: Self-harm thoughts, severe depression/anxiety symptoms, psychosis symptoms
    - Moderate: Multiple moderate symptoms affecting daily life
    - Mild: Some symptoms but functioning relatively well
    - NoConcerns: Minimal or no symptoms
    """
    
    # Extract symptoms (dictionary format)
    if isinstance(symptoms, dict):
        sadness = symptoms.get("Sadness") == 1
        loss_interest = symptoms.get("LossInterest") == 1
        sleep_issues = symptoms.get("SleepIssues") == 1
        appetite_changes = symptoms.get("AppetiteChanges") == 1
        fatigue = symptoms.get("Fatigue") == 1
        worthlessness = symptoms.get("Worthlessness") == 1
        concentration = symptoms.get("Concentration") == 1
        anxiety = symptoms.get("Anxiety") == 1
        panic_attacks = symptoms.get("PanicAttacks") == 1
        physical_symptoms = symptoms.get("PhysicalSymptoms") == 1
        avoidance = symptoms.get("Avoidance") == 1
        hopelessness = symptoms.get("Hopelessness") == 1
        self_harm = symptoms.get("SelfHarm") == 1
        substance_use = symptoms.get("SubstanceUse") == 1
        social_withdrawal = symptoms.get("SocialWithdrawal") == 1
        irritability = symptoms.get("Irritability") == 1
        restlessness = symptoms.get("Restlessness") == 1
        paranoia = symptoms.get("Paranoia") == 1
        hallucinations = symptoms.get("Hallucinations") == 1
        mood_swings = symptoms.get("MoodSwings") == 1
        
        # Special: Self-harm plan (if we have it)
        self_harm_plan = symptoms.get("SelfHarmPlan") == 1
    else:
        # Assume tuple/list (simplified)
        return "NoConcerns"
    
    # CRISIS: Immediate danger
    if self_harm_plan or (self_harm and hopelessness) or hallucinations or paranoia:
        return "Crisis"
    
    # SEVERE: Professional help needed urgently
    severe_depression = (sadness or loss_interest) and hopelessness and worthlessness and (sleep_issues or appetite_changes)
    severe_anxiety = anxiety and panic_attacks and physical_symptoms and avoidance
    psychosis = hallucinations or paranoia
    
    if self_harm or severe_depression or severe_anxiety or psychosis or (substance_use and hopelessness):
        return "Severe"
    
    # MODERATE: Should seek help
    depression_count = sum([sadness, loss_interest, sleep_issues, appetite_changes, fatigue, worthlessness, concentration])
    anxiety_count = sum([anxiety, panic_attacks, physical_symptoms, avoidance, restlessness])
    other_count = sum([social_withdrawal, irritability, mood_swings])
    
    if depression_count >= 4 or anxiety_count >= 3 or (depression_count >= 3 and other_count >= 2):
        return "Moderate"
    
    # MILD: Self-care may help
    total_symptoms = (depression_count + anxiety_count + other_count + 
                     sum([hopelessness, substance_use]))
    
    if total_symptoms >= 2:
        return "Mild"
    
    # NO CONCERNS
    if total_symptoms == 0:
        return "NoConcerns"
    else:
        return "Mild"  # 1 symptom = mild


def test_rules():
    """Test mental health classification rules"""
    
    test_cases = [
        {
            "name": "No symptoms",
            "symptoms": {s: 0 for s in ["Sadness", "LossInterest", "SleepIssues", "Anxiety", "SelfHarm"]},
            "expected": "NoConcerns"
        },
        {
            "name": "Mild - single symptom",
            "symptoms": {"Sadness": 1, "LossInterest": 0, "SleepIssues": 0, "Anxiety": 0, "SelfHarm": 0},
            "expected": "Mild"
        },
        {
            "name": "Moderate depression",
            "symptoms": {"Sadness": 1, "LossInterest": 1, "SleepIssues": 1, "Fatigue": 1, "Concentration": 1, 
                        "Anxiety": 0, "SelfHarm": 0},
            "expected": "Moderate"
        },
        {
            "name": "Severe - self-harm",
            "symptoms": {"Sadness": 1, "LossInterest": 1, "Hopelessness": 1, "SelfHarm": 1, 
                        "SleepIssues": 1, "Anxiety": 1},
            "expected": "Severe"
        },
        {
            "name": "Crisis - self-harm plan",
            "symptoms": {"SelfHarm": 1, "SelfHarmPlan": 1, "Hopelessness": 1},
            "expected": "Crisis"
        },
        {
            "name": "Crisis - hallucinations",
            "symptoms": {"Hallucinations": 1, "Paranoia": 0, "SelfHarm": 0},
            "expected": "Crisis"
        },
        {
            "name": "Severe anxiety",
            "symptoms": {"Anxiety": 1, "PanicAttacks": 1, "PhysicalSymptoms": 1, "Avoidance": 1, "Restlessness": 1},
            "expected": "Severe"
        },
        {
            "name": "Moderate mixed",
            "symptoms": {"Sadness": 1, "Anxiety": 1, "SleepIssues": 1, "Irritability": 1, "SocialWithdrawal": 1},
            "expected": "Moderate"
        }
    ]
    
    print("Testing Mental Health Classification Rules (WHO mhGAP based):")
    print("=" * 70)
    
    all_passed = True
    for test in test_cases:
        result = determine_severity(test["symptoms"])
        passed = result == test["expected"]
        all_passed = all_passed and passed
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test['name']}")
        print(f"  Expected: {test['expected']}, Got: {result}")
        print()
    
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed. Please check the logic.")
    
    return all_passed


if __name__ == "__main__":
    test_rules()