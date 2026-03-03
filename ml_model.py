import joblib
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
import warnings
warnings.filterwarnings('ignore')

class MentalHealthMLPredictor:
    def __init__(self, model_path='mental_health_model.pkl', encoder_path='mental_health_encoder.pkl'):
        self.model_path = model_path
        self.encoder_path = encoder_path
        self.model_version = '1.0'
        self.model = None
        self.label_encoder = None
        
        # Mental health symptom features (from messages.py SYMPTOM_ORDER)
        self.feature_names = [
            'sadness', 'loss_interest', 'sleep_issues', 'appetite_changes',
            'fatigue', 'worthlessness', 'concentration', 'anxiety',
            'panic_attacks', 'physical_symptoms', 'avoidance', 'hopelessness',
            'self_harm', 'substance_use', 'social_withdrawal', 'irritability',
            'restlessness', 'paranoia', 'hallucinations', 'mood_swings'
        ]
        
        self.symptom_map = {
            "Sadness": "sadness",
            "LossInterest": "loss_interest",
            "SleepIssues": "sleep_issues",
            "AppetiteChanges": "appetite_changes",
            "Fatigue": "fatigue",
            "Worthlessness": "worthlessness",
            "Concentration": "concentration",
            "Anxiety": "anxiety",
            "PanicAttacks": "panic_attacks",
            "PhysicalSymptoms": "physical_symptoms",
            "Avoidance": "avoidance",
            "Hopelessness": "hopelessness",
            "SelfHarm": "self_harm",
            "SubstanceUse": "substance_use",
            "SocialWithdrawal": "social_withdrawal",
            "Irritability": "irritability",
            "Restlessness": "restlessness",
            "Paranoia": "paranoia",
            "Hallucinations": "hallucinations",
            "MoodSwings": "mood_swings"
        }
        
    def prepare_training_data(self, dataset_path='mental_health_dataset.csv'):
        """Prepare data for training from the provided MentalHealthSurvey.csv"""
        df = pd.read_csv(dataset_path)
        
        # Map your CSV columns to symptom features
        # This mapping adapts your CSV to the ML model format
        feature_mapping = {
            'depression': ['sadness', 'loss_interest', 'fatigue', 'worthlessness', 'concentration'],
            'anxiety': ['anxiety', 'panic_attacks', 'physical_symptoms', 'restlessness'],
            'isolation': ['social_withdrawal'],
            'future_insecurity': ['hopelessness']
        }
        
        # Create feature dataframe
        X = pd.DataFrame(0, index=df.index, columns=self.feature_names)
        
        # Map CSV columns to features
        for i, row in df.iterrows():
            # Depression symptoms
            if row['depression'] >= 4:  # High depression
                for feat in feature_mapping['depression']:
                    X.loc[i, feat] = 1
            elif row['depression'] >= 2:  # Moderate depression
                X.loc[i, 'sadness'] = 1
                X.loc[i, 'fatigue'] = 1
            
            # Anxiety symptoms
            if row['anxiety'] >= 4:
                for feat in feature_mapping['anxiety']:
                    X.loc[i, feat] = 1
            elif row['anxiety'] >= 2:
                X.loc[i, 'anxiety'] = 1
            
            # Isolation
            if row['isolation'] >= 4:
                X.loc[i, 'social_withdrawal'] = 1
            
            # Hopelessness
            if row['future_insecurity'] >= 4:
                X.loc[i, 'hopelessness'] = 1
            
            # Sleep issues from average_sleep
            if row['average_sleep'] in ['2-4 hrs', '4-6 hrs']:
                X.loc[i, 'sleep_issues'] = 1
            
            # Substance use
            if 'Substance Use' in str(row['stress_relief_activities']):
                X.loc[i, 'substance_use'] = 1
            
            # Appetite changes correlation with depression
            if row['depression'] >= 3:
                X.loc[i, 'appetite_changes'] = 1
        
        # Create target labels based on multiple factors
        y = []
        for i, row in df.iterrows():
            # Crisis level (based on severe depression + isolation + hopelessness)
            if row['depression'] >= 4 and row['future_insecurity'] >= 4 and row['isolation'] >= 3:
                y.append('Crisis')
            # Severe (high scores in multiple areas)
            elif (row['depression'] >= 4 and row['anxiety'] >= 4) or row['depression'] >= 5:
                y.append('Severe')
            # Moderate
            elif (row['depression'] >= 3 and row['anxiety'] >= 3) or (row['depression'] >= 3 and row['isolation'] >= 3):
                y.append('Moderate')
            # Mild
            elif row['depression'] >= 2 or row['anxiety'] >= 2 or row['isolation'] >= 2:
                y.append('Mild')
            else:
                y.append('NoConcerns')
        
        # Encode severity labels
        self.label_encoder = LabelEncoder()
        severity_order = ['NoConcerns', 'Mild', 'Moderate', 'Severe', 'Crisis']
        self.label_encoder.fit(severity_order)
        y_encoded = self.label_encoder.transform(y)
        
        return X, y_encoded
    
    def train_model(self, dataset_path='MentalHealthSurvey.csv', cv_folds=5):
        """Train Random Forest model with optional cross-validation"""
        print("🔄 Training Mental Health ML model...")
        
        X, y = self.prepare_training_data(dataset_path)
        
        # Optional: Cross-validation
        if cv_folds > 0:
            print(f"📊 Performing {cv_folds}-fold cross-validation...")
            cv_scores = cross_val_score(
                RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'),
                X, y, cv=cv_folds, scoring='accuracy'
            )
            print(f"  CV Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std()*2:.3f})")
        
        # Train final model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X, y)
        
        # Save model and encoder
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.label_encoder, self.encoder_path)
        
        # Calculate accuracy
        train_accuracy = self.model.score(X, y)
        print(f"✅ Model trained with {train_accuracy*100:.1f}% training accuracy")
        print(f"💾 Model saved to: {self.model_path}")
        
        # Print feature importance
        self.print_feature_importance()
        
        return train_accuracy
    
    def load_model(self):
        """Load trained model"""
        try:
            self.model = joblib.load(self.model_path)
            self.label_encoder = joblib.load(self.encoder_path)
            print(f"✅ Mental Health ML model loaded from {self.model_path}")
            print(f"📊 Model info: {self.get_model_info()}")
            return True
        except Exception as e:
            print(f"❌ No trained model found: {e}")
            print("⚠️ Using rule-based system only")
            return False
    
    def predict(self, symptoms_dict):
        """Predict severity from symptoms dictionary"""
        if not self.model or not self.label_encoder:
            return None, 0.0, {}
        
        try:
            # Convert chatbot symptoms to ML features
            features = self._convert_symptoms_to_features(symptoms_dict)
            
            # Make prediction
            prediction_encoded = self.model.predict([features])[0]
            prediction_prob = self.model.predict_proba([features]).max()
            
            # Get all probabilities
            all_probs = self.model.predict_proba([features])[0]
            prob_dict = {
                self.label_encoder.inverse_transform([i])[0]: float(prob) 
                for i, prob in enumerate(all_probs)
            }
            
            # Decode prediction
            prediction = self.label_encoder.inverse_transform([prediction_encoded])[0]
            
            return prediction, prediction_prob, prob_dict
            
        except Exception as e:
            print(f"ML prediction error: {e}")
            return None, 0.0, {}
    
    def _convert_symptoms_to_features(self, symptoms_dict):
        """Convert chatbot symptoms to ML features"""
        features = np.zeros(len(self.feature_names))
        
        for i, feature in enumerate(self.feature_names):
            for chatbot_key, ml_key in self.symptom_map.items():
                if ml_key == feature:
                    if chatbot_key in symptoms_dict:
                        value = symptoms_dict[chatbot_key]
                        features[i] = 1 if value == 1 else 0
                    break
        
        return features
    
    def print_feature_importance(self):
        """Print feature importance scores"""
        if not self.model:
            return
        
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n🔝 Feature Importance:")
        for _, row in importance_df.iterrows():
            feature_name = row['feature'].replace('_', ' ').title()
            print(f"  {feature_name:30s}: {row['importance']:.3f}")
    
    def get_model_info(self):
        """Get information about the trained model"""
        if not self.model:
            return "No model loaded"
        
        info = {
            'model_type': type(self.model).__name__,
            'n_features': len(self.feature_names),
            'n_classes': len(self.label_encoder.classes_) if self.label_encoder else 0,
            'classes': list(self.label_encoder.classes_) if self.label_encoder else [],
            'version': self.model_version
        }
        
        if hasattr(self.model, 'n_estimators'):
            info['n_estimators'] = self.model.n_estimators
        
        return info

# Train model if run directly
if __name__ == "__main__":
    print("=" * 60)
    print("🧠 MENTAL HEALTH ML MODEL TRAINING")
    print("=" * 60)
    
    # Check if CSV exists
    if not os.path.exists('MentalHealthSurvey.csv'):
        print("❌ Error: MentalHealthSurvey.csv not found in current directory!")
        print("Please make sure the file exists before training.")
        exit(1)
    
    predictor = MentalHealthMLPredictor()
    
    # Train with 5-fold cross-validation
    accuracy = predictor.train_model(dataset_path='MentalHealthSurvey.csv', cv_folds=5)
    
    print("\n" + "=" * 60)
    print(f"🎯 Model training complete!")
    print(f"📊 Training Accuracy: {accuracy*100:.1f}%")
    print(f"💾 Model saved: mental_health_model.pkl")
    print("=" * 60)