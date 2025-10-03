#!/usr/bin/env python3
"""
Simple build script for MongoDB Backup Tool executables.
Creates cross-platform executables using PyInstaller.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def build_executable():
    """Build executable for current platform."""
    print("MongoDB Backup Tool - Simple Builder")
    print("=" * 40)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"[OK] PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("[ERROR] PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Check dependencies
    try:
        import pymongo
        import tkinter
        from bson import json_util
        print("[OK] All dependencies found")
    except ImportError as e:
        print(f"[ERROR] Missing dependency: {e}")
        return False
    
    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    print("[OK] Cleaned previous builds")
    
    # Build command
    current_platform = platform.system().lower()
    
    if current_platform == "windows":
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "MongoDB_Backup_Tool_Windows",
            "--add-data", "requirements.txt;.",
            "--add-data", "README.md;.",
            "mongodb_backup_gui_proper.py"
        ]
    elif current_platform == "darwin":  # macOS
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "MongoDB_Backup_Tool_macOS",
            "--add-data", "requirements.txt:.",
            "--add-data", "README.md:.",
            "mongodb_backup_gui_proper.py"
        ]
    else:
        print(f"[ERROR] Unsupported platform: {current_platform}")
        return False
    
    print(f"Building for {current_platform}...")
    
    try:
        subprocess.run(cmd, check=True)
        print("[OK] Build completed successfully!")
        
        # Check if executable was created
        if current_platform == "windows":
            exe_path = Path("dist") / "MongoDB_Backup_Tool_Windows.exe"
        else:
            exe_path = Path("dist") / "MongoDB_Backup_Tool_macOS"
        
        if exe_path.exists():
            print(f"[OK] Executable created: {exe_path}")
            print(f"Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            return True
        else:
            print("[ERROR] Executable not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed: {e}")
        return False

def main():
    """Main function."""
    success = build_executable()
    
    if success:
        print("\n" + "=" * 40)
        print("BUILD SUCCESSFUL!")
        print("=" * 40)
        print("Your executable is ready in the 'dist' folder.")
        print("You can now distribute this executable to users.")
    else:
        print("\n" + "=" * 40)
        print("BUILD FAILED!")
        print("=" * 40)
        print("Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
