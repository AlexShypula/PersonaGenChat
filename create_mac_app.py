#!/usr/bin/env python3
"""
Creates a proper Mac .app bundle for double-clicking
"""
import os
import shutil
from pathlib import Path

def create_mac_app():
    """Create a Mac .app bundle"""
    project_root = Path(__file__).parent
    app_name = "Persona System.app"
    app_path = project_root / app_name
    
    # Remove existing app if it exists
    if app_path.exists():
        shutil.rmtree(app_path)
    
    # Create app bundle structure
    contents_dir = app_path / "Contents"
    macos_dir = contents_dir / "MacOS"
    resources_dir = contents_dir / "Resources"
    
    os.makedirs(macos_dir, exist_ok=True)
    os.makedirs(resources_dir, exist_ok=True)
    
    # Create Info.plist
    info_plist = contents_dir / "Info.plist"
    with open(info_plist, 'w') as f:
        f.write('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>PersonaSystem</string>
    <key>CFBundleIdentifier</key>
    <string>com.local.persona-system</string>
    <key>CFBundleName</key>
    <string>Persona System</string>
    <key>CFBundleDisplayName</key>
    <string>Persona System</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.9</string>
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>''')
    
    # Create the main executable script
    executable = macos_dir / "PersonaSystem"
    with open(executable, 'w') as f:
        f.write(f'''#!/bin/bash

# Get the directory where this app bundle is located
APP_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")/../../../" && pwd)"
cd "$APP_DIR"

echo "🎭 Starting Persona System..."
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    osascript -e 'display dialog "Python 3 is not installed. Please install Python 3 from https://python.org" buttons {{"OK"}} default button "OK"'
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    osascript -e 'display dialog "You need API keys from OpenAI and Hugging Face. Set them up now?" buttons {{"Cancel", "Setup"}} default button "Setup"' > /dev/null
    if [ $? -eq 0 ]; then
        OPENAI_KEY=$(osascript -e 'display dialog "Enter your OpenAI API key (from https://platform.openai.com/api-keys):" default answer "" with hidden answer' -e 'text returned of result' 2>/dev/null)
        HF_TOKEN=$(osascript -e 'display dialog "Enter your Hugging Face token (from https://huggingface.co/settings/tokens):" default answer "" with hidden answer' -e 'text returned of result' 2>/dev/null)
        
        {
            if [ ! -z "$OPENAI_KEY" ]; then
                echo "OPENAI_API_KEY=$OPENAI_KEY"
            else
                echo "# OPENAI_API_KEY=your_openai_key_here"
            fi
            
            if [ ! -z "$HF_TOKEN" ]; then
                echo "HUGGINGFACE_HUB_TOKEN=$HF_TOKEN"
            else
                echo "# HUGGINGFACE_HUB_TOKEN=your_hf_token_here"
            fi
        } > .env
        
        osascript -e 'display notification "API keys saved!" with title "Persona System"'
    else
        osascript -e 'display dialog "API keys are required. Please create a .env file manually with OPENAI_API_KEY and HUGGINGFACE_HUB_TOKEN." buttons {{"OK"}} default button "OK"'
        exit 1
    fi
fi

# Change to frontend directory
cd frontend

# Install requirements
echo "📦 Installing/checking requirements..."
python3 -m pip install -r requirements.txt > /dev/null 2>&1

# Show notification
osascript -e 'display notification "Opening in your web browser..." with title "Persona System"'

# Open browser after a delay
(sleep 3 && open "http://localhost:8501") &

# Start streamlit
python3 -m streamlit run app.py --server.port 8501 --server.headless true

''')
    
    # Make executable
    os.chmod(executable, 0o755)
    
    print(f"✅ Created {app_name}")
    print("🖱️  You can now double-click the app to start!")
    print(f"📁 Location: {app_path}")
    
    return app_path

if __name__ == "__main__":
    create_mac_app()
