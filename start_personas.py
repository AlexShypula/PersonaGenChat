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
        print("You need to create a .env file with your API keys:")
        print("OPENAI_API_KEY=your_openai_key_here")
        print("HUGGINGFACE_HUB_TOKEN=your_hf_token_here")
        print()
        print("🔑 You'll need tokens from:")
        print("   • OpenAI: https://platform.openai.com/api-keys")
        print("   • Hugging Face: https://huggingface.co/settings/tokens")
        print()
        
        create_env = input("Would you like me to help you create the .env file? (y/n): ").lower().strip()
        if create_env == 'y':
            print("\n🔑 Let's set up your API keys...")
            print("(You can press Enter to skip any key and add it manually later)")
            print()
            
            # Get OpenAI API key
            openai_key = input("📝 Enter your OpenAI API key (starts with sk-): ").strip()
            
            # Get Hugging Face token
            print("\n💡 For Hugging Face token:")
            print("   1. Go to https://huggingface.co/settings/tokens")
            print("   2. Click 'New token'")
            print("   3. Choose 'Read' permission")
            print("   4. Copy the token (starts with hf_)")
            hf_token = input("📝 Enter your Hugging Face token (starts with hf_): ").strip()
            
            # Create .env file
            with open(env_file, 'w') as f:
                if openai_key:
                    f.write(f"OPENAI_API_KEY={openai_key}\n")
                else:
                    f.write("# OPENAI_API_KEY=your_openai_key_here\n")
                
                if hf_token:
                    f.write(f"HUGGINGFACE_HUB_TOKEN={hf_token}\n")
                else:
                    f.write("# HUGGINGFACE_HUB_TOKEN=your_hf_token_here\n")
            
            if openai_key and hf_token:
                print("✅ .env file created with both tokens!")
            elif openai_key or hf_token:
                print("✅ .env file created! Please add the missing tokens manually.")
            else:
                print("✅ .env template created! Please add your tokens manually.")
        else:
            print("Please create a .env file manually with your API keys.")
            input("Press Enter to exit...")
            return
    
    # Check if we have the required tokens
    import os
    from dotenv import load_dotenv
    load_dotenv(env_file)
    
    openai_key = os.getenv("OPENAI_API_KEY")
    hf_token = os.getenv("HF_TOKEN")
    
    if not openai_key:
        print("⚠️  Missing OPENAI_API_KEY in .env file")
        print("   Get one from: https://platform.openai.com/api-keys")
        
    if not hf_token:
        print("⚠️  Missing HF_TOKEN in .env file")
        print("   Get one from: https://huggingface.co/settings/tokens")
    
    if not openai_key or not hf_token:
        print("\n❌ Missing required API keys. Please update your .env file.")
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
