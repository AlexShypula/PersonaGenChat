#!/bin/bash

echo "🎭 Starting Persona System..."
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3 from https://python.org"
    read -p "Press Enter to exit..."
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo "You need to create a .env file with your OpenAI API key"
    echo
    read -p "Enter your OpenAI API key: " api_key
    echo "OPENAI_API_KEY=$api_key" > .env
    echo "✅ .env file created!"
    echo
fi

# Change to frontend directory
cd frontend

# Install requirements
echo "📦 Installing/checking requirements..."
pip3 install -r requirements.txt > /dev/null 2>&1

# Start the application
echo "🚀 Starting web interface..."
echo "📱 Your browser should open automatically"
echo "🌐 If not, go to: http://localhost:8501"
echo
echo "💡 To stop the server, press Ctrl+C"
echo "================================"
echo

# Open browser after a delay (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    (sleep 2 && open "http://localhost:8501") &
# Open browser after a delay (Linux)
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    (sleep 2 && xdg-open "http://localhost:8501") &
fi

# Start streamlit
python3 -m streamlit run app.py --server.port 8501
