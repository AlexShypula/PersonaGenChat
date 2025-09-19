#!/usr/bin/env python3
"""
Simple script to run the Streamlit app
"""
import subprocess
import sys
import os

def main():
    # Change to the frontend directory
    frontend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(frontend_dir)
    
    # Run streamlit
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
