#!/usr/bin/env python3
"""
Simple double-click launcher for the Persona System
"""
import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    print("🎭 Starting Persona System...")
    print("=" * 50)
    
    # Get the script directory
    script_dir = Path(__file__).parent
    frontend_dir = script_dir / "frontend"
    
    # Check if we're in the right directory
    if not frontend_dir.exists():
        print("❌ Error: frontend directory not found!")
        print("Please make sure this script is in the personas project root.")
        input("Press Enter to exit...")
        return
    
    # Check for .env file
    env_file = script_dir / ".env"
    if not env_file.exists():
        print("⚠️  No .env file found!")
        print("You need to create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_key_here")
        print()
        create_env = input("Would you like me to help you create one? (y/n): ").lower().strip()
        if create_env == 'y':
            api_key = input("Enter your OpenAI API key: ").strip()
            if api_key:
                with open(env_file, 'w') as f:
                    f.write(f"OPENAI_API_KEY={api_key}\n")
                print("✅ .env file created!")
            else:
                print("❌ No API key provided. Exiting...")
                input("Press Enter to exit...")
                return
        else:
            print("Please create a .env file manually and try again.")
            input("Press Enter to exit...")
            return
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Install requirements if needed
    try:
        import streamlit
        print("✅ Streamlit found")
    except ImportError:
        print("📦 Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Packages installed")
    
    print("🚀 Starting web interface...")
    print("📱 Your browser should open automatically")
    print("🌐 If not, go to: http://localhost:8501")
    print()
    print("💡 To stop the server, close this window or press Ctrl+C")
    print("=" * 50)
    
    # Start streamlit in a way that opens browser automatically
    try:
        # Wait a moment then open browser
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:8501')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down Persona System...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
