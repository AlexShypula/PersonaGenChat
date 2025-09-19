#!/bin/bash

# This .command file can be double-clicked on Mac
# It will open Terminal and run the script

echo "🎭 Starting Persona System..."
echo "================================"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3 from https://python.org"
    echo "Press any key to open the Python download page..."
    read -n 1 -s
    open "https://python.org/downloads/"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo "You need API keys from:"
    echo "   • OpenAI: https://platform.openai.com/api-keys"
    echo "   • Hugging Face: https://huggingface.co/settings/tokens"
    echo
    read -p "Enter your OpenAI API key (starts with sk-): " openai_key
    echo
    echo "💡 For Hugging Face token:"
    echo "   1. Go to https://huggingface.co/settings/tokens"
    echo "   2. Click 'New token'"
    echo "   3. Choose 'Read' permission"
    echo "   4. Copy the token (starts with hf_)"
    read -p "Enter your Hugging Face token (starts with hf_): " hf_token
    
    # Create .env file
    {
        if [ ! -z "$openai_key" ]; then
            echo "OPENAI_API_KEY=$openai_key"
        else
            echo "# OPENAI_API_KEY=your_openai_key_here"
        fi
        
        if [ ! -z "$hf_token" ]; then
            echo "HUGGINGFACE_HUB_TOKEN=$hf_token"
        else
            echo "# HUGGINGFACE_HUB_TOKEN=your_hf_token_here"
        fi
    } > .env
    
    echo "✅ .env file created!"
    if [ -z "$openai_key" ] || [ -z "$hf_token" ]; then
        echo "⚠️  Please edit .env file to add missing tokens"
    fi
    echo
fi

# Change to frontend directory
cd frontend

# Install requirements
echo "📦 Installing/checking requirements..."
python3 -m pip install -r requirements.txt > /dev/null 2>&1

# Start the application
echo "🚀 Starting web interface..."
echo "📱 Your browser should open automatically"
echo "🌐 If not, go to: http://localhost:8501"
echo
echo "💡 To stop the server, press Ctrl+C or close this window"
echo "================================"
echo

# Open browser after a delay
(sleep 3 && open "http://localhost:8501") &

# Start streamlit
python3 -m streamlit run app.py --server.port 8501

echo
echo "👋 Persona System has stopped."
read -p "Press Enter to close this window..."
