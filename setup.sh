#!/bin/bash
echo "🚀 Setting up CampusSpace..."
python3 -m venv .venv
source .venv/bin/activate
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "🗄️ Initializing Database..."
python scripts/init_db.py --reset
echo "✅ Setup complete! Run ./run.sh to start the app."
