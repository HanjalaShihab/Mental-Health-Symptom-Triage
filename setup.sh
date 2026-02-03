#!/bin/bash

# Mental Health Symptom Triage - Startup Script
# This script automates the installation and startup process

echo "=========================================="
echo "Mental Health Symptom Triage - Setup"
echo "=========================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js found: $(node --version)"
echo ""

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    exit 1
fi

echo "✅ npm found: $(npm --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo "This may take a few minutes..."
echo ""

npm run install-all

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✅ Dependencies installed successfully!"
echo ""
echo "=========================================="
echo "✨ Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application, run:"
echo ""
echo "  Option 1 (Separate terminals):"
echo "    Terminal 1: npm run dev"
echo "    Terminal 2: npm run client"
echo ""
echo "  Option 2 (Combined):"
echo "    npm run dev:full"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo "For more details, see QUICKSTART.md"
echo "=========================================="
