@echo off
echo 🚀 Setting up CampusSpace...
python -m venv .venv
call .venv\Scripts\activate
echo 📦 Installing dependencies...
pip install -r requirements.txt
echo 🗄️ Initializing Database...
python scripts\init_db.py --reset
echo ✅ Setup complete! Run run.bat to start the app.
pause
