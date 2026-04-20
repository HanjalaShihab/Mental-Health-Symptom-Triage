def determine_severity(symptoms):
    """Determine mental health severity from symptom flags."""
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
    self_harm_plan = symptoms.get("SelfHarmPlan") == 1

    if self_harm_plan or (self_harm and hopelessness) or hallucinations or paranoia:
        return "Crisis"

    severe_depression = (
        (sadness or loss_interest)
        and hopelessness
        and worthlessness
        and (sleep_issues or appetite_changes)
    )
    severe_anxiety = anxiety and panic_attacks and physical_symptoms and avoidance
    psychosis = hallucinations or paranoia

    if self_harm or severe_depression or severe_anxiety or psychosis or (substance_use and hopelessness):
        return "Severe"

    depression_count = sum([
        sadness,
        loss_interest,
        sleep_issues,
        appetite_changes,
        fatigue,
        worthlessness,
        concentration,
    ])
    anxiety_count = sum([anxiety, panic_attacks, physical_symptoms, avoidance, restlessness])
    other_count = sum([social_withdrawal, irritability, mood_swings])

    if depression_count >= 4 or anxiety_count >= 3 or (depression_count >= 3 and other_count >= 2):
        return "Moderate"

    total_symptoms = depression_count + anxiety_count + other_count + sum([hopelessness, substance_use])
    if total_symptoms >= 2:
        return "Mild"

    return "NoConcerns" if total_symptoms == 0 else "Mild"
