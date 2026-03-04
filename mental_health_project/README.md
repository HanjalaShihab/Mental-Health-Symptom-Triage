# Mental Health Symptom Triage - Django Web Application

A Django-based web application for mental health symptom screening based on WHO mhGAP guidelines.

## Features

- 📋 **Symptom Assessment**: 20 carefully selected questions covering various mental health domains
- 📊 **Intelligent Scoring**: Uses both rules-based and optional ML-based severity classification
- 💾 **Assessment History**: Track your mental health assessments over time
- 🎯 **Personalized Recommendations**: Get tailored advice based on your assessment results
- 🔒 **Privacy-Focused**: All data stored locally, no third-party sharing
- 🎨 **Modern UI**: Responsive Bootstrap-based interface

## Severity Levels

- ✅ **No Significant Concerns**: Minimal symptoms
- 🟢 **Mild Concerns**: Some symptoms present
- 🟡 **Moderate Concerns**: Multiple symptoms affecting daily life
- 🔴 **Severe Concerns**: Significant symptoms requiring professional help
- 🚨 **Immediate Crisis**: Acute risk requiring emergency intervention

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup Instructions

1. **Clone or navigate to the project directory**:
   ```bash
   cd /home/hanjala/Documents/Mental Health Symptom Triage/mental_health_project
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Copy backend files**:
   The application uses `ml_model.py` and `rules.py` from the parent directory.
   Ensure these files are in the parent directory:
   ```
   /home/hanjala/Documents/Mental Health Symptom Triage/
   ├── mental_health_project/
   │   ├── manage.py
   │   ├── requirements.txt
   │   └── ...
   ├── ml_model.py
   ├── rules.py
   ├── messages.py
   ├── MentalHealthSurvey.csv
   └── .env
   ```

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - **Web Application**: http://localhost:8000
   - **Admin Panel**: http://localhost:8000/admin

## Usage

### Taking an Assessment

1. Click "Start Assessment" on the home page
2. Answer 20 questions about your mental health symptoms
3. If self-harm thoughts are reported, answer a follow-up question
4. Receive your assessment results with recommendations

### Viewing History

1. Go to the "History" page
2. Filter assessments by severity level
3. Click "View" to see detailed results for any assessment

### Admin Panel

Access the admin panel at `/admin` to:
- View all assessments
- Filter by severity and date
- View symptom details for any assessment

## Project Structure

```
mental_health_project/
├── manage.py
├── requirements.txt
├── README.md
├── mental_health_project/
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── triage_app/
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base template
│   │   ├── index.html       # Home page
│   │   ├── assessment.html  # Assessment form
│   │   ├── results.html     # Results page
│   │   ├── history.html     # History view
│   │   ├── about.html       # About page
│   │   └── self_harm_followup.html
│   ├── static/css/          # CSS stylesheets
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── forms.py             # Form definitions
│   ├── models.py            # Database models
│   ├── tests.py             # Unit tests
│   ├── urls.py              # App URL routing
│   └── views.py             # View logic
└── db.sqlite3               # SQLite database (created after migration)
```

## Backend Integration

The application integrates with:

### rules.py
- Implements WHO mhGAP-based severity classification
- Function: `determine_severity(symptoms_dict)` → severity level

### ml_model.py
- Optional machine learning model for enhanced predictions
- Uses scikit-learn's RandomForest classifier
- Provides confidence scores for predictions

## Development

### Running Tests

```bash
python manage.py test
```

### Collecting Static Files

```bash
python manage.py collectstatic
```

### Creating New Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Deployment

### Production Settings

1. Update `settings.py`:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com']
   SECRET_KEY = 'your-secure-secret-key'
   ```

2. Use a production database (PostgreSQL recommended)

3. Use a production web server (Gunicorn, uWSGI)

### Example Gunicorn Deployment

```bash
pip install gunicorn
gunicorn mental_health_project.wsgi
```

## Important Disclaimer

⚠️ **This tool provides preliminary mental health screening only and is NOT:**
- A diagnosis
- A substitute for professional mental health assessment
- Capable of replacing care from qualified mental health professionals

**If you are in crisis or experiencing thoughts of self-harm:**
- Call emergency services immediately (999 in UK, 112 in EU)
- Go to your nearest hospital emergency room
- Contact a crisis helpline in your country

## Clinical Framework

This application uses the **WHO mhGAP (Mental Health Gap Action Programme)** framework, which provides evidence-based recommendations for mental health assessment and management.

## Support

For issues or questions, please refer to:
- The "About" page within the application
- Django documentation: https://docs.djangoproject.com/
- WHO mhGAP: https://www.who.int/teams/mental-health-and-substance-use/mental-health-gap-action-programme

## License

Educational use only. Not for clinical deployment without proper validation and regulatory approval.

## Credits

Built with:
- Django
- Bootstrap 5
- scikit-learn
- pandas
- numpy
