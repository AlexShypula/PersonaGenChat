#!/usr/bin/env python3
"""
Creates a desktop shortcut for the Persona System
"""
import os
import sys
from pathlib import Path

def create_windows_shortcut():
    """Create a Windows desktop shortcut"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Persona System.lnk")
        target = str(Path(__file__).parent / "start_personas.bat")
        wDir = str(Path(__file__).parent)
        icon = target
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.save()
        
        print("✅ Desktop shortcut created!")
        return True
    except ImportError:
        print("⚠️  Windows shortcut creation requires: pip install winshell pywin32")
        return False
    except Exception as e:
        print(f"❌ Error creating shortcut: {e}")
        return False

def create_mac_shortcut():
    """Create a macOS desktop shortcut"""
    desktop = Path.home() / "Desktop"
    app_path = desktop / "Persona System.app"
    
    try:
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
    <string>persona_system</string>
    <key>CFBundleIdentifier</key>
    <string>com.local.persona-system</string>
    <key>CFBundleName</key>
    <string>Persona System</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
</dict>
</plist>''')
        
        # Create executable script
        executable = macos_dir / "persona_system"
        script_path = Path(__file__).parent / "start_personas.sh"
        with open(executable, 'w') as f:
            f.write(f'''#!/bin/bash
cd "{Path(__file__).parent}"
bash "{script_path}"
''')
        
        os.chmod(executable, 0o755)
        print("✅ Desktop app created!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating app: {e}")
        return False

def create_linux_shortcut():
    """Create a Linux desktop shortcut"""
    desktop = Path.home() / "Desktop"
    shortcut_path = desktop / "Persona System.desktop"
    script_path = Path(__file__).parent / "start_personas.sh"
    
    try:
        with open(shortcut_path, 'w') as f:
            f.write(f'''[Desktop Entry]
Version=1.0
Type=Application
Name=Persona System
Comment=AI Persona Generator and Chat
Exec=bash "{script_path}"
Icon=applications-internet
Path={Path(__file__).parent}
Terminal=true
StartupNotify=false
''')
        
        os.chmod(shortcut_path, 0o755)
        print("✅ Desktop shortcut created!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating shortcut: {e}")
        return False

def main():
    print("🖥️  Creating desktop shortcut for Persona System...")
    
    if sys.platform == "win32":
        create_windows_shortcut()
    elif sys.platform == "darwin":
        create_mac_shortcut()
    elif sys.platform.startswith("linux"):
        create_linux_shortcut()
    else:
        print(f"❌ Unsupported platform: {sys.platform}")
    
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()
