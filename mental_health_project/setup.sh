#!/bin/bash

# Mental Health Triage - Setup Script

echo "🏥 Mental Health Symptom Triage - Setup Script"
echo "==============================================="
echo ""

# Check Python version
echo "Checking Python installation..."
python3 --version

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py migrate
echo "✓ Database migrations completed"

# Create superuser
echo ""
echo "Creating superuser account..."
python manage.py createsuperuser

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected"

echo ""
echo "✓ Setup complete!"
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then visit: http://localhost:8000"
