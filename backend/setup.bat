@echo off
echo Setting up AI Code Review Bot Backend...

REM Create virtual environment
python -m venv .venv

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Copy environment file
copy .env.example .env

echo Backend setup complete!
echo Please edit .env file with your actual values:
echo - OPENAI_API_KEY: Your OpenAI API key
echo - GITHUB_APP_ID: Your GitHub App ID  
echo - GITHUB_WEBHOOK_SECRET: Your webhook secret
echo - GITHUB_PRIVATE_KEY_BASE64: Base64 encoded private key

echo.
echo To run the backend:
echo uvicorn main:app --reload

pause
