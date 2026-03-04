#!/bin/bash

# Quick start script for development

echo "🏥 Starting Mental Health Triage Server..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run migrations if needed
echo "Checking database..."
python manage.py migrate --noinput

# Start development server
echo "Starting Django development server..."
echo "Visit: http://localhost:8000"
echo "Admin: http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
