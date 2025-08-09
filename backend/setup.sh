#!/bin/bash

# Backend setup script
echo "Setting up AI Code Review Bot Backend..."

# Create virtual environment
python -m venv .venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

echo "Backend setup complete!"
echo "Please edit .env file with your actual values:"
echo "- OPENAI_API_KEY: Your OpenAI API key"
echo "- GITHUB_APP_ID: Your GitHub App ID"
echo "- GITHUB_WEBHOOK_SECRET: Your webhook secret"
echo "- GITHUB_PRIVATE_KEY_BASE64: Base64 encoded private key"

echo ""
echo "To run the backend:"
echo "uvicorn main:app --reload"
